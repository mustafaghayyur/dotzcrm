"""
    Please read the README.md in this folder before using.
"""

from querysets.tasks import *
from tasks.models import *
from . import CRUD as crud  # generic, parent crud class
from core import settings
from core.helpers import crud

class CRUD(crud):
    idCols = None
    space = 'tasks'

    def __init__(self):
        self.idCols = settings['rdbms']['tasks']['keys']['only_pk']

    def create(self, dictionary):
        self.dictValidation(self.space, 'create', dictionary)

        task_id = self.createMasterTable(dictionary)

        if not task_id or isinstance(task_id, int):
            raise Exception('Something went wrong. Task could not be created in: Tasks.CRUD.create().')

        # Time to create child records:
        for pk in self.idCols:
            if pk == 'tid':
                continue

            tbl = pk[0]  # table abbreviation
            model = settings['rdbms']['tasks']['model_names'][tbl]  # identify model
            table = settings['rdbms']['tasks']['table_names'][tbl]  # identify table
            cols = settings['rdbms']['tables'][table]  # grab column names
            dictionary['tid'] = task_id

            self.createChildTable(model, table, cols, dictionary)
            
    def read(self, selectors, conditions, orderBy, limit):
        # some logic...

        user_id = 1
        rawObj = Task.rawobjects.fetchTasks(user_id, selectors, conditions, orderBy, limit)

        if rawObj:
            return rawObj

        return None

    def update(self, dictionary):
        self.dictValidation(self.space, 'update', dictionary)

        if 'tid' not in dictionary:
            raise Exception('Update operation needs task id, in: Tasks.CRUD.update().')

        if not isinstance(dictionary['tid'], int) or dictionary['tid'] < 1:
            raise Exception('Task ID provided must be of int() format and greater than zero, in: Tasks.CRUD.update().')

        task = Task.objects.filter(id=dictionary['tid'])
        if not task:
            raise Exception('No valid record found for provided Task ID, in: Tasks.CRUD.update().')

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            if pk == 'tid':
                self.updateMasterTable('tasks', task, dictionary)
                continue

            tbl = pk[0]  # table abbreviation
            model = settings['rdbms']['tasks']['model_names'][tbl]  # identify model
            table = settings['rdbms']['tasks']['table_names'][tbl]  # identify table
            cols = settings['rdbms']['tables'][table]  # grab column names

            if pk not in dictionary:  # create a new record for child table
                self.createChildTable(model, table, cols, dictionary)
                continue

            # we have a proper record to update
            latest = {model}.rawobjects.fetchLatest(user_id=1, dictionary['tid'])  # fetch latest record for table:
            updateRequired = False

            if not latest:
                self.createChildTable(model, table, cols, dictionary)
                continue

            rec = {}  # initiate new dictionary
            for key in dictionary:
                if crud.isProblematicKey(self.space, tbl, key):
                    key = key[1:]  # chop off first character

                if key in cols:  # check if this key is relevant to the current table
                    rec[key] = dictionary[key]  # store in rec in case an update is necessary
                    
                    if dictionary[key] != latest.{key}
                        updateRequired = True  # changes found in dictionary record

            if updateRequired:  # update record for child table
                self.updateChildTable(model, table, cols, rec, latest.id)
                    

                    
        

    def delete(self, modelName, obj):
        # Delete the tasks
        model = self.fetchModel(modelName)
        model.delete(obj)
