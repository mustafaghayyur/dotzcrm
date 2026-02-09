from django.utils import timezone

class Delete:
    """
        Static CLass
        Handles deleting operations in CRUD
    """
    
    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, masterId, rlc = False):
        state.get('log').record(None, f'ENTERING delete for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[mapper.master('foreignKeyName')] = masterId
        if not rlc:
            fieldsF['latest'] = mapper.values.latest('latest')
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        if not rlc:
            fieldsU['latest'] = mapper.values.latest('archive')

        designation = '[RLC]' if rlc else ''

        state.get('log').record({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}] | {designation}')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    
    @staticmethod
    def masterTable(state, mapper, modelClass, tbl, tableName, columnsList, masterId):
        state.get('log').record(None, f'ENTERING delete for MT [{tbl}]')
        fieldsU = {}
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']

        state.get('log').record({'id': masterId, 'update': fieldsU}, f'ID for deletion find | Fields for deletion update [{tbl}]')        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    
    @staticmethod
    def childTableById(state, mapper, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteById()
            For RLC type nodes only
        """
        state.get('log').record(None, f'ENTERING deleteById for CT [{state.get('tbl')}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()

        state.get('log').record({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{state.get('tbl')}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
    
    @staticmethod
    def allChildTableFirstCol(state, mapper, modelClass, tbl, tableName, columnsList, firstColId):
        """
            Archive all matching first-column. 
            M2M nodes only.
        """
        state.get('log').record(None, f'ENTERING deleteAllForFirstCol for CT [{state.get('tbl')}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[state.get('firstCol')] = firstColId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = mapper.values.latest('archive')

        state.get('log').record({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{state.get('tbl')}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)


    def allChildTableM2ms(state, mapper, modelClass, tbl, tableName, columnsList):
        """
            Archive any existing records matching both firstCol & secondCol
            M2M nodes only.
        """
        state.get('log').record(None, f'ENTERING update for childtable [{tbl}]')

        fieldsF = {}
        fieldsF[state.get('firstCol')] = state.get('submission')[state.get('firstCol')]
        fieldsF[state.get('secondCol')] = state.get('submission')[state.get('secondCol')]

        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = mapper.values.latest('archive')        

        modelClass.objects.filter(**fieldsF).update(**fieldsU)
        state.get('log').record({'fields': fieldsU}, f'Attempted update For: [{tbl}]')

    