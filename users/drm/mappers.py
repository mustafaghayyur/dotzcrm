from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers
from .mapper_values import ValuesMapper

class UsersMapper(RelationshipMappers):
    """
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """
    def startUpCode(self):
        """
            Used to insert operations in __init__()
        """
        # tables belonging to this mapper
        tables = ['usus', 'uspr', 'usre', 'usse', 'used']
        self.state.set('mapperTables', tables)
        
        self.setValuesMapper(ValuesMapper)

    def _master(self):
        return {
            'table': 'auth_user',
            'abbreviation': 'usus',
            'foreignKeyName': 'user_id',
        }

    def _commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately. Master().foreignKeyName is not included.
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Carries any fields within a table to ignore in CRUD.update() operations.
            Master().foreignKeyName is NOT included.
        """
        return {
            'usus': ['id'],
            'uspr': ['id', 'latest'],
            'usre': ['id', 'latest'],
            'usse': ['id'],
            'used': ['id'],
        }
    
    def _ignoreOnCreate(self):
        """
            Sets fields we can ignore in crud.create() proceses.
            Master().foreignKeyName is NOT included.
        """
        return {
            'usus': ['delete_time', 'create_time', 'update_time', 'id'],
            'uspr': ['delete_time', 'create_time', 'latest', 'id'],
            'usre': ['delete_time', 'create_time', 'latest', 'id'],
            'usse': ['delete_time', 'create_time', 'update_time', 'id'],
            'used': ['delete_time', 'create_time', 'update_time', 'id'],
        }
    
    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'usre': {
                'firstCol': 'reporter_id',
                'secondCol': 'reportsTo_id',
                'tables': ['usus']
            },
        }
    
    def _dateFields(self):
        """
            Add all columns found in this mapper, that are date fields.
        """
        return ['create_time', 'update_time', 'delete_time', 'date_joined']

    
    def _bannedFromInput(self):
        """
            Carries Mapper fields that cannot take user input directly.
            Need special handling while carrying out C.U.(D.) operations
        """
        return ['reporter_id', 'reportsTo_id', 'owner_id', 'log_user_id']
    
    def _bannedFromOpenAccess(self):
        """
            Carries dictionary of definitions on which CRUD operations are permitted
            on the universal API nodes (restapi.views.list|crud).
        """
        return {
            'read': {
                'usus': ['password', 'last_login', 'is_superuser', 'is_staff', 'date_joined'],
                'usse': ['settings'],
                'used': ['change_log']
            }
        }

    def _defaults_order_by(self):
        return [
            {
                'tbl': 'usus',
                'col': 'update_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'uspr',
                'col': 'create_time',
                'sort': 'DESC',
            }
        ]

    def _defaults_where_conditions(self):
        return {
            "latest": self.values.latest('latest'),
            "usus_delete_time": 'IS NULL'
        }
    
    def _defaults_limit_value(self):
        """
            Should be returned in string format.
        """
        return '20'




class DepartmentsMapper(RelationshipMappers):
    """
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """
    def startUpCode(self):
        """
            Used to insert operations in __init__()
        """
        # tables belonging to this mapper
        tables = ['dede', 'dehe', 'deus']
        self.state.set('mapperTables', tables)
        

    def _master(self):
        return {
            'table': 'users_department',
            'abbreviation': 'dede',
            'foreignKeyName': 'department_id',
        }


    def _commonFields(self):
        """
            These keys tend to be found in every table and cause problems 
            if not handled separately. Master().foreignKeyName is not included.
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'dede': ['id', 'latest'],
            'dehe': ['id', 'latest'],
            'deus': ['id', 'latest'],
        }
    
    def _ignoreOnCreate(self):
        """
            Sets fields we can ignore in crud.create() proceses.
            Master().foreignKeyName is NOT included.
        """
        return {
            'dede': ['delete_time', 'create_time', 'update_time', 'id'],
            'dehe': ['delete_time', 'create_time', 'latest', 'id'],
            'deus': ['delete_time', 'create_time', 'latest', 'id'],
        }

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'dehe': {
                'firstCol': 'department_id',
                'secondCol': 'head_id',
                'tables': ['dede', 'usus']
            },
            'deus': {
                'firstCol': 'department_id',
                'secondCol': 'user_id',
                'tables': ['dede', 'usus']
            },
        }
    
    def _dateFields(self):
        """
            Add all columns found in this mapper, that are date fields.
        """
        return ['create_time', 'update_time', 'delete_time']
    
    def _bannedFromInput(self):
        """
            Carries Mapper fields that cannot take user input directly.
            Need special handling while carrying out C.U.(D.) operations
        """
        return ['creator_id', 'user_id', 'head_id']

    def _defaults_order_by(self):
        return [
            {
                'tbl': 'dede',
                'col': 'update_time',
                'sort': 'DESC',
            },
        ]

    def _defaults_where_conditions(self):
        return {
            # "latest": self.values.latest('latest'),
            "dede_delete_time": 'IS NULL'
        }
    
    def _defaults_limit_value(self):
        """
            Should be returned in string format.
        """
        return '20'
