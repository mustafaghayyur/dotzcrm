from django.utils import timezone
from tasks.models import *
from core.helpers import crud
from core import settings
from .Validation import ErrorHandling

"""
    This class holds the background crud operations.
"""
class Background(ErrorHandling):
    currentUser = None  # FUTURE IMPLEMENTATION

    mtModel = None
    space = None
    module = None
    dbConfigs = None
    tables = None
    idCols = None

    submission = None


    def __init__(self):
        # loads configs related to the module (defined in self.space)
        self.module = getattr(settings, self.space)

        # loads configs for this module, more secifically related to the Database
        self.dbConfigs = settings.rdbms[self.space]

        # loads tables data needed for certain operations
        self.tables = settings.rdbms['tables']

        # holds all primary keys for given space/module
        self.idCols = self.dbConfigs['keys']['only_pk']

        super().__init__()

    def saveSubmission(self, operation, submission):
        # First, we do some error checking on the dictionary supplied:
        self.dictValidation(self.space, operation, submission)
        # Second, we make sure the master-table-id is included in record:
        submission = self.mtIdValidation(operation, submission)
        # Finally, we save the submitted form into self.submission
        self.submission = submission

    def deleteChildTable(self, modelClass, tbl, tableName, columnsList, masterId):
        fieldsF = {}  # fields to find records with
        fieldsF[self.dbConfigs['mtId']] = masterId
        fieldsF['latest'] = self.module['values']['latest']['latest']
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.module['values']['latest']['archive']
        
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    def deleteMasterTable(self, masterId):
        fieldsU = {}
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']
        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    def updateMasterTable(self, mtModel, tableName, columnsList, completeRecord):
        self.log(None, f'ENTERING update for MT [{self.dbConfigs['mtAbbrv']}]')
        
        fields = {}
        for col in columnsList:
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = self.dbConfigs['mtAbbrv'] + col  # need tbl_abbrv prefix for comparison
            else:
                key = col

            if key in self.submission:
                if self.submission[key] != getattr(completeRecord, col):
                    fields[col] = self.submission[key]
                    self.log([key, self.submission[key], col, getattr(completeRecord, col)], 'MISMATCH')
                self.log([key, col], 'comparing in MT Update')

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=self.submission[self.dbConfigs['mtAbbrv'] + 'id']).update(**fields)
        self.log({'fields': fields}, f'Update For: [{self.dbConfigs['mtAbbrv']}]')
        return None

    def updateChildTable(self, modelClass, tbl, tableName, columnsList, completeRecord):
        self.log(None, f'ENTERING update for childtable [{tbl}]')

        if not hasattr(completeRecord, tbl + 'id'):
            raise Exception(f'Something went wrong. Update record not found in system. {self.space}.CRUD.update()')

        updateRequired = False
        for col in columnsList:
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = tbl + col  # need tbl-abbrv prefix for comparison
            else:
                key = col

            if key in self.submission:
                if isinstance(self.submission[key], object):
                    if hasattr(self.submission[key], 'id'):
                        # need to overwrite dictionary key with int value for comparison
                        self.submission[key] = self.submission[key].id
                
                if col in self.dbConfigs['updates']['ignore'][tableName]:
                    continue  # ignore columns don't need a comparison in child-update operations

                if self.submission[key] != getattr(completeRecord, col):
                    self.log([key, self.submission[key], col, getattr(completeRecord, col)], f'MISMATCH -  update needed')
                    updateRequired = True  # changes found in dictionary record

                self.log([key, col], 'comparing in CT Update')

        if updateRequired:
            fields = {}
            fields['delete_time'] = timezone.now()
            fields['latest'] = self.module['values']['latest']['archive']
            
            # update old record, create new one...
            modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
            self.log({'fields': fields}, f'Update For: [{tbl}]')
            self.createChildTable(modelClass, tbl, tableName, columnsList)

        return None

    def createChildTable(self, modelClass, tbl, tableName, columnsList):
        self.log(None, f'Entering create operation for childtable: [{tbl}]')
        
        fields = {}
        for col in columnsList:
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
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
            if self.dbConfigs['mtId'] in fields:
                return None  # only the master ID is added, no need need to insert

        fields['create_time'] = timezone.now()
        fields['latest'] = 1
        record = modelClass(**fields)
        record.save()
        self.log({'fields': fields}, f'Create For: [{tbl}]')
        return record

    def createMasterTable(self, tbl, modelClass):
        self.log(None, f'Entering create operation for MasterTable: [{tbl}]')
        
        t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
        fields = {}

        for col in t['cols']:
            # get the correct key reference for column in self.submission...
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = tbl + col  # add on a prefix to match self.submission keys
            else:
                key = col

            if key in self.submission:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    fields[col] = self.submission[key]
                    self.log(key, self.submission[key], 'Field added')

        if len(fields) == 0:  # if fields is empty, abort insertion...
            return None

        fields['parent_id'] = self._generateParentId(self.submission)
        assignor = self.submission['assignor_id'].id  # this is for initial testing ... should be removed
        fields['creator_id'] = self._generateCreatorId(assignor)

        fields['create_time'] = timezone.now()
        fields['update_time'] = fields['create_time']

        record = modelClass(**fields)
        record.save()
        self.log({'fields': fields}, f'Create For: [{tbl}]')
        return record

    def _generateParentId(self, dictionary):
        if 'parent' in dictionary:
            if isinstance(dictionary['parent'], object) and dictionary['parent'] is not None:
                return dictionary['parent'].id
        return None

    def _generateCreatorId(self, assignor):
        if self.currentUser is not None:
            return self.currentUser

        return assignor

    