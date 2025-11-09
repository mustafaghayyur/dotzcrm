from django.db import models
from core.settings import tasks
from core.helpers import strings, misc


##########################################################################
# The QuerySet family of definitions will be essential to maintaining
# strict data-integrity and database-interactions standards.
# Where Python ORM's standard functions are not used to operate
# on the MySQL DB, these QuerySet methods should be used to
# interact with the MySQL DB.
# DO NOT use raw queries anywhere outside of QuerySets in this CRM.
##########################################################################
class TasksQuerySet(models.QuerySet):
    
    # these are all the column names callable in the fetchTasks() query generator
    # individual child table's create/delete datetime cols cannot be fetched in the fetchTasks() call
    tableCols = {
        'id': 't',
        'description': 't',
        'create_time': 't',
        'update_time': 't',
        'delete_time': 't',
        'creator_id': 't',
        'parent_id': 't',
        'details': 'd',
        'deadline': 'l',
        'status': 's',
        'visibility': 'v',
        'assignor_id': 'a',
        'assignee_id': 'a',
        'watcher_id': 'w',
        'latest': ''
        }

    def fetchTasks(self, user_id, selectors = [], conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        """
        # Fetches full Task records with latest records (of sub tables).
        # The 'keys' dictionary defines which tasks will be fetched.
        # PARAMS:
        #  - user_id: [int] the current user's ID
        #  - selectors: [list] list of columns you wish the result set to carry (from all Tasks' tables combined)
        #  - conditions: [dictionary] book of parameters for which tasks should be fetched.
        """        
        defaultConditions = self.generateDefaultConditions()

        if conditions is None:
            conditions = {}

        actualConditions = self.mergeConditions(defaultConditions, conditions)

        whereStatements = []
        params = {}
        i = 0
        tbl = self.tableCols

        for key, item in actualConditions:
            whereStatements[i] = self.generateWhereStatements(i, tbl[key], key)
            params[key] = item
            i += 1

        selectString = self.generateProperSelectors(selectors, tbl)

        # sub it any column names you wish to output differently in the ORM
        translations = {}

        start = 'SELECT ' + selectString
        
        start += """
            FROM tasks_task AS t
                LEFT JOIN tasks_taskdetails AS d ON t.id = d.task_id
                LEFT JOIN tasks_taskdeadline AS l ON t.id = l.task_id
                LEFT JOIN tasks_taskstatus AS s ON t.id = s.task_id
                LEFT JOIN tasks_taskuserassignment AS a ON t.id = a.task_id
                LEFT JOIN tasks_taskvisibility AS v ON t.id = v.task_id
            WHERE """
        
        if 'latest' in actualConditions:
            latest = """ d.latest <> %(latest)s AND l.latest <> %(latest)s AND s.latest <> %(latest)s
                AND a.latest <> %(latest)s AND v.latest <> %(latest)s"""
        else:
            latest = ''

        end = " ORDER BY " + orderBy + " LIMIT " + limit + ";"

        wheres = strings.concatenate(whereStatements)
        query = strings.concatenate([start, wheres, latest, end])
        misc.log(query, 'REMEMBER MG: THE inputs CANNOT have quotes around them!!!!')

        return self.raw(query, params, translations)

    def generateProperSelectors(self, selectors, table):
        string = ''
        
        for key in selectors:
            if key == 'details':
                string += ' ' + table[key] + '.description AS ' + key + ','
                continue

            string += ' ' + table[key] + '.' + key +','

        return string[:-1]

    def generateWhereStatements(self, i, tbl, key):
        andPref = ''

        if i > 0:
            andPref = ' AND '

        if key == 'latest':
            return ''

        if key in ['update_time', 'delete_time', 'create_time']:
            return andPref + '(' + tbl + '.' + key + ' >= NOW() - INTERVAL %(' + key + ')s DAY OR ' + tbl + '.' + key + ' IS NULL )'

        if isinstance(item, list):
            return andPref + tbl + '.' + key + ' IN (%(' + key + ')s)'
        
        if isinstance(item, str):
            return andPref + tbl + '.' + key + ' = %(' + key + ')s'

        return ''

    def generateDefaultConditions(self, user_id):
        params = {
            "assignee_id": user_id,
            "delete_time": 'IS NULL',
            "update_time": tasks.recentInterval,
            "latest": tasks.keys.latest.archive,
            "visibility": tasks.keys.visibility.private,
            "status": [tasks.keys.status.completed, tasks.keys.status.failed],
        }

        return params

    def mergeConditions(self, defaults, provided):
        conditions = defaults | provided  # merge provided conditions into the defaults
        final = self.validateConditions(conditions)
        return final

    def validateConditions(self, conditions):

        for k, v in conditions:
            if k in keys:
                if isinstance(v, str) or isinstance(v, list):
                    continue
                else:
                    conditions[k] = ''
            else:
                del conditions[k]  # delete the key from dictionary
                


class TaskDetailQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskDeadlineQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskStatusQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])

class TaskVisibilityQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskWatacherQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskAssignmentQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])

