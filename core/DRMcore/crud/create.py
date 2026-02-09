from django.utils import timezone
from core.helpers import crud, strings
from .values import Values

class Create:
    """
        Static class
        Handles all create operations for CRUD
    """

    @staticmethod
    def childTable(state, mapper, modelClass, tbl, tableName, columnsList, rlc = False):
        state.get('log').record(None, f'Entering create operation for childtable: [{tbl}]')
        
        fields = {}
        for col in columnsList:
            if mapper.isCommonField(col):
                key = tbl + col  # add on a prefix to match state.get('submission') keys
            else:
                key = col

            if key in state.get('submission'):
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    if isinstance(state.get('submission')[key], object):
                        if hasattr(state.get('submission')[key], 'id'):
                            state.get('submission')[key] = state.get('submission')[key].id  # must be a foreignkey Model instance, grab only the id.
                    
                    fields[col] = state.get('submission')[key]
                    state.get('log').record([key, state.get('submission')[key]], 'Field added')

        if len(fields) <= 1:  # if record is empty, abort insertion...
            if mapper.master('foreignKeyName') in fields:
                return None  # only the master ID is added, no need need to insert

        fields['create_time'] = timezone.now()
        if rlc:
            fields['update_time'] = fields['create_time']
        else:
            fields['latest'] = 1

        record = modelClass(**fields)
        record.save()
        designation = '[RLC]' if rlc else ''
        state.get('log').record({'fields': fields}, f'Create For: [{tbl}] | {designation}')
        return record


    @staticmethod
    def masterTable(state, mapper, tbl, modelClass, rlc = False):
        state.get('log').record(None, f'Entering create operation for MT: [{tbl}]')
        
        t = crud.generateModelInfo(mapper, tbl)
        fields = {}

        for col in t['cols']:
            # get the correct key reference for column in state.get('submission')...
            if mapper.isCommonField(col):
                key = tbl + col  # add on a prefix to match state.get('submission') keys
            else:
                key = col

            if key in state.get('submission'):
                if col not in ['delete_time', 'create_time', 'update_time', 'id']:
                    if isinstance(state.get('submission')[key], object):
                        if hasattr(state.get('submission')[key], 'id'):
                            state.get('submission')[key] = state.get('submission')[key].id  # must be a foreignkey Model instance, grab only the id.
                    
                    fields[col] = state.get('submission')[key]
                    state.get('log').record(key, state.get('submission')[key], 'Field added')

        if len(fields) == 0:  # if fields is empty, abort insertion...
            return None

        fields['creator_id'] = Create.generateCreatorId()
        fields['create_time'] = timezone.now()
        fields['update_time'] = fields['create_time']

        record = modelClass(**fields)
        record.save()
        state.get('log').record({'fields': fields}, f'Create For: [{tbl}]')
        return record
    

    @staticmethod
    def generateCreatorId(state,  mapper):
        if 'assignor_id' in state.get('submission'):
            if state.get('submission')['assignor_id'] is not None:

                if strings.isPrimitiveType(state.get('submission')['assignor_id']):
                    return state.get('submission')['assignor_id']
                if hasattr(state.get('submission')['assignor_id'], 'id'):
                    return state.get('submission')['assignor_id'].id
                
        return None