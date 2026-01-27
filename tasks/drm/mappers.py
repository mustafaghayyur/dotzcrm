from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers

class TasksMapper(RelationshipMappers):
    tablesList = ['tata', 'tade', 'tadl', 'tast', 'tavi', 'taas', 'taco', 'tawa']

    def __init__(self, VMClassInstance = None):
        super().__init__(VMClassInstance)
    
    def _master(self):
        return {
            'table': 'tasks_task',
            'abbreviation': 'tata',
            'foreignKeyName': 'task_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['tata', 'tade', 'tadl', 'tast', 'tavi', 'taas']
            case 'm2m':
                return ['tawa']
            case 'rlc':
                return ['taco']
            case 'm2o':
                return []
            case _:
                return []

    def _commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately
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

    def _m2mFields(self):
        """
            Define first and second fields for M2M tables.
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
                'tbl': 'tata',
                'col': 'update_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'tade',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'tadl',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'tast',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'tavi',
                'col': 'create_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'taas',
                'col': 'create_time',
                'sort': 'DESC',
            },
        ]

    def _defaults_where_conditions(self):
        return {
            "latest": self.values.latest('latest'), # left without table prefix for reasons.
            "tata_delete_time": 'IS NULL',  # @todo needs to be handled
        }
    
    def _defaults_limit_value(self):
        """
            Should be returned in string format.
        """
        return '20'



class WorkSpacesMapper(RelationshipMappers):
    """
        Maps all tables relating to WorkSpaces
    """
    tablesList = ['wowo', 'wode', 'wous', 'wota']

    def __init__(self, VMClassInstance = None):
        super().__init__(VMClassInstance)
    
    def _master(self):
        return {
            'table': 'users_department',
            'abbreviation': 'wowo',
            'foreignKeyName': 'workspace_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['wowo']
            case 'm2m':
                return ['wode', 'wous', 'wota']
            case 'rlc':
                return []
            case 'm2o':
                return []
            case _:
                return []

    def _commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'wowo': ['id'],
            'wode': ['id', 'latest', 'workspace_id'],
            'wous': ['id', 'latest', 'workspace_id'],
            'wota': ['id', 'latest', 'workspace_id'],
        }

    def _ignoreOnRetrieval(self):
        return []

    def _m2mFields(self):
        """
            Define first and second fields for M2M tables.
        """
        return {
            'wode': {
                'firstCol': 'workspace_id',
                'secondCol': 'department_id',
            },
            'wous': {
                'firstCol': 'workspace_id',
                'secondCol': 'user_id',
            },
            'wota': {
                'firstCol': 'workspace_id',
                'secondCol': 'task_id',
            },
        }

    def _defaults_order_by(self):
        return [
            {
                'tbl': 'wowo',
                'col': 'update_time',
                'sort': 'DESC',
            }
        ]

    def _defaults_where_conditions(self):
        return {
            "latest": self.values.latest('latest'), # left without table prefix for reasons.
            "wowo_delete_time": 'IS NULL',  # @todo needs to be handled
        }
    
    def _defaults_limit_value(self):
        """
            Should be returned in string format.
        """
        return '20'

