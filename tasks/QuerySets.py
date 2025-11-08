from django.db import models
from dotzcore import settings
from .helpers.strings

from .helpers.misc import log

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
    tableCols = ['id', 'description', 'create_time', 'update_time', 'delete_time', 'creator_id', 'parent_id', 'details', 'deadline', 'status', 'visibility', 'assignor_id', 'assignee_id', 'watcher_id', 'latest']


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
        tbl = self.generateTablesList()

        for key, item in actualConditions:
            whereStatements[i] = self.generateWhereStatements(i, tbl[key], key)
            params[key] = item
            i += 1

        # sub it any column names you wish to output differently in the ORM
        translations = {}

        start = """
            SELECT t.id, t.description, t.create_time, t.update_time, t.creator_id, t.parent_id
                d.description AS details,
                l.deadline, s.status, a.assignor_id
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
        log(query, 'REMEMBER MG: THE inputs CANNOT have quotes around them!!!!')

        return self.raw(query, params, translations)

    def generateWhereStatements(self, i, tbl, key):
        if i > 0:
            andPref = ' AND '

        if key == 'latest':
            return ''

        if key = 'update_time':
            return andPref + '(' + tbl + '.' + key + ' >= NOW() - INTERVAL %(' + key + ')s DAY OR ' + tbl + '.' + key + ' IS NULL )'

        if isinstance(item, list):
            return andPref + tbl + '.' + key + ' IN (%(' + key + ')s)'
        
        if isinstance(item, str):
            return andPref + tbl + '.' + key + ' = %(' + key + ')s'

        return ''

    def generateTablesList(self):
        """
        # Generates table acronyms for all col_names in fetchTasks() query.
        """
        tablesCols = {}
        i = 0

        for col in self.tableCols:
            if col in ['id', 'description', 'create_time', 'update_time', 'delete_time', 'creator_id', 'parent_id']:
                tableCols[col] = 't'
            if col in ['details']:
                tableCols[col] = 'd'
            if col in ['deadline']:
                tableCols[col] = 'l'
            if col in ['status']:
                tableCols[col] = 's'
            if col in ['visibility']:
                tableCols[col] = 'v'
            if col in ['assignor_id', 'assignee_id']:
                tableCols[col] = 'a'
            if col in ['watcher_id']:
                tableCols[col] = 'w'
            if col == 'latest':
                tableCols[col] = ''

            i += 1

        return tableCols

    def generateDefaultConditions(self, user_id):
        params = {
            "assignee_id": user_id
            "delete_time": 'IS NULL'
            "update_time": settings.task.recent_interval,
            "latest": settings.task.keys.latest.archive,
            "visibility": settings.task.keys.visibility.private,
            "status": [settings.task.keys.status.completed, settings.task.keys.status.failed]
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

