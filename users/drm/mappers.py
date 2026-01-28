from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers

class UsersMapper(RelationshipMappers):
    """
        All calls should be made to following method names without the '_' prefix.
        RelationshipMappers() has proper wrapper functions.
    """
    def startUpCode(self):
        tables = ['usus', 'uspr', 'usre', 'usse', 'used']
        additions = self.addTables(tables)

        self.state.set('tablesUsed', additions)

    def _master(self):
        return {
            'table': 'auth_user',
            'abbreviation': 'usus',
            'foreignKeyName': 'user_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['usus', 'uspr']
            case 'm2m':
                return ['usre']
            case 'rlc':
                return ['usse', 'used']
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
            'usus': ['id'],
            'uspr': ['id', 'latest', 'user_id'],
        }

    def _ignoreOnRetrieval(self):
        return []

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'usre': {
                'firstCol': 'reports_to_id',
                'secondCol': 'user_id',
            },
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
                'col': 'update_time',
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
    tablesList = ['dede', 'dehe', 'deus']

    def _master(self):
        return {
            'table': 'users_department',
            'abbreviation': 'dede',
            'foreignKeyName': 'department_id',
        }

    def _tablesForRelationType(self, relationType):
        match relationType:
            case 'o2o':
                return ['dede']
            case 'm2m':
                return ['dehe', 'deus']
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
            'users_department': ['id', 'latest', 'department_id'],  # @todo: confirm mt_fk_id should be in the ignore list in our crud logic
            'users_departmenthead': ['id', 'latest', 'department_id'],
            'users_userreportsto': ['id', 'latest', 'department_id'],
            'users_usertodepartment': ['id', 'latest', 'department_id'],
        }

    def _ignoreOnRetrieval(self):
        return [] # @todo: inspect this for users and depts mappers

    def _m2mFields(self):
        """
            Retrieves relational fields for specific M2M table.
        """
        return {
            'dehe': {
                'firstCol': 'department_id',
                'secondCol': 'user_id',
            },
            'deus': {
                'firstCol': 'department_id',
                'secondCol': 'user_id',
            },
        }

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
