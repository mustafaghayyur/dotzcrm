from . import master, child
from core.Models.mappers.tasks import *

"""
    REFORMATION (Notes):
    -----------------------------
    So far we have worked with MT and CT in QuerySets.
    But what if, we could make QuertSet.fetch() so generic that it could fetch
    anything? Thus making the CT/MT distinction for fetches void...

    We will now attempt so:
     1) C.U.D. in CRUD operations remain unchanged. This is absolute.
     2) QuersySet will become a singular entity that any table, whether CT, MT
        or M2MCT/RLCCT alike can be based off of. And allows for highly
        versatile retrievals/select statements.

    queryset_reformation2 branch CANNOT have any changes to core.Models.CRUD.
    To ensure only QuerySets are modified, and that they still output the exact
    same returns as before.
"""
class TaskQuerySet(master.MTQuerySet):
    """
        TaskQuerySet allows for highly versatile Select queries to DB.
        For One-to-One data models (i.e. records).
    """
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.app = 'tasks'
        self.mapper = TasksMapper()
        self.valuesMapper = ValuesMapper()
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
        super().fetch(selectors, conditions, orderBy, limit)


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

