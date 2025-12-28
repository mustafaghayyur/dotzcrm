from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers
from core.DRMcore.mappers.ValuesMapper import ValuesMapperGeneric

class TasksMapper(RelationshipMappers):
    """
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """

    def __init__(self, VMClassInstance):
        super().__init__(VMClassInstance)

    def _tables(self):
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

    def _models(self):
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

    def _master(self):
        return {
            'table': 'tasks_task',
            'abbreviation': 't',
            'foreignKeyName': 'task_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['t', 'd', 'l', 's', 'v', 'a']
            case 'm2m':
                return ['w']
            case 'rlc':
                return ['c']
            case 'm2o':
                return []
            case _:
                return []

    def _commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately

            Note: 'latest' is intentionally excluded.
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'tasks_task': ['id'],
            'tasks_details': ['id', 'latest', 'task_id'],
            'tasks_deadline': ['id', 'latest', 'task_id'],
            'tasks_status': ['id', 'latest', 'task_id'],
            'tasks_visibility': ['id', 'latest', 'task_id'],
            'tasks_assignment': ['id', 'latest', 'task_id'],
            'tasks_watcher': ['id', 'latest', 'task_id'],
            'tasks_comment': ['id', 'task_id'],
        }

    def _ignoreOnRetrieval(self):
        return ['task_id']

    def _tableFields(self):
        """
            Outline all tables within Tasks system here
        """
        return {
            'tasks_task': ['id', 'description', 'create_time', 'update_time', 'delete_time', 'creator_id', 'parent_id'],
            'tasks_details': ['id', 'details', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_deadline': ['id', 'deadline', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_status': ['id', 'status', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_visibility': ['id', 'visibility', 'latest', 'create_time', 'delete_time', 'task_id'],
            'tasks_assignment': ['id', 'latest', 'create_time', 'delete_time', 'assignee_id', 'assignor_id', 'task_id'],
            'tasks_watcher': ['id', 'latest', 'create_time', 'delete_time', 'task_id', 'watcher_id'],
            'tasks_comment': ['id', 'comment', 'parent_id', 'create_time', 'update_time', 'delete_time', 'task_id']
        }

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'w': {
                'firstCol': 'task_id',
                'secondCol': 'watcher_id',
            },
        }

    def _defaults_order_by(self):
        return [
            {
                'tbl': 't',
                'col': 'update_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'd',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'l',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 's',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'v',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'a',
                'col': 'create_time',
                'sort': 'DESC',
            },
        ]

    def _defaults_where_conditions(self):
        return {
            "latest": self.values.latest('latest'),
            # "tdelete_time": 'IS NULL',  # @todo needs to be handled
        }
    
    def _defaults_limit_value(self):
        """
            Should be returned in string format.
        """
        return '20'


class ValuesMapper(ValuesMapperGeneric):
    """
        This class will help manage value expectations for certain enum fields.
        Enums will be managed in the application layer.
    """
    
    def latest(self, key = 'all'):
        values = {
            'archive': 2,
            'latest': 1,
        }
        
        if key is not None and key in values:
            return values[key]

        return values

    def status(self, key = 'all'):
        values = {
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

        if key is not None and key in values:
            return values[key]

        return values

    def visibility(self, key = 'all'):
        values = {
            'private': 'private',
            'assigned': 'assigned',
            'organization': 'organization',
            'stakeholders': 'stakeholders',
        }

        if key is not None and key in values:
            return values[key]

        return values
