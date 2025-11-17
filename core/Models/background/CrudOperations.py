from django.utils import timezone
from tasks.models import *
from core.helpers import crud
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
        fieldsF = {}
        fieldsF[settings.rdbms[self.space]['master_id']] = masterId
        fieldsF['latest'] = settings[self.space]['values']['latest']['latest']
        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = settings[self.space]['values']['latest']['archive']
        
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
        return None

    def updateChildTable(self, modelClass, completeRecord, tbl, tableName, columnsList, newRecordDictionary):
        updateRequired = False
        for col in columnsList:
            if crud.isProblematicKey(settings.rdbms[self.space]['keys']['problematic'], col, True):
                key = tbl + col  # need tbl_abbrv prefix for comparison

            if key in newRecordDictionary:
                if newRecordDictionary[key] != getattr(completeRecord, col):
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:  # update record for child table
            fields = {}
            fields['delete_time'] = timezone.now()
            fields['latest'] = 2
            
            modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
            self.createChildTable(modelClass, tbl, tableName, columnsList, newRecordDictionary)

        return None

    def createChildTable(self, modelClass, tbl, tableName, columnsList, newRecordDictionary):
        """
        """
        if settings.rdbms[self.space]['master_id'] not in newRecordDictionary:
            raise Exception(f'Could not create child record; master_id missing. In {self.space}.CRUD.create()')

        fields = {}

        if tbl == 'a':
            misc.log(columnsList, f'checking columns for [{tbl}]')

        for col in columnsList:
            if crud.isProblematicKey(settings.rdbms[self.space]['keys']['problematic'], col, True):
                key = tbl + col  # add on a prefix to match newRecordDictionary keys
            else:
                key = col

            if key in newRecordDictionary:
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    if tbl == 'a':
                        misc.log(newRecordDictionary[key], f'KEY [{key}] check for assignment table')
                    if isinstance(newRecordDictionary[key], object):
                        if hasattr(newRecordDictionary[key], 'id'):
                            fields[col] = newRecordDictionary[key].id  # must be a foreignkey Model instance, grab only the id.
                            continue
                        fields[col] = None
                    fields[col] = newRecordDictionary[key]

        # if record is empty, abort insert...
        if len(fields) <= 1:
            if settings.rdbms[self.space]['master_id'] in fields:
                return None  # only the master ID is added, no need need to insert

        misc.log(fields, f'This is fields.dict for [{tbl}] table')

        fields['create_time'] = timezone.now()
        fields['latest'] = 1
        record = modelClass(**fields)
        record.save()

        misc.log(record, f'This is record for {tbl} table')
        return record

    def createMasterTable(self, tbl, modelClass, newRecordDictionary):
        t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
        misc.log(t['cols'], 'cols fot MT')
        tblColumns = settings.rdbms['tables'][settings.rdbms[self.space]['master_table']]
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
        misc.log([record.id, assignor], 'let\'s inspect the returned MT record create')
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
