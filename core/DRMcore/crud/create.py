
class Create:
    """
        Static class
        Handles all create operations for CRUD
    """

    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, rlc = False):
        self.log(None, f'Entering create operation for childtable: [{tbl}]')
        
        fields = {}
        for col in columnsList:
            if self.mapper.isCommonField(col):
                key = tbl + col  # add on a prefix to match self.submission keys
            else:
                key = col

            if key in self.submission:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    if isinstance(self.submission[key], object):
                        if hasattr(self.submission[key], 'id'):
                            self.submission[key] = self.submission[key].id  # must be a foreignkey Model instance, grab only the id.
                    
                    fields[col] = self.submission[key]
                    self.log([key, self.submission[key]], 'Field added')

        if len(fields) <= 1:  # if record is empty, abort insertion...
            if self.mapper.master('foreignKeyName') in fields:
                return None  # only the master ID is added, no need need to insert

        fields['create_time'] = timezone.now()
        if rlc:
            fields['update_time'] = fields['create_time']
        else:
            fields['latest'] = 1

        record = modelClass(**fields)
        record.save()
        designation = '[RLC]' if rlc else ''
        self.log({'fields': fields}, f'Create For: [{tbl}] | {designation}')
        return record


    @staticmethod
    def masterTable(state, mapper, tbl, modelClass, rlc = False):
        self.log(None, f'Entering create operation for MT: [{tbl}]')
        
        t = crud.generateModelInfo(self.mapper, tbl)
        fields = {}

        for col in t['cols']:
            # get the correct key reference for column in self.submission...
            if self.mapper.isCommonField(col):
                key = tbl + col  # add on a prefix to match self.submission keys
            else:
                key = col

            if key in self.submission:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    if isinstance(self.submission[key], object):
                        if hasattr(self.submission[key], 'id'):
                            self.submission[key] = self.submission[key].id  # must be a foreignkey Model instance, grab only the id.
                    
                    fields[col] = self.submission[key]
                    self.log(key, self.submission[key], 'Field added')

        if len(fields) == 0:  # if fields is empty, abort insertion...
            return None

        fields['creator_id'] = Create.generateCreatorId()
        fields['create_time'] = timezone.now()
        fields['update_time'] = fields['create_time']

        record = modelClass(**fields)
        record.save()
        self.log({'fields': fields}, f'Create For: [{tbl}]')
        return record
    

    @staticmethod
    def generateCreatorId(state,  mapper):
        if 'assignor_id' in self.submission:
            if self.submission['assignor_id'] is not None:

                if strings.isPrimitiveType(self.submission['assignor_id']):
                    return self.submission['assignor_id']
                if hasattr(self.submission['assignor_id'], 'id'):
                    return self.submission['assignor_id'].id
                
        return None