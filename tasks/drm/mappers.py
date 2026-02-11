from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers
from .mapper_values import ValuesMapper

class TasksMapper(RelationshipMappers):
    """
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """
    def startUpCode(self):
        """
            Used to insert operations in __init__()
        """
        # tables belonging to this mapper
        tables = ['tata', 'tade', 'tadl', 'tast', 'tavi', 'taas', 'taco', 'tawa']
        self.state.set('mapperTables', tables)

        self.setValuesMapper(ValuesMapper)
    
    def _master(self):
        return {
            'table': 'tasks_task',
            'abbreviation': 'tata',
            'foreignKeyName': 'task_id',
        }

    def _commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in CRUD.update() operation.
        """
        return {
            'tata': ['id'],
            'tade': ['id', 'latest', 'task_id'],
            'tadl': ['id', 'latest', 'task_id'],
            'tast': ['id', 'latest', 'task_id'],
            'tavi': ['id', 'latest', 'task_id'],
            'taas': ['id', 'latest', 'task_id'],
            'tawa': ['id', 'latest'],
            'taco': ['id'], # @todo: confirm ids should be ignored on rlc & m2ms
        }
    
    def _ignoreOnCreate(self):
        return {
            'tata': ['delete_time', 'create_time', 'update_time', 'id'],
            'tade': ['delete_time', 'create_time', 'latest', 'id'],
            'tadl': ['delete_time', 'create_time', 'latest', 'id'],
            'tast': ['delete_time', 'create_time', 'latest', 'id'],
            'tavi': ['delete_time', 'create_time', 'latest', 'id'],
            'taas': ['delete_time', 'create_time', 'latest', 'id'],
            'tawa': ['delete_time', 'create_time', 'latest', 'id'],
            'taco': ['delete_time', 'create_time', 'update_time', 'id'],
        }

    def _m2mFields(self):
        """
            Define first and second fields for M2M tables.
        """
        return {
            'tawa': {
                'firstCol': 'task_id',
                'secondCol': 'watcher_id',
                'tables': ['tata', 'usus']
            },
        }
    
    def _dateFields(self):
        """
            Add all columns found in this mapper, that are date fields.
        """
        return ['create_time', 'update_time', 'delete_time', 'deadline']
    
    def _serializers(self):
        """
            returns serializers relevent to mapper
        """
        return {
            'default': {
                'path': 'tasks.validators.tasks',
                'generic': 'TaskO2ORecordSerializerGeneric',
                'lax': 'TaskO2ORecordSerializerLax',
                'strict': 'TaskO2ORecordSerializerStrict',
            },
            'taco': {
                'path': 'tasks.validators.comments',
                'generic': 'CommentSerializerGeneric',
                'lax': 'CommentSerializerLax',
                'strict': 'CommentSerializerStrict',
            },
            'tawa': {
                'path': 'tasks.validators.watchers',
                'generic': 'WatcherSerializerGeneric',
                'lax': 'WatcherSerializerLax',
                'strict': 'WatcherSerializerStrict',
            },
        }
    
    def _crudClasses(self):
        """
            returns CRUD classes relevent to mapper
        """
        return {
            'default': {
                'path': 'tasks.drm.crud',
                'name': 'Tasks',
            },
            'taco': {
                'path': 'tasks.drm.crud',
                'name': 'Comments',
            },
            'tawa': {
                'path': 'tasks.drm.crud',
                'name': 'Watchers',
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
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """
    def startUpCode(self):
        """
            Used to insert operations in __init__()
        """
        # tables belonging to this mapper
        tables = ['wowo', 'wode', 'wous', 'wota']
        self.state.set('mapperTables', tables)
        
    
    def _master(self):
        return {
            'table': 'users_department',
            'abbreviation': 'wowo',
            'foreignKeyName': 'workspace_id',
        }

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
    
    def _ignoreOnCreate(self):
        return {
            'wowo': ['delete_time', 'create_time', 'update_time', 'id'],
            'wode': ['delete_time', 'create_time', 'latest', 'id'],
            'wous': ['delete_time', 'create_time', 'latest', 'id'],
            'wota': ['delete_time', 'create_time', 'latest', 'id'],
        }

    def _m2mFields(self):
        """
            Define first and second fields for M2M tables.
        """
        return {
            'wode': {
                'firstCol': 'workspace_id',
                'secondCol': 'department_id',
                'tables': ['wowo', 'dede']
            },
            'wous': {
                'firstCol': 'workspace_id',
                'secondCol': 'user_id',
                'tables': ['wowo', 'usus']
            },
            'wota': {
                'firstCol': 'workspace_id',
                'secondCol': 'task_id',
                'tables': ['wowo', 'tata']
            },
        }
    
    def _dateFields(self):
        """
            Add all columns found in this mapper, that are date fields.
        """
        return ['create_time', 'update_time', 'delete_time']

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

