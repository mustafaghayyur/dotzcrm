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
        

    def updateChildTable(self, ModelInstance, latestRecord, tbl, tableName, columnsList, newRecordDictionary, dicKey):
        ignore = rdbms[self.space]['updates']['ignore'][tableName]
        fields = {
            'delete_time': timezone.now(),
            'latest': 2
        }

        latestRecord.update(**fields)  # update old record with deletion info

        for col in columnsList:
            if col in ignore:
                continue

            if crud.isProblematicKey(rdbms[self.space]['keys']['problematic'], col, True):
                key = tbl + col  # needs prefix added to column name to match dict key
            else:
                key = col

            fields[col] = newRecordDictionary[key]





        Details.save(obj['details'])
        Deadline.save(obj.['deadline'])
        Status.save(obj.['status'])
        Visibility.save(obj.['visibility'])
        Watcher.save(obj.['watcher'])
        Assignment.save(obj.['assignment'])
        pass

    def createChildTable(self, modelName, tableName, columnsList, newRecordDictionary):
        pass

    def createMasterTable(self, newRecordDictionary):
        pass

    def getCorrectUpdateValue(self, column, tbl, dic, qSet):
        
        

        if newRecordDictionary[key] is None:
            if column == 'update_time':
                return timezone.now()

            return qSet.{column}



    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to Tasks.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

