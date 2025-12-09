from . import RelationshipMappers

class TasksMapper():
    def __init__(self):
        pass

    def tables(self):
        """
            These keys (table-abbreviations) will be used throughout code.
            Change with care.
        """
        return {
            't': 'tasks_task',
            'd': 'tasks_details',
            'l': 'tasks_deadline',
            's': 'tasks_status',
            'v': 'tasks_visibility',
            'a': 'tasks_assignment',
            'w': 'tasks_watcher',
            'c': 'tasks_comment',
        }

    def models(self):
        """
            These keys (table-abbreviations) will be used throughout code.
            Change with care.
        """
        return {
            't': 'Task',
            'd': 'Details',
            'l': 'Deadline',
            's': 'Status',
            'v': 'Visibility',
            'a': 'Assignment',
            'w': 'Watcher',
            'c': 'Comment',
        }

    def master(self, key = 'all'):
        info = {
            'table': 'tasks_task',
            'abbreviation': 't',
            'foreignKeyName': 'task_id',
        }

        if key is not None and key in info:
            return info[key]

        return info

    def tablesForRelationType(self, relationType = 'o2o'):
        match relationType:
            case 'o2o':
                return ['d', 'l', 's', 'v', 'a']
            case 'm2m':
                return ['w']
            case 'rlc':
                return ['c']
            case 'm2o':
                return []
            case _:
                return []

    def commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately

            Note: 'latest' is intentionally excluded.
        """
        return ['id', 'create_time', 'update_time', 'delete_time']

    def ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'tasks_task': [],
            'tasks_details': ['id', 'latest', 'task_id'],
            'tasks_deadline': ['id', 'latest', 'task_id'],
            'tasks_status': ['id', 'latest', 'task_id'],
            'tasks_visibility': ['id', 'latest', 'task_id'],
            'tasks_assignment': ['id', 'latest', 'task_id'],
            'tasks_watcher': ['id', 'latest', 'task_id'],
            'tasks_comment': ['id', 'task_id'],
        }

    def ignoreOnRetrieval(self):
        return ['task_id']

    def tableFields(self, name = None):
        """
            Outline all tables within Tasks system here
        """
        tables = {
            'tasks_task': ['id', 'description', 'create_time', 'update_time', 'delete_time', 'creator_id', 'parent_id'],
            'tasks_details': ['id', 'details', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_deadline': ['id', 'deadline', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_status': ['id', 'status', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_visibility': ['id', 'visibility', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_assignment': ['id', 'latest', 'create_time', 'delete_time', 'assignee_id', 'assignor_id', 'task_id'],
            'tasks_watcher': ['id', 'latest', 'create_time', 'delete_time', 'task_id', 'watcher_id'],
            'tasks_comment': ['id', 'comment', 'parent_id', 'create_time', 'update_time', 'delete_time', 'task_id']
        }

        if name is not None and name in tables:
            return table[name]

        return tables


class ValuesManager():
    """
    This class will help manage value expectations for certain enum fields.
    Enums will be managed in the application layer.
    """

    def latest(self):
        return {
            'archive': 2,
            'latest': 1,
        }

    def status(self):
        return {
            'assigned': 'assigned',
            'viewed': 'viewed',
            'queued': 'queued',
            'started': 'started',
            'onhold': 'onhold',
            'abandoned': 'abandoned',
            'reassigned': 'reassigned',
            'awaitingfeedback': 'awaitingfeedback',
            'completed': 'completed',
            'failed': 'failed',
        }

    def visibility(self):
        return {
            'private': 'private',
            'assigned': 'assigned',
            'organization': 'organization',
            'stakeholders': 'stakeholders',
        }
