from django.utils import timezone
from tasks.models import *
from core.helpers import crud, misc
from core import settings
from .Validation import ErrorHandling

"""
    This class holds the background crud operations.
"""
class Background(ErrorHandling):
    currentUser = None # FUTURE IMPLEMENTATION

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

    def saveSubmission(self, submission, operation):
        self.dictValidation(self.space, operation, submission)
        self.submission = submission

    def deleteChildTable(self, modelClass, tbl, tableName, columnsList, masterId):
        fieldsF = {}  # fields to find records with
        fieldsF[self.dbConfigs['master_id']] = masterId
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

    def updateMasterTable(self, space, completeRecord, newRecordDictionary, mtModel, tableName, columnsList):
        fields = {}

        for col in columnsList:
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = self.dbConfigs['mtAbbrv'] + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:
                if newRecordDictionary[key] != getattr(completeRecord, col):
                    fields[col] = newRecordDictionary[key]

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=newRecordDictionary[self.dbConfigs['mtAbbrv'] + 'id']).update(**fields)
        misc.log({'fields': fields}, f'Update For: [{self.dbConfigs['mtAbbrv']}]')
        return None

    def updateChildTable(self, modelClass, completeRecord, tbl, tableName, columnsList, newRecordDictionary):
        misc.log(modelClass, f'ENTERING update for [{tbl}]')

        if not hasattr(completeRecord, tbl + 'id'):
            raise Exception(f'Something went wrong. Update record not found in system. {self.space}.CRUD.update()')

        updateRequired = False
        for col in columnsList:
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = tbl + col  # need tbl-abbrv prefix for comparison

            if key in newRecordDictionary:
                if isinstance(newRecordDictionary[key], object):
                    if hasattr(newRecordDictionary[key], 'id'):
                        # need to overwrite dictionary key with int value for comparison
                        newRecordDictionary[key] = newRecordDictionary[key].id
                        continue
                
                if col in self.dbConfigs['updates']['ignore'][tableName]:
                    continue  # ignore columns don't need a comparison in child-update operations

                if newRecordDictionary[key] != getattr(completeRecord, col):
                    misc.log([newRecordDictionary[key], getattr(completeRecord, col)], f' - UPDATE CHILD Opr.: these form, DB values for [{col}] column did not match.')
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:  
            fields = {}
            fields['delete_time'] = timezone.now()
            fields['latest'] = self.module['values']['latest']['archive']
            
            # update old record, create new one...
            modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
            misc.log({'fields': fields}, f'Update For: [{tbl}]')
            self.createChildTable(modelClass, tbl, tableName, columnsList, newRecordDictionary)

        return None

    def createChildTable(self, modelClass, tbl, tableName, columnsList, newRecordDictionary):
        masterId = self.dbConfigs['mtId']  # grab master_id for this space
        
        if masterId not in newRecordDictionary:
            newRecordDictionary[masterId] = newRecordDictionary[self.dbConfigs['mtAbbrv'] + 'id']

        if not crud.isValidId(newRecordDictionary, masterId):
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        fields = {}
        
        for col in columnsList:
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    if isinstance(newRecordDictionary[key], object):
                        if hasattr(newRecordDictionary[key], 'id'):
                            fields[col] = newRecordDictionary[key].id  # must be a foreignkey Model instance, grab only the id.
                            continue
                        fields[col] = None
                        continue
                    fields[col] = newRecordDictionary[key]

        if len(fields) <= 1:  # if record is empty, abort insertion...
            if self.dbConfigs['mtId'] in fields:
                return None  # only the master ID is added, no need need to insert

        fields['create_time'] = timezone.now()
        fields['latest'] = 1
        record = modelClass(**fields)
        record.save()
        misc.log({'fields': fields}, f'Create For: [{tbl}]')
        return record

    def createMasterTable(self, tbl, modelClass, newRecordDictionary):
        t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
        record = {}

        for col in t['cols']:
            # get the correct key reference for column in newRecordDictionary...
            if crud.isProblematicKey(self.dbConfigs['keys']['problematic'], col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    record[col] = newRecordDictionary[key]

        if len(record) == 0:  # if record is empty, abort insertion...
            return None

        record['parent_id'] = self._generateParentId(newRecordDictionary)
        assignor = newRecordDictionary['assignor_id'].id  # this is for initial testing ... should be removed
        record['creator_id'] = self._generateCreatorId(assignor)

        record['create_time'] = timezone.now()
        record['update_time'] = record['create_time']

        record = modelClass(**record)
        record.save()
        misc.log({'fields': record}, f'Create For: [{tbl}]')
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
