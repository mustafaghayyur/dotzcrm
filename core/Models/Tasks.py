from .querysets.tasks import *
from tasks.models import *
from .background import CRUD, Comments  # generic, parent crud class
from .background.CRUD import Generic  # generic, parent crud class

"""
    Handles ALL crud operations for Tasks Module of DotzCRM.
    Please read the README.md in this folder before using.
"""
class CRUD(CRUD.Generic):

    def __init__(self):
        self.space = 'tasks'  # holds the name of current module/space
        self.mtModel = Task  # holds the class reference for Master Table's model

        super().__init__()

    def create(self, dictionary):
        return super().create(dictionary)

    def read(self, selectors, conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        if not isinstance(selectors, list) or len(selectors) < 1:
            raise Exception(f'Record fetch request for {self.space} failed. Improper selectors, in {self.space}.CRUD.read()')

        if 'all' in selectors:
            selectors = list(self.dbConfigs['keys']['full_record'].keys())

        user_id = 1
        rawObj = self.mtModel.objects.fetchTasks(user_id, selectors, conditions, orderBy, limit)
        
        if rawObj:
            return rawObj

        return None

    def update(self, dictionary):
        return super().update(dictionary)

    def delete(self, task_id):
        # Delete the tasks
        super().delete(task_id)

    def fetchFullRecordForUpdate(self, task_id):
        conditions = {
            #"assignee_id": None,
            "update_time": None,
            "latest": self.module['values']['latest']['latest'],
            "visibility": None,
            "status": None,
            "tid": task_id,
        }

        rawObj = self.read(['all'], conditions)

        if rawObj:
            return rawObj[0]  # we only want one
        return None

class Comments(Comments.CRUD):
    def __init__(self):
        pass

    def readComments(self, definitions):
        if not isinstance(definitions, dictionary) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        for pk in self.idCols:
            if self.dbConfigs['models'][pk] != 'Comment'
                continue

            user_id = 1
            model = globals()[self.dbConfigs['models'][pk]]
            if pk in selectors:
                # specific record being saught:
                rawObj = model.objects.fetchRevisionlessById(user_id, selectors[self.dbConfigs['mtId']], selectors[pk])

            else:
                rawObj = model.objects.fetchAllRevisionlessByMaster(user_id, selectors[self.dbConfigs['mtId']])
        
        if rawObj:
            return rawObj

        return None
