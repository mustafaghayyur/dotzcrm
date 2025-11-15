"""
    Please read the README.md in this folder before using.
"""

from querysets.tasks import *
from tasks.models import *
from . import CRUD  # generic, parent crud class
from core import settings
from core.helpers import crud

class CRUD(CRUD.Generic):

    def __init__(self):
        self.idCols = settings['rdbms']['tasks']['keys']['only_pk']
        self.space = 'tasks'
        self.mtabbrv = settings['rdbms']['tasks']['master_table_abbrv']
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

    def delete(self, modelName, obj):
        # Delete the tasks
        model = self.fetchModel(modelName)
        model.delete(obj)
