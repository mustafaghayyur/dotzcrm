from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.helpers import pagination, crud, misc
from restapi.lib.helpers import *
from tasks.drm.crud import *
from tasks.drm.mapper_values import ValuesMapper
from tasks.validators.tasks import TaskO2ORecordSerializerGeneric

@api_view(['GET'])
def list(request, type, format=None):
    """
        List all tasks for type of request.
    """
    selectors = ['tata_id', 'tast_id', 'description', 'tata_update_time', 'status']
    conditions = {
        'tata_delete_time': 'is Null',
        'assignee_id': request.user.id
    }

    match type:
        case 'private':
            conditions['visibility'] = 'private'
        case 'workspaces':
            vm = ValuesMapper()
            conditions['workspace'] = None
            conditions['visibility'] = 'workspaces'
            conditions['status'] = [vm.status('assigned'), vm.status('queued'), vm.status('started')]
            selectors.append('deadline')
        case '_':
            pass

    try:
        pgntn = pagination.assembleParamsForView(request.query_params)
        
        records = Tasks().read(selectors, conditions, limit=[str(pgntn['offset']), str(pgntn['page_size'])])
        serialized = TaskO2ORecordSerializerGeneric(records, many=True)
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)


