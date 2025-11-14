"""
    Please read the README.md in this folder before using.
"""

from querysets.tasks import *
from tasks.models import *
from .CRUD import Generic  # generic, parent crud class
from core import settings
from core.helpers import crud

class CRUD(Generic):
    idCols = None
    space = 'tasks'

    def __init__(self):
        self.idCols = settings['rdbms']['tasks']['keys']['only_pk']

    def create(self, dictionary):
        self.dictValidation(self.space, 'create', dictionary)

        task_id = self.createMasterTable(Task, dictionary)

        if not task_id or isinstance(task_id, int):
            raise Exception('Something went wrong. Task could not be created in: Tasks.CRUD.create().')

        # Time to create child records:
        for pk in self.idCols:
            if pk == 'tid':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(settings['rdbms'], self.space, tbl)
            dictionary['tid'] = task_id

            self.createChildTable(t['model'], t['table'], t['cols'], dictionary)
            
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
            tbl = pk[0]  # table abbreviation

            if pk == 'tid':
                self.updateMasterTable('tasks', task, dictionary)
                continue

            t = crud.generateModelInfo(settings['rdbms'], self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            if pk not in dictionary:  # create a new record for child table
                self.createChildTable(model, t['table'], t['cols'], dictionary)
                continue

            # we have a proper record to update
            latest = model().rawobjects.fetchLatest(1, dictionary['tid'])  # fetch latest record for table:
            updateRequired = False

            if not latest:
                self.createChildTable(model, t['table'], t['cols'], dictionary)
                continue

            rec = {}  # initiate new dictionary
            for col in t['cols']:
                if crud.isProblematicKey(settings['rdbms'][self.space]['keys']['problematic'], self.space, col, True):
                    key = tbl + col  # need tbl_abbrv for comparison

                if key in dictionary:
                    rec[col] = dictionary[key]  # store in rec in case an update is necessary
                    
                    if dictionary[key] != getattr(latest, col):
                        updateRequired = True  # changes found in dictionary record

            if updateRequired:  # update record for child table
                self.updateChildTable(model, latest, tbl, t['table'], t['cols'], rec)

    def delete(self, modelName, obj):
        # Delete the tasks
        model = self.fetchModel(modelName)
        model.delete(obj)
