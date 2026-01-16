from django.utils import timezone
from . import Background
from core.helpers import crud

"""
    Handles all crud operations for Revision-less Children (RLC) tables.
"""
class CRUD(Background.CrudOperations):
    tbl = None
    pk = None  # primary-key of RLC table in question

    def __init__(self, MasterCRUDClass):
        self.masterCrudObj = MasterCRUDClass()
        super().__init__()

    def create(self, dictionary):
        """
            Creates single RLC CT record.
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        
        mtId = self.mapper.master('abbreviation') + 'id'
        # self.log(self.submission, 'FORM-------------------------------------')

        masterRecord = self.masterCrudObj.read([mtId], {mtId: self.submission[mtId]})
        self.log(masterRecord, 'JUST CONFIRMING if master record is being fetched correctly in createRLC()')

        if not masterRecord:
            raise Exception('Master Record could not be found. RLC cannot be created in {self.space}.CRUD.create()')

        t = crud.generateModelInfo(self.mapper, self.tbl)

        return self.createChildTable(t['model'], self.tbl, t['table'], t['cols'], True)
        
    def read(self):
        pass  # defined in individual Module's class extensions.

    def update(self, dictionary):
        """
            Updates single RLC CT record.
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        mtId = self.mapper.master('abbreviation') + 'id'
        mtForeignKey = self.mapper.master('foreignKeyName')

        # masterRecords gets the parent record id, to which this RLC belongs
        masterRecord = self.masterCrudObj.read([mtId], {mtId: self.submission[mtId]})
        self.log(masterRecord, 'JUST CONFIRMING if master record is being fetched correctly in updateRLC()')

        if not masterRecord:
            raise Exception(f'No valid record found for provided {self.space} ID for RLC update, in: {self.space}.CRUD.update().')

        
        originalRLC = self.read({self.pk: self.submission[self.pk], mtForeignKey: self.submission[mtForeignKey]})
        self.log(originalRLC, 'JUST CONFIRMING if originalRLC record is being fetched correctly in updateRLC()')

        if not originalRLC:
            raise Exception(f'No valid RLC record found for provided ID, in: {self.space}.CRUD.update().')
        
        t = crud.generateModelInfo(self.mapper, self.tbl)
            
        # determine if an update is necessary and carry out update operations...
        return self.updateChildTable(t['model'], self.tbl, t['table'], t['cols'], originalRLC, True)

    def deleteById(self, rlcId):
        """
            Deletion for specific RLC child record by its ID.
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save deletion update to DB. Else, throws an exception.
        """
        if not crud.isValidId({'id': rlcId}, 'id'):
            raise Exception(f'RLC Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        t = crud.generateModelInfo(self.mapper, self.tbl)

        return self.deleteChildTableById(t['model'], self.tbl, t['table'], t['cols'], rlcId)

    def deleteAllForMT(self, masterId):
        """
            Deletion for all child RLC records for master-table record.
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save deletion update to DB. Else, throws an exception.
        """
        if not crud.isValidId({'id': masterId}, 'id'):
            raise Exception(f'RLC Records could not be deleted. Invalid Master-ID supplied in {self.space}.CRUD.delete()')

        t = crud.generateModelInfo(self.mapper, self.tbl)

        return self.deleteChildTable(t['model'], self.tbl, t['table'], t['cols'], masterId, True)

    def deleteChildTableById(self, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteById()
            For RLC type nodes only
        """
        self.log(None, f'ENTERING deleteById for CT [{self.tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{self.tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
