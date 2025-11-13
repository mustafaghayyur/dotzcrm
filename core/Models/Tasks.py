"""
    Please read the README.md in this folder before using.
"""

from querysets.tasks import *
from tasks.models import *
from . import CRUD as crud
from . import settings

class CRUD(crud):
    idCols = None

    def __init__(self):
        self.idCols = settings.rdbms.tasks_keys.only_pk

    def create(self, obj):
        # some logic...
        Task.save(obj['master'])
        Details.save(obj['details'])
        Deadline.save(obj.['deadline'])
        Status.save(obj.['status'])
        Visibility.save(obj.['visibility'])
        Watcher.save(obj.['watcher'])
        Assignment.save(obj.['assignment'])

    def read(self, selectors, conditions, orderBy, limit):
        # some logic...

        user_id = 1
        rawObj = Task.rawobjects.fetchTasks(user_id, selectors, conditions, orderBy, limit)

        if rawObj:
            return rawObj

        return None

    def update(self, dictionary):
        if isinstance(dictionary, dict):
            if len(dictionary) > 0:
                
                # Loop through each defined Primary Key to see if its table needs an update
                for pk in self.idCols:
                    if pk in dictionary:
                        # we have a proper record to update
                        Model = settings['tasks']['model_names'][pk[0]]  # identify model
                        latest = {Model}.rawobjects.fetchRevision(1, 1, 0)  # fetch latest record for table:
                        
                        updateRequired = False
                        table = settings['tasks']['table_names'][pk[0]]  # identify table
                        cols = settings['rdbms']['table']  # grab column names

                        if latest:
                            rec = {}  # initiate new dictionary
                            for key in dictionary:
                                if key in cols:  # this key is relevant to the current table
                                    rec[key] = dictionary[key]  # store in rec in case an update is necessary
                                    
                                    if dictionary[key] != latest.{col}
                                        updateRequired = True  # changes found in dictionary record

                        if updateRequired:
                            self._updateModel(Model, table, cols, rec, latest)
                            # So what of the scenario where this child table has no existing
                            #  record to compare against?

                    
        Task.save(obj['master'])
        Details.save(obj['details'])
        Deadline.save(obj.['deadline'])
        Status.save(obj.['status'])
        Visibility.save(obj.['visibility'])
        Watcher.save(obj.['watcher'])
        Assignment.save(obj.['assignment'])

    def delete(self, modelName, obj):
        # Delete the tasks
        model = self.fetchModel(modelName)
        model.delete(obj)
