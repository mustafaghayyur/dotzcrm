"""
    Please read the README.md in this folder before using.
"""

from querysets.tasks import *
from tasks.models import *

class CRUD:
    def __init__(self):
        # some logic...

    def create(self, obj):
        # some logic...
        Task.save(obj['master'])
        Details.save(obj['details'])
        Deadline.save(obj.['deadline'])
        Status.save(obj.['status'])
        Visibility.save(obj.['visibility'])
        Watcher.save(obj.['watcher'])
        Assignment.save(obj.['assignment'])

    def read(self, selectors, conditions, extras, orderBy, limit):
        # some logic...
        rawObj = Task.rawobjects.fetchTasks('1', ['id', 'description', 'create_time', 'update_time', 'status', 'visibility'])

        if rawObj:
            return rawObj

        return None

    def update(self, obj):
        # some logic...
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
