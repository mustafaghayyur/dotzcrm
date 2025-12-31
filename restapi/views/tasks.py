from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from restapi.validators.tasks import *
from tasks.drm.crud import CRUD
from core.helpers import pagination

"""
    Views starting with [_H_] are not directly accessible by django urls.
    They serve to handle (thus the 'H') a specific HTTP method request.

    _H_ usually acompany {someObject}_crud() views; and handle full crud operations.

    NOTE: the [request] argument being passed to views with the @api_view decorator,
        is not the conventional Django request object. Rather, DRF's enhanced
        Request object.
"""
@api_view(['GET'])
def task_list(request, type, format=None):
    """
        List all  tasks for type of request
    """
    selectors = ['tid', 'description', 'creator_id', 'tupdate_time', 'status', 'visibility', 'assignor_id']
    conditions = {
        'tdelete_time': 'is Null',
        'assignee': request.user.id,
    }

    match type:
        case 'private':
            conditions['visibility'] = 'private'
        case 'workspace':
            conditions['workspace'] = request.data['workspace']
            conditions['assignee'] = None
        case '_':
            pass

    try:
        pgntn = pagination.assembleParamsForView(request.query_params)
        
        records = CRUD().read(selectors, conditions, limit=[str(pgntn['offset']), str(pgntn['page_size'])])
        serialized = TaskO2ORecord(records, many=True)
        
        return Response({
            'page': pgntn['page'],
            'page_size': pgntn['page_size'],
            'has_more': pagination.determineHasMore(records, pgntn['page_size']),
            'results': serialized.data
        })
    except ValidationError as e:
        return Response(f'errors: {e}', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def task_crud(request, pk, format=None):
    method = request.method
    
    try:
        match method:
            case 'GET':
                return _H_task_detail(request, pk, format)
            case 'POST':
                return _H_task_create(request, format)
            case 'PUT':
                return _H_task_edit(request, format)
            case 'DELETE':
                return _H_task_delete(request, pk, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response({'errors': e.errors()}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)

"""
======================== HANDLER FUNCTIONS ===============================
"""
def _H_task_create(request, format=None):
    """
        Create single task record (with all it's related child-tables).
    """
    serializer = TaskO2ORecord(data=request.data)
    if serializer.is_valid():
        result = CRUD().create(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED)
    else:
        raise ValidationError('Could not validate submitted data.')
    

def _H_task_edit(request, format=None):
    """
        Edit single task record (with all it's related child-tables).
    """
    serializer = TaskO2ORecord(data=request.data)
    if serializer.is_valid():
        result = CRUD().update(serializer.validated_data)
        return Response(result)
    else:
        raise ValidationError('Could not validate submitted data.')
    
def _H_task_delete(request, pk, format=None):
    """
        Delete single task record (with all it's related child-tables).
    """
    crud = CRUD().delete(pk)
    return Response(status=status.HTTP_204_NO_CONTENT)    

def _H_task_detail(request, pk, format=None):
    """
        Retrieve single task record (with all it's related child-tables).
    """
    record = CRUD().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
    if record:
        serialized = TaskO2ORecord(record[0])
        return Response(serialized.data)
    