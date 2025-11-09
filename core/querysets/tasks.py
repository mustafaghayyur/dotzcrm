from . import records
from core.settings import tasks
from core.helpers import strings, misc


##########################################################################
# TasksQuerySet customizes generic RecordsQuerySet to be usable by Tasks module.
#
# DO NOT use raw queries anywhere outside of QuerySets in this CRM.
##########################################################################
class TasksQuerySet(records.QuerySet):
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
        whereStatements = obj['whereStatements']
        conditions = obj['conditions']
        params = obj['params']

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
        
        if 'latest' in conditions:
            latest = """ d.latest <> %(latest)s AND l.latest <> %(latest)s AND s.latest <> %(latest)s
                AND a.latest <> %(latest)s AND v.latest <> %(latest)s"""
        else:
            latest = ''

        end = " ORDER BY " + orderBy + " LIMIT " + limit + ";"

        wheres = strings.concatenate(whereStatements)
        query = strings.concatenate([start, wheres, latest, end])
        misc.log(query, 'REMEMBER MG: THE inputs CANNOT have quotes around them!!!!')

        return self.raw(query, params, translations)

    def _generateDefaultConditions(self, user_id):
        params = {
            "assignee_id": user_id,
            "delete_time": 'IS NULL',
            "update_time": tasks.recentInterval,
            "latest": tasks.keys.latest.archive,
            "visibility": tasks.keys.visibility.private,
            "status": [tasks.keys.status.completed, tasks.keys.status.failed],
        }

        return params
                


class TaskDetailQuerySet(records.ChildrenQuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskDeadlineQuerySet(records.ChildrenQuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskStatusQuerySet(records.ChildrenQuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])

class TaskVisibilityQuerySet(records.ChildrenQuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskWatacherQuerySet(records.ChildrenQuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskAssignmentQuerySet(records.ChildrenQuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])

