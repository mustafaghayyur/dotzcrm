
"""
    Generic CRUD Operations that can be used through out the system.
"""
class Generic:

    def __init__(self):
        # some code..

    def updateMasterTable(self, space, QuerySet, newRecordDictionary):
        Task.save(obj['master'])
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

    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to Tasks.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

