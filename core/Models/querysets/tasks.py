from . import records
from core.settings import tasks, rdbms
from core.helpers import strings


##########################################################################
# TasksQuerySet customizes generic RecordsQuerySet to be usable by Tasks module.
#
# DO NOT use raw queries anywhere outside of QuerySets in this CRM.
##########################################################################
class TasksQuerySet(records.QuerySet):

    def __init__(self, model=None, query=None, using=None, hints=None):
        self.tableCols = rdbms['tasks']['keys']['full_record']
        self.space = 'tasks'  # used by some modules

        super().__init__(model, query, using, hints)
        
    # NOTE: Watchers table is not query-able in this comprehensive search.
    #       Will have to query all watchers separately.
    def fetchTasks(self, user_id, selectors = [], conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        """
        # Fetches full Task records with latest records (of sub tables).
        #
        # PARAMS:
        #  - user_id: [int] the current user's ID
        #  - selectors: [list] list of columns you wish the result set to carry (from all Tasks' tables combined)
        #  - conditions: [dictionary] book of parameters for which tasks should be fetched. The 'conditions' dictionary defines which tasks will be fetched.
        #  - orderBy: [string] any specific ordering you want.
        #  - limit: [string] number of records you want retrieved.
        """
        obj = self._compileVariables(user_id, selectors, conditions, orderBy, limit)

        selectString = obj['selectString']
        whereStatements = strings.concatenate(obj['whereStatements'])
        params = obj['params']
        joins = obj['joins']

        # sub it any column names you wish to output differently in the ORM
        translations = {}
        
        query = f"""
            SELECT {selectString}
            FROM tasks_task AS t
            {joins}
            WHERE {whereStatements} 
            ORDER BY {orderBy} LIMIT {limit};
            """
        return self.raw(query, params, translations)

    def _generateDefaultConditions(self, user_id):
        s = tasks['values']['status']
        params = {
            "assignee_id": user_id,
            #"delete_time": 'IS NULL',  # needs to be handled
            "tupdate_time": tasks['recentInterval'],
            "latest": tasks['values']['latest']['latest'],
            "visibility": tasks['values']['visibility']['private'],
            "status": [s['assigned'], s['viewed'], s['queued'], s['started'], s['reassigned']],
        }

        return params

    # define how each join statement should be formed:
    def _generateJoinStatements(self, selectors, conditions):
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



class DetailQuerySet(records.ChildrenQuerySet):
    tbl = 'tasks_details'
    master_col = 'task_id'
    valTbl = 'tasks_assignment'
    valCol = 'assignor_id'


class DeadlineQuerySet(records.ChildrenQuerySet):
    tbl = 'tasks_deadline'
    master_col = 'task_id'
    valTbl = 'tasks_assignment'
    valCol = 'assignor_id'


class StatusQuerySet(records.ChildrenQuerySet):
    tbl = 'tasks_status'
    master_col = 'task_id'
    valTbl = 'tasks_assignment'
    valCol = 'assignor_id'


class VisibilityQuerySet(records.ChildrenQuerySet):
    tbl = 'tasks_assignment'
    master_col = 'task_id'
    valTbl = 'tasks_assignment'
    valCol = 'assignor_id'


class WatacherQuerySet(records.ChildrenQuerySet):
    tbl = 'tasks_watcher'
    master_col = 'task_id'
    valTbl = 'tasks_assignment'
    valCol = 'assignor_id'

    def fetchAllCurrentWatchers(self, user_id, task_id):
        pass

    def fetchAllWatchersHistory(self, user_id, task_id):
        pass

    def fetchSpecificWatcherHistory(self, user_id, task_id):
        pass

class AssignmentQuerySet(records.ChildrenQuerySet):
    tbl = 'tasks_visibility'
    master_col = 'task_id'

