from django.utils import timezone
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

        mtRecord = self.mtModel.objects.filter(id=dictionary[self.mtabbrv + 'id'])
        if not mtRecord:
            raise Exception(f'No valid record found for provided Task ID, in: {self.space}.CRUD.update().')

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation

            if pk == self.mtabbrv + 'id':
                self.updateMasterTable(self.space, mtRecord, dictionary)
                continue

            t = crud.generateModelInfo(settings['rdbms'], self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            if pk not in dictionary:  # create a new record for child table
                self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)
                continue

            # we have a proper record to update(possibly)
            latest = model().rawobjects.fetchLatest(1, dictionary[self.mtabbrv + 'id'])  # fetch latest record for table:

            if not latest:
                self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)
                continue

            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, latest, tbl, t['table'], t['cols'], dictionary)

    def updateMasterTable(self, space, QuerySet, newRecordDictionary):
        # update the QuerySet
        fields = {}
        fields['description'] = newRecordDictionary['description']
        fields['parant_id'] = newRecordDictionary['parent_id']
        fields['update_time'] = timezone.now()
        QuerySet.update(**fields)  # double-asterisk operator can be used to pass a dictionary as a collection of individual key=param arguments in Python
        return None

    def updateChildTable(self, modelClass, latestRecord, tbl, tableName, columnsList, newRecordDictionary):
        rec = {}  # initiate new dictionary
        updateRequired = False

        for col in columnsList:
            if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:
                rec[col] = newRecordDictionary[key]  # store in rec in case an update is necessary
                
                if newRecordDictionary[key] != getattr(latestRecord, col):
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:  # update record for child table
            latestRecord.delete_time = timezone.now()
            latestRecord.latest = 2
            latestRecord.save(update_fields=['delete_time', 'latest'])  # update old record with deletion info

            self.createChildTable(modelClass, tbl, tableName, columnsList, newRecordDictionary)

        return None

    def createChildTable(self, modelClass, tbl, tableName, columnsList, newRecordDictionary):
        """
        """
        newRecordDictionary['create_time'] = timezone.now()
        newRecordDictionary['latest'] = 1

        if settings['rdbms'][self.space]['master_id'] not in newRecordDictionary:
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        record = {}

        for col in columnsList:
            if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    record[col] = newRecordDictionary[key]

        record = modelClass(**record)
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

