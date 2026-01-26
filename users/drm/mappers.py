from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers

class UsersMapper(RelationshipMappers):
    """
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """

    def __init__(self, VMClassInstance = None):
        super().__init__(VMClassInstance)

    def _tables(self):
        """
            These keys (table-abbreviations) will be used throughout code.
            Change with care.
        """
        return {
            'u': 'auth_user',
            'p': 'users_userprofile',
            'r': 'users_userreportsto',
            's': 'users_usersettings',
        }

    def _models(self):
        """
            These keys (table-abbreviations) will be used throughout code.
            Change with care.
        """
        return {
            'u': 'User',
            'p': 'UserProfile',
            's': 'UserSettings',
            'r': 'UserReportsTo',
        }

    def _modelPaths(self):
        return {
            'u': 'users.models',
            'p': 'users.models',
            's': 'users.models',
            'r': 'users.models',
        }

    def _master(self):
        return {
            'table': 'auth_user',
            'abbreviation': 'u',
            'foreignKeyName': 'user_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['u', 'p', 's']
            case 'm2m':
                return ['r']
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

            Note: 'latest' is intentionally excluded.
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'auth_user': ['id'],
            'users_userprofile': ['id', 'latest'],
            'users_userreportsto': ['id', 'latest'],
            'users_usersettings': ['id', 'latest'],
        }

    def _ignoreOnRetrieval(self):
        return []

    def _tableFields(self):
        """
            Outline all tables within Tasks system here
        """
        return {
            'auth_user': ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'create_time', 'delete_time', 'update_time', 'user_level'],
            'users_userprofile': ['id', 'legal_first_name', 'legal_last_name', 'office_phone', 'office_ext', 'cell_phone', 'home_phone', 'office_location', 'create_time', 'update_time', 'delete_time', 'user_id'],
            'users_userreportsto': ['id', 'create_time', 'delete_time', 'reports_to_id', 'user_id'],
            'users_usersettings': ['id', 'settings', 'create_time', 'update_time', 'delete_time', 'user_id'],
        }

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'r': {
                'firstCol': 'reports_to_id',
                'secondCol': 'user_id',
            },
        }

    def _defaults_order_by(self):
        return [
            {
                'tbl': 'u',
                'col': 'update_time',
                'sort': 'DESC',
            },
            {
                'tbl': 'p',
                'col': 'update_time',
                'sort': 'DESC',
            },
            {
                'tbl': 's',
                'col': 'update_time',
                'sort': 'DESC',
            }
        ]

    def _defaults_where_conditions(self):
        return {
            # "latest": self.values.latest('latest'),
            # "tdelete_time": 'IS NULL'
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

    def __init__(self, VMClassInstance = None):
        super().__init__(VMClassInstance)

    def _tables(self):
        """
            These keys (table-abbreviations) will be used throughout code.
            Change with care.
        """
        return {
            'd': 'users_department',
            'h': 'users_departmenthead',
            't': 'users_usertodepartment',
        }

    def _models(self):
        """
            These keys (table-abbreviations) will be used throughout code.
            Change with care.
        """
        return {
            'd': 'Department',
            'h': 'DepartmentHead',
            't': 'UserToDepartment',
        }

    def _modelPaths(self):
        return {
            'd': 'users.models',
            'h': 'users.models',
            't': 'users.models',
        }

    def _master(self):
        return {
            'table': 'users_department',
            'abbreviation': 'd',
            'foreignKeyName': 'department_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['d']
            case 'm2m':
                return ['h', 't']
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

            Note: 'latest' is intentionally excluded.
        """
        return ['id', 'create_time', 'update_time', 'delete_time', 'latest']

    def _ignoreOnUpdates(self):
        """
            Can carry any fields within a table to ignore in a certain operation
        """
        return {
            'users_department': ['id', 'latest'],
            'users_departmenthead': ['id', 'latest'],
            'users_userreportsto': ['id', 'latest'],
            'users_usertodepartment': ['id', 'latest'],
        }

    def _ignoreOnRetrieval(self):
        return [] # @todo: inspect this for users and depts mappers

    def _tableFields(self):
        """
            Outline all tables within Tasks system here
        """
        return {
            'users_department': ['id', 'name', 'description', 'create_time', 'update_time', 'delete_time', 'parent_id'],
            'users_departmenthead': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
            'users_usertodepartment': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
        }

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'h': {
                'firstCol': 'department_id',
                'secondCol': 'user_id',
            },
            't': {
                'firstCol': 'department_id',
                'secondCol': 'user_id',
            },
        }

    def _defaults_order_by(self):
        return [
            {
                'tbl': 'd',
                'col': 'update_time',
                'sort': 'DESC',
            },
        ]

    def _defaults_where_conditions(self):
        return {
            # "latest": self.values.latest('latest'),
            # "tdelete_time": 'IS NULL'
        }
    
    def _defaults_limit_value(self):
        """
            Should be returned in string format.
        """
        return '20'
