
class Update:
    """
        Static class
        Handles all update operations for CRUD
    """

    @staticmethod
    def masterTable(state, mapper, mtModel, tableName, columnsList, completeRecord, rlc = False):
        self.log(None, f'ENTERING update for MT [{tableName}]')

        if not completeRecord.id or completeRecord.id is None:
            raise Exception(f'Something went wrong. Update record not found in system. {self.space}.CRUD.update()')

        fields = {}
        ignored = self.mapper.ignoreOnUpdates(self.mapper.master('abbreviation'))

        for col in columnsList:
            if col in ignored:
                continue  # ignore columns don't need a comparison in update operations

            if self.mapper.isCommonField(col):
                key = self.mapper.master('abbreviation') + col  # need tbl_abbrv prefix for comparison
            else:
                key = col

            if key in self.submission:
                self.submission[key] = Values.convertModelToId(getattr(completeRecord, col), self.submission[key])
                dbVal = Values.amendDatabaseValue(getattr(completeRecord, col), self.submission[key])
                
                self.log([key, col], 'comparing in MT Update')

                if self.submission[key] != dbVal:
                    fields[col] = self.submission[key]
                    self.log([key, self.submission[key], col, dbVal], 'MISMATCH')

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=completeRecord.id).update(**fields)
        self.log({'fields': fields}, f'Update For: [{tableName}]')
        return None

    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, completeRecord, rlc = False):
        self.log(None, f'ENTERING update for childtable [{tbl}]')

        if not hasattr(completeRecord, tbl + 'id') or getattr(completeRecord, tbl + 'id') is None:
            raise Exception(f'Something went wrong. Update record not found in system. {self.space}.CRUD.update()')

        updateRequired = False
        ignored = self.mapper.ignoreOnUpdates(tbl)
        rlcFields = {}  # fields for RLC update

        for col in columnsList:
            if col in ignored:
                continue  # ignore columns don't need a comparison in update operations

            if self.mapper.isCommonField(col):
                key = tbl + col  # need tbl-abbrv prefix for comparison
            else:
                key = col

            if key in self.submission:
                if isinstance(self.submission[key], models.Model):
                    self.submission[key] = Values.convertModelToId(self.submission[key])
                
                if col in self.mapper.dateFields():
                    dbVal = Values.amendDatabaseValue(getattr(completeRecord, col))
                else:
                    dbVal = getattr(completeRecord, col)

                self.log([key, col], 'comparing in CT Update')

                if self.submission[key] != dbVal:
                    self.log([key, self.submission[key], col, dbVal], f'MISMATCH -  update needed')
                    rlcFields[col] = dbVal
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:
            if rlc:
                rlcFields['update_time'] = timezone.now()
                modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**rlcFields)
                self.log({'fields': rlcFields}, f'Update For: [{tbl}] | [RLC]')
            else:
                fields = {}
                fields['delete_time'] = timezone.now()
                fields['latest'] = self.mapper.values.latest('archive')
                
                # update old record, create new one...
                modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
                self.log({'fields': fields}, f'Update For: [{tbl}]')
                self.createChildTable(modelClass, tbl, tableName, columnsList)

        return None



    def childTableM2M(self, modelClass, tbl, tableName, columnsList):
        """
            updateChildTable() will be overwritten in M2MChildren for special handling.
            We will simply archive any existing records matching firstCal & secondCol
        """
        self.log(None, f'ENTERING update for childtable [{tbl}]')

        fieldsF = {}
        fieldsF[self.firstCol] = self.submission[self.firstCol]
        fieldsF[self.secondCol] = self.submission[self.secondCol]

        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.mapper.values.latest('archive')        

        modelClass.objects.filter(**fieldsF).update(**fieldsU)
        self.log({'fields': fieldsU}, f'Attempted update For: [{tbl}]')

    