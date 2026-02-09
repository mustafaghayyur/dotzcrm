

class Delete:
    """
        Static CLass
        Handles deleting operations in CRUD
    """
    
    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, masterId, rlc = False):
        self.log(None, f'ENTERING delete for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[self.mapper.master('foreignKeyName')] = masterId
        if not rlc:
            fieldsF['latest'] = self.mapper.values.latest('latest')
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        if not rlc:
            fieldsU['latest'] = self.mapper.values.latest('archive')

        designation = '[RLC]' if rlc else ''

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}] | {designation}')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    
    @staticmethod
    def masterTable(state, mapper, modelClass, tbl, tableName, columnsList, masterId):
        self.log(None, f'ENTERING delete for MT [{tbl}]')
        fieldsU = {}
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']

        self.log({'id': masterId, 'update': fieldsU}, f'ID for deletion find | Fields for deletion update [{tbl}]')        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    
    @staticmethod
    def childTableById(self, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteById()
            For RLC type nodes only
        """
        self.log(None, f'ENTERING deleteById for CT [{self.tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{self.tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
    
    @staticmethod
    def allM2Ms(self, modelClass, tbl, tableName, columnsList, firstColId):
        """
            Helper function for deleteAllForFirstCol(). M2M nodes only.
        """
        self.log(None, f'ENTERING deleteAllForFirstCol for CT [{self.tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[self.firstCol] = firstColId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.mapper.values.latest('archive')

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{self.tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
