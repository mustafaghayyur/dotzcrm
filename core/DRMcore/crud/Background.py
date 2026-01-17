from django.utils import timezone
from . import Validation
from core import dotzSettings
from .staticHelpers import ValuesHandler
from core.helpers import crud, strings


"""
    This class holds the background crud operations.
    Primary focus: One-to-One relationship CRUD types
"""
class CrudOperations(Validation.ErrorHandling):
    space = None  # set in inheritor class
    module = None  # settings for 'app' or module in system (e.g. Tasks, Tickets, etc)
    submission = None  # will hold dictionary of submitted data by user


    def __init__(self):
        # loads configs related to the module (defined in self.space)
        self.module = getattr(dotzSettings, self.space)

        # holds all O2O primary keys for given space/module
        self.idCols = self.mapper.generateRelationTypeIds('o2o')
        self.rlcIdCols = self.mapper.generateRelationTypeIds('rlcIds')

        super().__init__()

    def saveSubmission(self, operation, submission):
        # First, we do some error checking on the dictionary supplied:
        self.dictValidation(self.space, operation, submission)
        
        if operation != 'create':
            # Second, we make sure the master-table-id is included in record:
            submission = self.mtIdValidation(operation, submission)
            
        # Finally, we save the submitted form into self.submission
        self.submission = submission

    def deleteChildTable(self, modelClass, tbl, tableName, columnsList, masterId, rlc = False):
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

    def deleteMasterTable(self, modelClass, tbl, tableName, columnsList, masterId):
        self.log(None, f'ENTERING delete for MT [{tbl}]')
        fieldsU = {}
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']

        self.log({'id': masterId, 'update': fieldsU}, f'ID for deletion find | Fields for deletion update [{tbl}]')        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    def updateMasterTable(self, mtModel, tableName, columnsList, completeRecord, rlc = False):
        self.log(None, f'ENTERING update for MT [{tableName}]')

        if not completeRecord.id or completeRecord.id is None:
            raise Exception(f'Something went wrong. Update record not found in system. {self.space}.CRUD.update()')

        fields = {}
        ignored = self.mapper.ignoreOnUpdates(tableName)

        for col in columnsList:
            if col in ignored:
                continue  # ignore columns don't need a comparison in update operations

            if self.mapper.isCommonField(col):
                key = self.mapper.master('abbreviation') + col  # need tbl_abbrv prefix for comparison
            else:
                key = col

            if key in self.submission:
                self.submission[key] = ValuesHandler.amendFormValue(getattr(completeRecord, col), self.submission[key])
                dbVal = ValuesHandler.amendDatabaseValue(getattr(completeRecord, col), self.submission[key])
                
                self.log([key, col], 'comparing in MT Update')

                if self.submission[key] != dbVal:
                    fields[col] = self.submission[key]
                    self.log([key, self.submission[key], col, dbVal], 'MISMATCH')

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=completeRecord.id).update(**fields)
        self.log({'fields': fields}, f'Update For: [{tableName}]')
        return None

    def updateChildTable(self, modelClass, tbl, tableName, columnsList, completeRecord, rlc = False):
        self.log(None, f'ENTERING update for childtable [{tbl}]')

        if not hasattr(completeRecord, tbl + 'id') or getattr(completeRecord, tbl + 'id') is None:
            raise Exception(f'Something went wrong. Update record not found in system. {self.space}.CRUD.update()')

        updateRequired = False
        ignored = self.mapper.ignoreOnUpdates(tableName)
        rlcFields = {}  # fields for RLC update

        for col in columnsList:
            if col in ignored:
                continue  # ignore columns don't need a comparison in update operations

            if self.mapper.isCommonField(col):
                key = tbl + col  # need tbl-abbrv prefix for comparison
            else:
                key = col

            if key in self.submission:
                self.submission[key] = ValuesHandler.amendFormValue(getattr(completeRecord, col), self.submission[key])
                dbVal = ValuesHandler.amendDatabaseValue(getattr(completeRecord, col), self.submission[key])
                
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

    def createChildTable(self, modelClass, tbl, tableName, columnsList, rlc = False):
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

    def createMasterTable(self, tbl, modelClass, rlc = False):
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

        fields['creator_id'] = self._generateCreatorId()
        fields['create_time'] = timezone.now()
        fields['update_time'] = fields['create_time']

        record = modelClass(**fields)
        record.save()
        self.log({'fields': fields}, f'Create For: [{tbl}]')
        return record

    def checkChildForMultipleLatests(self, modelClass, tbl, tableName, columnsList, fetchedRecords):
        """
            For given CT, see if fetched records have multiple entries 
            marked as 'latest' in the DB.
            @todo
        """
        pass

    def _generateCreatorId(self):
        if 'assignor_id' in self.submission:
            if self.submission['assignor_id'] is not None:

                if strings.isPrimitiveType(self.submission['assignor_id']):
                    return self.submission['assignor_id']
                if hasattr(self.submission['assignor_id'], 'id'):
                    return self.submission['assignor_id'].id
                
        return None

    