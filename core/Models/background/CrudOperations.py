from django.utils import timezone
from tasks.models import *
from core.helpers import crud, misc
from core import settings
from .Validation import ErrorHandling

"""
    This class holds the background crud operations.
"""
class Background(ErrorHandling):
    mtabbrv = None  # master-table-abbreviation
    mtModel = None  # master-table-modelClass
    currentUser = None

    def __init__(self):
        super().__init__()

    def deleteChildTable(self, modelClass, latestRecord, tbl, tableName, columnsList, masterId):
        spaceSettings = getattr(settings, self.space)
        fieldsF = {}
        fieldsF[settings.rdbms[self.space]['master_id']] = masterId
        fieldsF['latest'] = spaceSettings['values']['latest']['latest']
        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = spaceSettings['values']['latest']['archive']
        
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)

    def deleteMasterTable(self, masterId):
        fieldsU = {}
        fieldsU['update_time'] = timezone.now()
        fieldsU['delete_time'] = fieldsU['update_time']
        
        return modelClass.objects.filter(id=masterId).update(**fieldsU)

    def updateMasterTable(self, space, completeRecord, newRecordDictionary, mtModel, tableName, columnsList):
        # update the QuerySet
        fields = {}

        for col in columnsList:
            if crud.isProblematicKey(settings.rdbms[self.space]['keys']['problematic'], col, True):
                key = self.mtabbrv + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:
                if newRecordDictionary[key] != getattr(completeRecord, col):
                    fields[col] = newRecordDictionary[key]

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=newRecordDictionary[self.mtabbrv + 'id']).update(**fields)
        misc.log({'fields': fields}, f'Update For: [{self.mtabbrv}]')
        return None

    def updateChildTable(self, modelClass, completeRecord, tbl, tableName, columnsList, newRecordDictionary):
        misc.log(modelClass, f'ENTERING update for [{tbl}]')
        updateRequired = False
        for col in columnsList:
            if crud.isProblematicKey(settings.rdbms[self.space]['keys']['problematic'], col, True):
                key = tbl + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:
                if isinstance(newRecordDictionary[key], object):
                    if hasattr(newRecordDictionary[key], 'id'):
                        # need to overwrite dictionary key with int value for comparison
                        newRecordDictionary[key] = newRecordDictionary[key].id
                        continue
                
                if col in settings.rdbms[self.space]['updates']['ignore'][tableName]:
                    continue  # ignore columns don't need a comparison in child-update operations

                if newRecordDictionary[key] != getattr(completeRecord, col):
                    misc.log([newRecordDictionary[key], getattr(completeRecord, col)], f' - UPDATE CHILD Opr.: these form, DB values for [{col}] column did not match.')
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:  # update old record for child table
            fields = {}
            fields['delete_time'] = timezone.now()
            fields['latest'] = getattr(settings, self.space)['values']['latest']['archive']
            
            modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
            misc.log({'fields': fields}, f'Update For: [{tbl}]')
            self.createChildTable(modelClass, tbl, tableName, columnsList, newRecordDictionary)

        return None

    def createChildTable(self, modelClass, tbl, tableName, columnsList, newRecordDictionary):
        """
        """
        masterId = settings.rdbms[self.space]['master_id']  # grab master_id for this space
        
        if masterId not in newRecordDictionary:
            newRecordDictionary[masterId] = newRecordDictionary[self.mtabbrv + 'id']

        if not crud.isValidId(newRecordDictionary, masterId):
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        fields = {}

        
        for col in columnsList:
            if crud.isProblematicKey(settings.rdbms[self.space]['keys']['problematic'], col, True):
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

        # if record is empty, abort insert...
        if len(fields) <= 1:
            if settings.rdbms[self.space]['master_id'] in fields:
                return None  # only the master ID is added, no need need to insert

        fields['create_time'] = timezone.now()
        fields['latest'] = 1
        record = modelClass(**fields)
        record.save()
        misc.log({'fields': fields}, f'Create For: [{tbl}]')
        return record

    def createMasterTable(self, tbl, modelClass, newRecordDictionary):
        t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
        
        masterTable = settings.rdbms[self.space]['master_table']
        tblColumns = settings.rdbms['tables'][masterTable]
        record = {}

        for col in tblColumns:
            if crud.isProblematicKey(settings.rdbms[self.space]['keys']['problematic'], col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    record[col] = newRecordDictionary[key]

        # if record is empty, abort insert...
        if len(record) == 0:
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
