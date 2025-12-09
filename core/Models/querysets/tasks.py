from . import records
from core.Models.mappers import tasks as tasksMappers
from core import settings  # tasks, rdbms
from core.helpers import strings, misc

class TasksQuerySet(records.MasterTableQuerySet):
    """
        TasksQuerySet allows for highly versatile Select queries to DB.
        For One-to-One data models (i.e. records).
    """
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.space = 'tasks'  # used by some modules
        self.mapper = tasksMappers.TasksMapper()
        self.valuesMapper = tasksMappers.ValuesManager
        self.tableCols = self.mapper.generateO2OFields()

        super().__init__(model, query, using, hints)
        
    def fetchTasks(self, selectors = [], conditions = None, orderBy = 't.update_time DESC', limit = '20'):
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
        obj = self._compileVariables(selectors, conditions, orderBy, limit)

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

        # misc.log(query, 'SEARCH QUERY STRING')
        # misc.log(params, 'SEARCH PARAMS')
        return self.raw(query, params, translations)

    def _generateDefaultConditions(self):
        # s = self.valuesMapper.status()
        params = {
            # "tdelete_time": 'IS NULL',  # @todo needs to be handled
            # "tupdate_time": settings.tasks['recentInterval'],
            "latest": self.valuesMapper.latest('latest'),
            # "visibility": self.valuesMapper.visibility('private'),
            # "status": [s['assigned'], s['viewed'], s['queued'], s['started'], s['reassigned']],
        }

        return params

    def _generateJoinStatements(self, selectors, conditions):
        """
            Forms Join statements string, as part of the search query.
        """
        tbls = self._getValidTablesUsed(selectors, conditions)
        joins = []

        for tbl in tbls:
            if tbl == 't' or tbl == '':
                continue
            if tbl == 'd':
                joins.append(' LEFT JOIN tasks_details AS d ON t.id = d.task_id')
            if tbl == 'l':
                joins.append(' LEFT JOIN tasks_deadline AS l ON t.id = l.task_id')
            if tbl == 's':
                joins.append(' LEFT JOIN tasks_status AS s ON t.id = s.task_id')
            if tbl == 'a':
                joins.append(' LEFT JOIN tasks_assignment AS a ON t.id = a.task_id')
            if tbl == 'v':
                joins.append(' LEFT JOIN tasks_visibility AS v ON t.id = v.task_id')
            if tbl == 'w':
                joins.append(' LEFT JOIN tasks_watcher AS w ON t.id = w.task_id')

            if 'latest' in conditions:
                joins.append(' AND '+tbl+'.latest = %(latest)s')

        return strings.concatenate(joins)



class DetailQuerySet(records.ChildQuerySet):
    tbl = 'tasks_details'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class DeadlineQuerySet(records.ChildQuerySet):
    tbl = 'tasks_deadline'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class StatusQuerySet(records.ChildQuerySet):
    tbl = 'tasks_status'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class VisibilityQuerySet(records.ChildQuerySet):
    tbl = 'tasks_assignment'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()


class WatcherQuerySet(records.M2MChildQuerySet):
    tbl = 'tasks_watcher'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()

class AssignmentQuerySet(records.ChildQuerySet):
    tbl = 'tasks_visibility'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()

class CommentQuerySet(records.RLCChildQuerySet):
    tbl = 'tasks_comment'
    master_col = 'task_id'
    space = 'tasks'
    mapper = tasksMappers.TasksMapper()
    valuesMapper = tasksMappers.ValuesManager()

