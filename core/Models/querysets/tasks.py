from . import master, child
from core.Models.mappers import tasks as tasksMappers
from core import settings  # tasks, rdbms
from core.helpers import strings, misc

class TaskQuerySet(master.MTQuerySet):
    """
        TaskQuerySet allows for highly versatile Select queries to DB.
        For One-to-One data models (i.e. records).
    """
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.app = 'tasks'
        self.mapper = tasksMappers.TasksMapper()
        self.valuesMapper = tasksMappers.ValuesManager()
        self.columnsMatrix = self.mapper.generateO2OFields()

        super().__init__(model, query, using, hints)
        
    def fetch(self, selectors = [], conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        """
        # Fetches full Task records with latest One-to-One records (of sub tables).
        #
        # PARAMS:
        #  - selectors: [list] list of columns you wish the result set to carry 
                (from all Tasks' O2O tables combined).
        #  - conditions: [dictionary] book of parameters which define what 
                tasks should be fetched. The 'conditions' dictionary defines 
                which tasks will be fetched.
        #  - orderBy: [string] any specific, legitimate ordering you want.
        #  - limit: [string] number of records you want retrieved. Can accept offsets.
        #
        # See documentation on legitimate ways of forming selectors, conditions, etc in this call.
        """
        obj = self.compileVariables(selectors, conditions, orderBy, limit)

        selectString = obj['selectString']
        whereStatements = strings.concatenate(obj['whereStatements'])
        params = obj['params']
        joins = obj['joins']

        # sub in any column names you wish to output differently in the ORM
        translations = {}
        
        query = f"""
            SELECT {selectString}
            FROM tasks_task AS t
            {joins}
            WHERE {whereStatements}
            ORDER BY {orderBy} LIMIT {limit};
            """

        misc.log(query, 'SEARCH QUERY STRING')
        misc.log(params, 'SEARCH PARAMS')
        return self.raw(query, params, translations)

    def generateDefaultConditions(self):
        # s = self.valuesMapper.status()
        params = {
            # "tdelete_time": 'IS NULL',  # @todo needs to be handled
            # "tupdate_time": settings.tasks['recentInterval'],
            "latest": self.valuesMapper.latest('latest'),
            # "visibility": self.valuesMapper.visibility('private'),
            # "status": [s['assigned'], s['viewed'], s['queued'], s['started'], s['reassigned']],
        }

        return params


class DetailQuerySet(child.CTQuerySet):
    tbl = 'tasks_details'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class DeadlineQuerySet(child.CTQuerySet):
    tbl = 'tasks_deadline'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class StatusQuerySet(child.CTQuerySet):
    tbl = 'tasks_status'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class VisibilityQuerySet(child.CTQuerySet):
    tbl = 'tasks_assignment'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class WatcherQuerySet(child.M2MQuerySet):
    tbl = 'tasks_watcher'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()

class AssignmentQuerySet(child.CTQuerySet):
    tbl = 'tasks_visibility'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()

class CommentQuerySet(child.RLCQuerySet):
    tbl = 'tasks_comment'
    app = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()

