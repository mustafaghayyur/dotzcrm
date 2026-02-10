from django.utils import timezone

class Delete:
    """
        Static CLass
        Handles deleting operations in CRUD
    """
    
    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, masterId, rlc = False):
        """
            Marks all child table records, for specified CT, as deleted, where MT id matches.
            For O2O & RLC records.
        
            :param state: State() instance
            :param mapper: Mapper() instance
            :param modelClass: table's Model class reference
            :param tbl: [str] table key/identifier
            :param tableName: [str] table full name
            :param columnsList: [list] columns of specified table
            :param masterId: [int] id to mark as deleted
            :param rlc: [bool] signifies wheather record is RLC type
        """
        state.get('log').record(None, f'ENTERING delete for CT [{tableName}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[mapper.master('foreignKeyName')] = masterId
        if not rlc:
            fieldsF['latest'] = mapper.values.latest('latest')
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        if not rlc:
            fieldsU['latest'] = mapper.values.latest('archive')

        designation = '[RLC]' if rlc else ''

        state.get('log').record({'find': fieldsF, 'update': fieldsU}, f'Attempted delete.childTable() for [{tableName}]. Fields for deletion find | Fields for deletion update [{tableName}] | {designation}')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    
    @staticmethod
    def masterTable(state, mapper, modelClass, tbl, tableName, columnsList, masterId):
        """
            Marks all master-table record as deleted, where MT id matches.

            :param state: State() instance
            :param mapper: Mapper() instance
            :param modelClass: table's Model class reference
            :param tbl: [str] table key/identifier
            :param tableName: [str] table full name
            :param columnsList: [list] columns of specified table
            :param masterId: [int] id to mark as deleted
        """
        state.get('log').record(None, f'ENTERING delete for MT [{tableName}]')
        fieldsU = {}
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']

        state.get('log').record({'id': masterId, 'update': fieldsU}, f'Attempted delete.masterTable() for [{tableName}]. ID for deletion find | Fields for deletion update.')        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    
    @staticmethod
    def childTableById(state, mapper, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteById()
            For RLC type nodes only
        
            :param state: State() instance
            :param mapper: Mapper() instance
            :param modelClass: table's Model class reference
            :param tbl: [str] table key/identifier
            :param tableName: [str] table full name
            :param columnsList: [list] columns of specified table
            :param childId: [int] id of child to archive
        """
        state.get('log').record(None, f'ENTERING delete.childTableById() for CT [{tableName}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()

        state.get('log').record({'find': fieldsF, 'update': fieldsU}, f'Attempted delete.childTableById() [{tableName}]. Fields for deletion find | Fields for deletion update')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
    
    @staticmethod
    def allChildTableFirstCol(state, mapper, modelClass, tbl, tableName, columnsList, firstColId):
        """
            Archive all matching first-column. 
            M2M nodes only.
        
            :param state: State() instance
            :param mapper: Mapper() instance
            :param modelClass: table's Model class reference
            :param tbl: [str] table key/identifier
            :param tableName: [str] table full name
            :param columnsList: [list] columns of specified table
            :param firstColId: [int] first column - as defined in mapper
        """
        state.get('log').record(None, f'ENTERING delete.allChildTableFirstCol for CT [{tableName}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[state.get('firstCol')] = firstColId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = mapper.values.latest('archive')

        state.get('log').record({'find': fieldsF, 'update': fieldsU}, f'Atempted delete.allChildTableFirstCol() [{tableName}]. Fields for deletion find | Fields for deletion update')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)


    def allChildTableM2ms(state, mapper, modelClass, tbl, tableName, columnsList):
        """
            Archive any existing records matching both firstCol & secondCol
            M2M nodes only.
        
            :param state: State() instance
            :param mapper: Mapper() instance
            :param modelClass: table's Model class reference
            :param tbl: [str] table key/identifier
            :param tableName: [str] table full name
            :param columnsList: [list] columns of specified table
        """
        state.get('log').record(None, f'ENTERING delete.allChildTableM2ms() for childtable [{tableName}]')

        fieldsF = {}
        fieldsF[state.get('firstCol')] = state.get('submission')[state.get('firstCol')]
        fieldsF[state.get('secondCol')] = state.get('submission')[state.get('secondCol')]

        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = mapper.values.latest('archive')        

        modelClass.objects.filter(**fieldsF).update(**fieldsU)
        state.get('log').record({'fields': fieldsU}, f'Attempted delete.allChildTableM2ms() for: [{tableName}]')

    