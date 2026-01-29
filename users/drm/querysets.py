from core.DRMcore.querysets import master, child
from .mappers import *

"""
    We are now removing MT/CT distinction from QuerySets.
"""
class UserQuerySet(master.MTQuerySet):
    """
        UserQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.app = 'users'
        self.mapper = UsersMapper()
        self.columnsMatrix = self.mapper.generateO2OFields()

        super().__init__(model, query, using, hints)


class DetailQuerySet(child.CTQuerySet):
    tbl = 'tasks_details'
    app = 'tasks'
    mapper = UsersMapper()


class DeadlineQuerySet(child.CTQuerySet):
    tbl = 'tasks_deadline'
    app = 'tasks'
    mapper = UsersMapper()


class StatusQuerySet(child.CTQuerySet):
    tbl = 'tasks_status'
    app = 'tasks'
    mapper = UsersMapper()


class VisibilityQuerySet(child.CTQuerySet):
    tbl = 'tasks_assignment'
    app = 'tasks'
    mapper = UsersMapper()

