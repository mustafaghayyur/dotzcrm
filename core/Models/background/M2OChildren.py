from tasks.models import *
from core.helpers import crud  #, misc
from . import CRUD

"""
    Generic CRUD Operations that can be used through out the system.
    Only Many-to-One relationship CRUD operations are handled here.
"""
class CRUD(CRUD.Generic):

    def __init__(self):
        super().__init__()

    def createM2O(self, dictionary):
        """
            Attempts to create child(ren) records that hold a M2O relationship
            with Master Table.
            Creation of a single record per M2O CT.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        
        mtId = self.dbConfigs['mtAbbrv'] + 'id'

        masterRecord = self.read([mtId], {mtId: self.submission[mtId]})
        self.log(masterRecord, 'JUST CONFIRMING if master record is being fetched correctly in createM2O()')

        if not masterRecord:
            raise Exception('Master Record could not be found. M2O cannot be created in {self.space}.CRUD.create()')

        for pk in self.m2oidCols:
            tbl = pk[0]  # table abbreviation
            rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope
    
            self.createChildTable(model, tbl, t['table'], t['cols'])

    def readM2O(self):
        pass  # defined in individual Module's class extensions.

    def updateM2O(self, dictionary):
        """
            Attempts to update child(ren) records that hold a M2O relationship
            with Master Table.
            Update of a single record per M2O CT.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
        mtId = self.dbConfigs['mtAbbrv'] + 'id'

        # masterRecords gets the parent record id, to which this M2O belongs
        masterRecord = self.read([mtId], {mtId: self.submission[mtId]})
        self.log(masterRecord, 'JUST CONFIRMING if master record is being fetched correctly in updateM2O()')

        if not masterRecord:
            raise Exception(f'No valid record found for provided {self.space} ID for M2O update, in: {self.space}.CRUD.update().')

        for pk in self.m2oidCols:
            
            originalM2O = self.readM2Os({pk: self.submission[pk], mtId: self.submission[mtId]})
            self.log(originalM2O, 'JUST CONFIRMING if originalM2O record is being fetched correctly in updateM2O()')

            if not originalM2O:
                raise Exception(f'No valid M2O record found for provided ID, in: {self.space}.CRUD.update().')
            
            tbl = pk[0]  # child table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope
                
            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, tbl, t['table'], t['cols'], originalM2O)

    def deleteM2OById(self, m2oId):
        """
            Attempts to delete a single child record that of M2O relationship
            type, by its Unique ID.
        """
        if not isinstance(m2oId, int) or m2oId < 1:
            raise Exception(f'M2O Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.m2oidCols:

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.deleteChildTableById(model, tbl, t['table'], t['cols'], m2oId)

    def deleteAllM2OsForMT(self, masterId):
        """
            Attempts to delete all M2O-type children records for a MT ID
            provided.
        """
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'M2O Records could not be deleted. Invalid Master-ID supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.m2oidCols:
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
