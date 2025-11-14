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
        

    def updateChildTable(self, modelClass, latestRecord, tbl, tableName, columnsList, newRecordDictionary, dicKey):
        ignore = rdbms[self.space]['updates']['ignore'][tableName]
        fields = {
            'delete_time': timezone.now(),
            'latest': 2
        }

        latestRecord.update(**fields)  # update old record with deletion info

        newRecordDictionary['create_time'] = timezone.now()
        newRecordDictionary['latest'] = 1

        if 'id' in newRecordDictionary:
            del newRecordDictionary['id']

        if 'delete_time' in newRecordDictionary:
            del newRecordDictionary['delete_time']

        return self.createChildTable(modelClass, tableName, columnsList, newRecordDictionary)

    def createChildTable(self, modelClass, tbl, tableName, columnsList, newRecordDictionary):
        if rdbms[self.space]['master_id'] not in newRecordDictionary:
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        record = modelClass(**newRecordDictionary)
        return record.save()

    def createMasterTable(self, modelClass, newRecordDictionary):
        if 'id' in newRecordDictionary:
            raise Exception(f'Could not create master record; id already set. In {self.space}.CRUD.create()')
        if rdbms[self.space]['master_id'] in newRecordDictionary:
            raise Exception(f'Could not create master record; id already set. In {self.space}.CRUD.create()')

        tbl = self.space[0]
        acrnym = tbl + 'id'

        if acrnym in newRecordDictionary:
            raise Exception(f'Could not create master record; id already set. In {self.space}.CRUD.create()')

        tblColumns = rdbms['tables'][rdbms[self.space]['master_table']]
        record = {}

        for col in tblColumns:
            if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], self.space, col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                record[col] = newRecordDictionary[key]

        record = modelClass(**record)
        return record.save()

    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to {space}.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

