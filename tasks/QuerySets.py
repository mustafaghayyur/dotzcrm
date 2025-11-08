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
    
    # Fetches full Task records with latest records (of sub tables).
    # Can be used on user's dashboard to fetch all recent private tasks
    # PARAMS:
    #  - user_id: the current user's ID
    #  - interval: string of integer value for how many days old tasks can be
    def user_tasks(self, user_id, keys = None):
        
        where_statements = []
        i = 0
        tbl = self.generateTablesList()

        for key, item in keys:
            where_statements[i] = self.validate(item, tbl[key], key)
            i += 1

        if keys is None:
            keys = self.generateDefaultKeys()
            #status = [settings.task.keys.status.completed, settings.task.keys.status.failed]

        qkeys = {
            "user_id": user_id,
            "visibility": visibility or settings.task.keys.visibility.private,
            "recent_interval": interval or settings.task.recent_interval,
            "status": status
            "archive": settings.task.keys.latest.archive,
        }

        new_labels = {

        }

        rq1 = """
            SELECT t.id, t.description, t.create_time, t.update_time, t.creator_id, t.parent_id
                d.description AS details,
                l.deadline, s.status, a.assignor_id
            FROM tasks_task AS t
                LEFT JOIN tasks_taskdetails AS d ON t.id = d.task_id
                LEFT JOIN tasks_taskdeadline AS l ON t.id = l.task_id
                LEFT JOIN tasks_taskstatus AS s ON t.id = s.task_id
                LEFT JOIN tasks_taskuserassignment AS a ON t.id = a.task_id
                LEFT JOIN tasks_taskvisibility AS v ON t.id = v.task_id
            WHERE a.assignee_id = %(user_id)s AND"""
                
        rq2 = """
                t.delete_time IS NULL AND (
                t.update_time >= NOW() - INTERVAL %(recent_interval)s DAY OR t.update_time IS NULL ) AND
                s.status IN (%(status)s) AND
               
                d.latest <> %(archive)s AND l.latest <> %(archive)s AND s.latest <> %(archive)s AND
                a.latest <> %(archive)s AND v.latest <> %(archive)s
            ;"""

        wheres = strings.concatenate(where_statements)
        query = strings.concatenate([rq1, wheres, rq2])
        log(query, 'REMEMBER MG: THE inputs CANNOT have quotes around them!!!!')

        return self.raw(query, qkeys, new_labels)

    def validate(self, item, tbl, key):
        if key == 'latest':
            return ''

        if isinstance(item, list):
            return tbl + '.' + key + ' IN (%(' + item + ')s)'
        
        if isinstance(item, str):
            return tbl + '.' + key + ' = %(' + item + ')s'

        return ''

    def generateTablesList(self):
        return {
            'id' = 't',
            'description' = 't',
            'create_time' = 't',
            'update_time' = 't',
            'delete_time' = 't',
            'creator_id' = 't',
            'parent_id' = 't',
            'details' = 'd',
            'deadline' = 'l',
            'status' = 's',
            'visibility' = 'v',
            'assignor_id' = 'a',
            'assignee_id' = 'a',
            'watcher_id' = 'w',
            'latest' = '',
        }

    def generateDefaultKeys(self):
        return {

        }


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

