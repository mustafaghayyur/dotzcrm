from django.utils import timezone
from core.settings import rdbms
from core.helpers import crud

"""
    Generic CRUD Operations that can be used through out the system.
"""
class Generic:

    def __init__(self):
        # some code..

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
            if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], self.space, col, True):
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

        if rdbms[self.space]['master_id'] not in newRecordDictionary:
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        record = {}

        for col in columnsList:
            if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    record[col] = newRecordDictionary[key]

        record = modelClass(**record)
        return record.save()


    def createMasterTable(self, tbl, modelClass, newRecordDictionary):
        tblColumns = rdbms['tables'][rdbms[self.space]['master_table']]
        record = {}

        for col in tblColumns:
            if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], self.space, col, True):
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

