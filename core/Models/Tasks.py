"""
    Please read the README.md in this folder before using.
"""

from querysets.tasks import *
from tasks.models import *
from . import CRUD  # generic, parent crud class
from core.settings import rdbms, tasks

class CRUD(CRUD.Generic):

    def __init__(self):
        self.idCols = rdbms['tasks']['keys']['only_pk']
        self.space = 'tasks'
        self.mtabbrv = rdbms['tasks']['master_table_abbrv']
        self.mtModel = Task

    def create(self, dictionary):
        return super.create(dictionary)

    def read(self, selectors, conditions, orderBy, limit):
        # some logic...

        user_id = 1
        rawObj = Task.rawobjects.fetchTasks(user_id, selectors, conditions, orderBy, limit)

        if rawObj:
            return rawObj

        return None

    def update(self, dictionary):
        return super.update(dictionary)

    def delete(self, task_id):
        # Delete the tasks
        super.delete(self, task_id)

    def fetchFullRecordForUpdate(self, task_id):
        user_id = 1

        conditions = {
            "assignee_id": None,
            "update_time": None,
            "latest": tasks['values']['latest']['latest'],
            "visibility": None,
            "status": None,
            "tid": task_id,
        }

        selectors = list(rdbms.tasks.full_record.keys())
        
        rawObj = Task.rawobjects.fetchTasks(user_id, selectors, conditions, orderBy, 1)

        if rawObj:
            return rawObj

