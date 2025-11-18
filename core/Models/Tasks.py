from .querysets.tasks import *
from tasks.models import *
from .background.CRUD import Generic  # generic, parent crud class
from core.settings import rdbms, tasks
from core.helpers import misc

"""
    Handles ALL crud operations for Tasks Module of DotzCRM.
    Please read the README.md in this folder before using.
"""
class CRUD(Generic):

    def __init__(self):
        self.idCols = rdbms['tasks']['keys']['only_pk']
        self.space = 'tasks'
        self.mtabbrv = rdbms['tasks']['master_table_abbrv']
        self.mtModel = Task

        super().__init__()

    def create(self, dictionary):
        return super().create(dictionary)

    def read(self, selectors, conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        if not isinstance(selectors, list) or len(selectors) < 1:
            raise Exception(f'Record fetch request for {self.space} failed. Improper selectors, in {self.space}.CRUD.read()')

        if 'all' in selectors:
            selectors = list(rdbms['tasks']['keys']['full_record'].keys())

        user_id = 1
        rawObj = Task.objects.fetchTasks(user_id, selectors, conditions, orderBy, limit)
        
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
            "latest": tasks['values']['latest']['latest'],
            "visibility": None,
            "status": None,
            "tid": task_id,
        }

        rawObj = self.read(['all'], conditions)

        if rawObj:
            return rawObj[0]  # we only want one
        return None

