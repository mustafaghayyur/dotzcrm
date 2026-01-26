from core.DRMcore.querysets import master, child
from .mappers import *
from .mapper_values import ValuesMapper

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

