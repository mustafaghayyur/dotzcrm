from django.utils import timezone
from core.settings import rdbms
from core.helpers import crud

"""
    Generic CRUD Operations that can be used through out the system.
"""
class Generic:

    def __init__(self):
        # some code..

    def updateMasterTable(self, space, tbl, QuerySet, newRecordDictionary):
        t = generateModelInfo(rdbms, space, tbl)
        query = ''
        for col in t['cols']:
            val = self.getCorrectUpdateValue(col, tbl, newRecordDictionary, QuerySet)
            query += col + '=' + newRecordDictionary[col]
        QuerySet.save(obj['master'])
        pass

    def updateChildTable(self, modelName, tableName, columnsList, newRecordDictionary, latestRecordId):
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
        
        if crud.isProblematicKey(rdbms, self.space, column, True):
            # needs prefix added to column name to match dict key
            key = tbl + column

        if newRecordDictionary[key] is None:
            if column == 'update_time':
                return timezone.now()
            
            return qSet.{column}



    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to Tasks.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

