from core.DRMcore.querysets import master, child
from .mappers import *

"""
    We are now removing MT/CT distinction from QuerySets.
"""
class TaskQuerySet(master.MTQuerySet):
    """
        TaskQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.app = 'tasks'
        self.mapper = TasksMapper(ValuesMapper)
        self.columnsMatrix = self.mapper.generateO2OFields()

        super().__init__(model, query, using, hints)
        
    def fetch(self, selectors = [], conditions = None, orderBy = None, limit = None):
        """
        # Fetches full Task records with latest One-to-One records (of sub tables).
        #
        # PARAMS:
        #  - selectors: [list] list of columns you want
        #  - conditions: [dictionary] key=>value pairs of what to select.
        #  - orderBy: [string] any specific, legitimate ordering you want.
        #  - limit: [string] number of records you want retrieved. Can accept offsets.
        #
        # See documentation on legitimate ways of forming selectors, conditions, etc in this call.
        """
        return super().fetch(selectors, conditions, orderBy, limit)


class DetailQuerySet(child.CTQuerySet):
    tbl = 'tasks_details'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)


class DeadlineQuerySet(child.CTQuerySet):
    tbl = 'tasks_deadline'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)


class StatusQuerySet(child.CTQuerySet):
    tbl = 'tasks_status'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)


class VisibilityQuerySet(child.CTQuerySet):
    tbl = 'tasks_assignment'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)


class WatcherQuerySet(child.M2MQuerySet):
    tbl = 'tasks_watcher'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)

class AssignmentQuerySet(child.CTQuerySet):
    tbl = 'tasks_visibility'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)

class CommentQuerySet(child.RLCQuerySet):
    tbl = 'tasks_comment'
    app = 'tasks'
    mapper = TasksMapper(ValuesMapper)

