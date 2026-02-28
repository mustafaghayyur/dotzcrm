from core.DRMcore.mappers.RelationshipMappers import RelationshipMappers

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
    
    
    def _serializers(self):
        """
            returns serializers relevent to mapper
            @todo fill in
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
            @todo fill in
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
    
    def _currentUserFieldsCrud(self):
        """
            Returns list of fields which hold current user's id.
            Should allow limiting of external entries in these fields.
        """
        return ['creator_id', 'user_id', 'head_id']
    
    def _currentUserFieldsRead(self):
        """
            Only where condition in read queries are impacted
        """
        return []
    
    def _bannedFromOpenAccess(self):
        """
            Carries dictionary of rules on which CRUD operations are permitted
            on the universal API nodes (restapi.views.list|crud).
        """
        return None

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
