from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from restapi.validators.tasks import *
from tasks.drm.crud import CRUD
from core.helpers import pagination, misc
from .helpers.task import *

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
        'assignee_id': 1  # @todo readd: request.user.id,
    }

    #misc.log(request.user, 'Investigating why assignee is not making it to query in rest.tasks.list()', 2)

    match type:
        case 'private':
            conditions['visibility'] = 'private'
            selectors.append('details')
        case 'workspaces':
            conditions['workspace'] = None
            conditions['assignee_id'] = None
            conditions['visibility'] = 'workspaces'
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
                return OneToOnes.detail(request, pk, format)
            case 'POST':
                return OneToOnes.create(request, format)
            case 'PUT':
                return OneToOnes.edit(request, format)
            case 'DELETE':
                return OneToOnes.delete(request, pk, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response({'errors': e.errors()}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def comments_crud(request, pk, format=None):
    method = request.method
    
    try:
        match method:
            case 'GET':
                return Comments.detail(request, pk, format)
            case 'POST':
                return Comments.create(request, format)
            case 'PUT':
                return Comments.edit(request, format)
            case 'DELETE':
                return Comments.delete(request, pk, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response({'errors': e.errors()}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)
    