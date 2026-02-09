from django.db import models
from django.utils import timezone
from core.helpers import crud, strings
from .create import Create
from .values import Values

class Update:
    """
        Static class
        Handles all update operations for CRUD
        @todo: reconcile create and update operation checks. Should be the same
    """

    @staticmethod
    def masterTable(state, mapper, mtModel, tableName, columnsList, completeRecord, rlc = False):
        state.get('log').record(None, f'ENTERING update for MT [{tableName}]')

        if not completeRecord.id or completeRecord.id is None:
            raise Exception(f'Something went wrong. Update record not found in system. {state.get('app')}.CRUD.update()')

        fields = {}
        ignored = mapper.ignoreOnUpdates(mapper.master('abbreviation'))

        for col in columnsList:
            if col in ignored:
                continue  # ignore columns don't need a comparison in update operations

            if mapper.isCommonField(col):
                key = mapper.master('abbreviation') + '_' + col  # need tbl_abbrv prefix for comparison
            else:
                key = col

            if key in state.get('submission'):
                state.get('submission')[key] = Values.convertModelToId(getattr(completeRecord, col), state.get('submission')[key])
                dbVal = Values.amendDatabaseValue(getattr(completeRecord, col), state.get('submission')[key])
                
                state.get('log').record([key, col], 'comparing in MT Update')

                if state.get('submission')[key] != dbVal:
                    fields[col] = state.get('submission')[key]
                    state.get('log').record([key, state.get('submission')[key], col, dbVal], 'MISMATCH')

        fields['update_time'] = timezone.now()

        mtModel.objects.filter(id=completeRecord.id).update(**fields)
        state.get('log').record({'fields': fields}, f'Update For: [{tableName}]')
        return None

    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, completeRecord, rlc = False):
        state.get('log').record(None, f'ENTERING update for childtable [{tbl}]')

        if not hasattr(completeRecord, tbl + 'id') or getattr(completeRecord, tbl + 'id') is None:
            raise Exception(f'Something went wrong. Update record not found in system. {state.get('app')}.CRUD.update()')

        updateRequired = False
        ignored = mapper.ignoreOnUpdates(tbl)
        rlcFields = {}  # fields for RLC update

        for col in columnsList:
            if col in ignored:
                continue  # ignore columns don't need a comparison in update operations

            if mapper.isCommonField(col):
                key = tbl + col  # need tbl-abbrv prefix for comparison
            else:
                key = col

            if key in state.get('submission'):
                if isinstance(state.get('submission')[key], models.Model):
                    state.get('submission')[key] = Values.convertModelToId(state.get('submission')[key])
                
                if col in mapper.dateFields():
                    dbVal = Values.amendDatabaseValue(getattr(completeRecord, col))
                else:
                    dbVal = getattr(completeRecord, col)

                state.get('log').record([key, col], 'comparing in CT Update')

                if state.get('submission')[key] != dbVal:
                    state.get('log').record([key, state.get('submission')[key], col, dbVal], f'MISMATCH -  update needed')
                    rlcFields[col] = dbVal
                    updateRequired = True  # changes found in dictionary record

        if updateRequired:
            if rlc:
                rlcFields['update_time'] = timezone.now()
                modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**rlcFields)
                state.get('log').record({'fields': rlcFields}, f'Update For: [{tbl}] | [RLC]')
            else:
                fields = {}
                fields['delete_time'] = timezone.now()
                fields['latest'] = mapper.values.latest('archive')
                
                # update old record, create new one...
                modelClass.objects.filter(id=getattr(completeRecord, tbl + 'id')).update(**fields)
                state.get('log').record({'fields': fields}, f'Update For: [{tbl}]')
                Create.childTable(state, mapper, modelClass, tbl, tableName, columnsList)

        return None


