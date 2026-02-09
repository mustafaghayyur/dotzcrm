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
            if not handled separately
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Carries any fields within a table to ignore in CRUD.update() operations.
        """
        return {
            'usus': ['id'],
            'uspr': ['id', 'latest', 'user_id'],
            'usre': ['id', 'latest'],
            'usse': ['id'],
            'used': ['id'],
        }
    
    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'usre': {
                'firstCol': 'user_id',
                'secondCol': 'reports_to_id',
                'tables': ['usus']
            },
        }
    
    def _dateFields(self):
        """
            Add all columns found in this mapper, that are date fields.
        """
        return ['create_time', 'update_time', 'delete_time', 'date_joined']

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
            if not handled separately
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'dede': ['id', 'latest', 'department_id'],
            'dehe': ['id', 'latest', 'department_id'],
            'deus': ['id', 'latest', 'department_id'],
        }

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'dehe': {
                'firstCol': 'department_id',
                'secondCol': 'user_id',
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
