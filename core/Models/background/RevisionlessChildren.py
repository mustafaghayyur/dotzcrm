from tasks.models import *
from core.helpers import crud
from .CRUD import Generic

"""
    Handles all crud operations for Revision-less Children (RLC).
"""
class CRUD(Generic):

    def __init__(self):
        super().__init__()

    def createRLC(self, dictionary):
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        
        mtId = self.dbConfigs['mtAbbrv'] + 'id'
        #self.log(self.submission, 'FORM-------------------------------------')

        masterRecord = self.read([mtId], {mtId: self.submission[mtId]})
        self.log(masterRecord, 'JUST CONFIRMING if master record is being fetched correctly in createRLC()')

        if not masterRecord:
            raise Exception('Master Record could not be found. RLC cannot be created in {self.space}.CRUD.create()')

        for pk in self.idCols:
            if self.dbConfigs['models'][pk] != 'Comment'
                continue

            tbl = pk[0]  # table abbreviation
            rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope
    
            self.createChildTable(model, tbl, t['table'], t['cols'])

    def readRLCs(self):
        pass  # defined in individual Module's class extensions.

    def updateRLC(self, dictionary):
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
        mtId = self.dbConfigs['mtAbbrv'] + 'id'

        # masterRecords gets the parent record id, to which this comment belongs
        masterRecord = self.read([mtId], {mtId: self.submission[mtId]})
        self.log(masterRecord, 'JUST CONFIRMING if master record is being fetched correctly in updateRLC()')

        if not masterRecord:
            raise Exception(f'No valid record found for provided {self.space} ID for comment update, in: {self.space}.CRUD.update().')

        for pk in self.idCols:
            
            if self.dbConfigs['models'][pk] != 'Comment':
                continue
            
            originalRLC = self.readRLCs({pk: self.submission[pk], mtId: self.submission[mtId]})
            self.log(originalRLC, 'JUST CONFIRMING if originalRLC record is being fetched correctly in updateRLC()')

            if not originalRLC:
                raise Exception(f'No valid comment record found for provided ID, in: {self.space}.CRUD.update().')
            
            tbl = pk[0]  # child table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope
                
            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, tbl, t['table'], t['cols'], originalRLC)

    def deleteRLCById(self, commentId):
        if not isinstance(commentId, int) or masterId < 1:
            raise Exception(f'RLC Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.idCols:
            if self.dbConfigs['models'][pk] != 'Comment':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.deleteChildTableById(model, tbl, t['table'], t['cols'], commentId)

    def deleteChildTableById(self, modelClass, tbl, tableName, columnsList, commentId):
        """
            Helper function for deleteRLCById()
        """
        self.log(None, f'ENTERING deleteById for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    def deleteAllRLCsForMT(self, masterId):
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'RLC Records could not be deleted. Invalid Master-ID supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.idCols:
            if self.dbConfigs['models'][pk] != 'Comment':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.deleteAllForChildTable(model, tbl, t['table'], t['cols'], masterId)

    def deleteAllForChildTable(self, modelClass, tbl, tableName, columnsList, masterId):
        """
            Helper function for deleteAllRLCsForMT()
        """
        self.log(None, f'ENTERING deleteAll for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[self.dbConfigs['mtId']] = masterId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)