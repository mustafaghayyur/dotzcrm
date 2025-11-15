from django.utils import timezone
from tasks.models import *
from core.helpers import crud
from core import settings

"""
    Generic CRUD Operations that can be used through out the system.
"""
class Generic:
    idCols = None
    space = None
    mtabbrv = None  # master-table-abbreviation
    mtModel = None  # master-table-modelClass

    def __init__(self):
        # some code..
        pass

    def create(self, dictionary):
        self.dictValidation(self.space, 'create', dictionary)

        mtId = self.createMasterTable(self.mtabbrv, self.mtModel, dictionary)

        if not mtId or not isinstance(mtId, int):
            raise Exception(f'Something went wrong. {self.space} could not be created in: {self.space}.CRUD.create().')

        # Time to create child records, loop through each child table:
        for pk in self.idCols:
            if pk == self.mtabbrv + 'id':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(settings['rdbms'], self.space, tbl)
            dictionary[settings['rdbms'][self.space]['master_id']] = mtId  # add master table ID to dictionary

            self.createChildTable(t['model'], tbl, t['table'], t['cols'], dictionary)

    def read(self):
        pass

    def update(self, dictionary):
        self.dictValidation(self.space, 'update', dictionary)

        if self.mtabbrv + 'id' not in dictionary:
            raise Exception(f'Update operation needs {self.space} id, in: {self.space}.CRUD.update().')

        if not isinstance(dictionary['tid'], int) or dictionary['tid'] < 1:
            raise Exception(f'{self.space} ID provided must be of int() format and greater than zero, in: {self.space}.CRUD.update().')

        #mtRecord = self.mtModel.objects.filter(id=dictionary[self.mtabbrv + 'id'])
        completeRecord = self.fetchFullRecordForUpdate(dictionary['tid'])

        if not completeRecord:
            raise Exception(f'No valid record found for provided Task ID, in: {self.space}.CRUD.update().')

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(settings['rdbms'], self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            if pk == self.mtabbrv + 'id':
                self.updateMasterTable(self.space, completeRecord, dictionary, model, t['table'], t['cols'])
                continue

            if pk not in dictionary:  # create a new record for child table
                self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)
                continue

            if not latest:
                self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)
                continue

            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, completeRecord, tbl, t['table'], t['cols'], dictionary)

    def delete(self, masterId):
        # Delete the tasks
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'{self.space} Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        if not mtRecord:
            raise Exception(f'Record for {self.space} could not be found. Therefore delete operation has failed, in {self.space}.CRUD.delete()')

        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation

            if pk == self.mtabbrv + 'id':
                continue  # skip, we delete master table at the end.

            t = crud.generateModelInfo(settings['rdbms'], self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            # run a 'delete' operation for latest child table record. 
            self.deleteChildTable(model, latest, tbl, t['table'], t['cols'], masterId)

        # once all children records have been updated with delete markers
        self.deleteMasterTable(masterId)

    def deleteChildTable(self, modelClass, latestRecord, tbl, tableName, columnsList, masterId):
        fieldsF = {}
        fieldsF[settings['rdbms'][self.space]['master_id']] = masterId
        fieldsF['latest'] = settings[self.space]['values']['latest']['latest']
        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = settings[self.space]['values']['latest']['archive']
        
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    def deleteMasterTable(self, masterId):
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']
        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    def updateMasterTable(self, space, completeRecord, newRecordDictionary, mtModel, tableName, columnsList):
        # update the QuerySet
        fields = {}

        for col in columnsList:
            if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                key = self.mtabbrv + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:                
                if newRecordDictionary[key] != getattr(completeRecord, col):
                    fields[col] = newRecordDictionary[key]

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=newRecordDictionary[self.mtabbrv + 'id']).update(**fields)
        return None

    def updateChildTable(self, modelClass, completeRecord, tbl, tableName, columnsList, newRecordDictionary):
        updateRequired = False
        for col in columnsList:
            if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:                
                if newRecordDictionary[key] != getattr(completeRecord, col):
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:  # update record for child table
            fields = {}
            fields['delete_time'] = timezone.now()
            fields['latest'] = 2
            
            modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
            self.createChildTable(modelClass, tbl, tableName, columnsList, newRecordDictionary)

        return None

    def createChildTable(self, modelClass, tbl, tableName, columnsList, newRecordDictionary):
        """
        """
        if settings['rdbms'][self.space]['master_id'] not in newRecordDictionary:
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        fields = {}

        for col in columnsList:
            if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    fields[col] = newRecordDictionary[key]

        fields['create_time'] = timezone.now()
        fields['latest'] = 1
        record = modelClass(**fields)
        return record.save()

    def createMasterTable(self, tbl, modelClass, newRecordDictionary):
        tblColumns = settings['rdbms']['tables'][settings['rdbms'][self.space]['master_table']]
        record = {}

        for col in tblColumns:
            if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    record[col] = newRecordDictionary[key]

        record = modelClass(**record)
        return record.save()

    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to {space}.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

