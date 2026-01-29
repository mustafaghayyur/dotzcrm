from core.DRMcore.querysets import QuerySet, child
from .mappers import *

"""
    We are now removing MT/CT distinction from QuerySets.
"""
class TaskQuerySet(QuerySet.QuerySetManager):
    """
        TaskQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()

        

class DetailQuerySet(child.CTQuerySet):
    tbl = 'tasks_details'
    app = 'tasks'
    mapper = TasksMapper()


class DeadlineQuerySet(child.CTQuerySet):
    tbl = 'tasks_deadline'
    app = 'tasks'
    mapper = TasksMapper()


class StatusQuerySet(child.CTQuerySet):
    tbl = 'tasks_status'
    app = 'tasks'
    mapper = TasksMapper()


class VisibilityQuerySet(child.CTQuerySet):
    tbl = 'tasks_assignment'
    app = 'tasks'
    mapper = TasksMapper()


class WatcherQuerySet(child.M2MQuerySet):
    tbl = 'tasks_watcher'
    app = 'tasks'
    mapper = TasksMapper()

class AssignmentQuerySet(child.CTQuerySet):
    tbl = 'tasks_visibility'
    app = 'tasks'
    mapper = TasksMapper()

class CommentQuerySet(child.RLCQuerySet):
    tbl = 'tasks_comment'
    app = 'tasks'
    mapper = TasksMapper()

