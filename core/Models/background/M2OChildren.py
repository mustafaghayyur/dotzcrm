from tasks.models import *
from core.helpers import crud  # , misc
from . import CrudOperations

"""
    Many-to-One CRUD Operations that can be used through out the system.
    
    In a M2O relationship, there are two key columns to watch out for, the
    one ID (often MT ID) that cannot have multiples; and the many ID (CT) which 
    can show up numerous times in the result sets.
    
    By making sure many-correct FKs are handled correctly in reference to
    a single MT ID, we can keep the M2O relationship meaningful.
"""
class CRUD(CrudOperations.Background):

    def __init__(self, MasterCRUDClass):
        self.masterCrudObj = MasterCRUDClass()
        super().__init__()

    def create(self, dictionary):
        """
            Creation of a single record per M2O CT.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
        
        # no need to check valid MT ID. MySQL FK checks are enough.
        for pk in self.m2oIdCols:
            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope
            
            m2oKeys = self.dbConfigs['keys']['m2o'][t['table']]  # fetch m2o keys for table
            skip = False

            if not crud.isValidId(self.submission, m2oKeys['o']):
                skip = True

            if not crud.isValidId(self.submission, m2oKeys['m']):
                skip = True

            if skip:
                continue  # required IDs missing, skip this table

            self.createChildTable(model, tbl, t['table'], t['cols'])

    def read(self):
        pass  # defined in individual Module's class extensions.

    def update(self, dictionary):
        """
            Update of a single record per M2O CT.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
        
        # no need to check valid MT ID. MySQL FK checks are enough.
        for pk in self.m2oIdCols:
            tbl = pk[0]  # child table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope
            m2oKeys = self.dbConfigs['keys']['m2o'][t['table']]  # fetch m2o keys for table

            originalM2O = self.read({m2oKeys['o']: self.submission[m2oKeys['o']], m2oKeys['m']: self.submission[m2oKeys['m']]})
            self.log(originalM2O, 'JUST CONFIRMING if originalM2O record is being fetched correctly in updateM2O()')

            if not originalM2O:
                raise Exception(f'No valid M2O record found for provided ID, in: {self.space}.CRUD.update().')
                
            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, tbl, t['table'], t['cols'], originalM2O)

    def deleteById(self, m2oId):
        """
            Attempts to delete a single child record that of M2O relationship
            type, by its Unique ID.
        """
        if not isinstance(m2oId, int) or m2oId < 1:
            raise Exception(f'M2O Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.m2oIdCols:

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.deleteChildTableById(model, tbl, t['table'], t['cols'], m2oId)

    def deleteAllForMT(self, masterId):
        """
            Attempts to delete all M2O-type children records for a MT ID
            provided.
        """
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'M2O Records could not be deleted. Invalid Master-ID supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.m2oIdCols:
            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.deleteChildTable(model, tbl, t['table'], t['cols'], masterId, True)

    def deleteChildTableById(self, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteM2OById()
            For M2O type nodes only
        """
        self.log(None, f'ENTERING deleteById for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.module['values']['latest']['archive']

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
