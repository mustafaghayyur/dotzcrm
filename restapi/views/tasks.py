from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.helpers import pagination, crud, misc

from tasks.drm.crud import CRUD
from tasks.drm.mapper_values import ValuesMapper
from tasks.validators.tasks import TaskO2ORecordSerializerGeneric
from tasks.validators.comments import CommentSerializerGeneric
from tasks.validators.watchers import WatcherSerializerGeneric
from .helpers.tasksO2Os import OneToOnes
from .helpers.taskComments import CommentMethods
from .helpers.taskWatchers import WatchersMethods

"""
    Classes under views/helpers are not directly accessible by django urls.
    They serve to handle a specific HTTP method request.

    NOTE: the [request] argument being passed to views with the @api_view decorator,
        is not the conventional Django request object. Rather, DRF's enhanced
        Request object.
"""
@api_view(['GET'])
def task_list(request, type, format=None):
    """
        List all  tasks for type of request
    """
    selectors = ['tid', 'description', 'creator_id', 'tupdate_time', 'status', 'assignor_id']
    conditions = {
        'tdelete_time': 'is Null',
        'assignee_id': request.user.id
    }

    #misc.log(request.user, 'Investigating why assignee is not making it to query in rest.tasks.list()', 2)

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
        
        records = CRUD().read(selectors, conditions, limit=[str(pgntn['offset']), str(pgntn['page_size'])])
        serialized = TaskO2ORecordSerializerGeneric(records, many=True)
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        details = getattr(e, 'detail', str(e))
        return Response(crud.generateError([e, details], "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

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
        details = getattr(e, 'detail', str(e))
        return Response(crud.generateError([e, details], "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def comment_crud(request, pk, format=None):
    method = request.method
    
    try:
        match method:
            case 'GET':
                return CommentMethods.detail(request, pk, format)
            case 'POST':
                return CommentMethods.create(request, format)
            case 'PUT':
                return CommentMethods.edit(request, format)
            case 'DELETE':
                return CommentMethods.delete(request, pk, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        details = getattr(e, 'detail', str(e))
        return Response(crud.generateError([e, details], "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def comments_list(request, format=None):
    """
        List all  tasks for type of request
    """
    selectors = ['tid', 'description', 'creator_id', 'tupdate_time', 'status', 'visibility', 'assignor_id']
    conditions = {
        'tdelete_time': 'is Null',
        'assignee_id': 1  # @todo readd: request.user.id,
    }

    #misc.log(request.user, 'Investigating why assignee is not making it to query in rest.tasks.list()', 2)

    try:
        pgntn = pagination.assembleParamsForView(request.query_params)
        
        records = Comments().read(selectors, conditions, limit=[str(pgntn['offset']), str(pgntn['page_size'])])
        serialized = CommentSerializerGeneric(records, many=True)
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        details = getattr(e, 'detail', str(e))
        return Response(crud.generateError([e, details], "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'DELETE'])
def watcher_crud(request, pk, format=None):
    method = request.method
    
    try:
        match method:
            case 'GET':
                return WatchersMethods.detail(request, pk, format)
            case 'POST':
                return WatchersMethods.create(request, format)
            case 'DELETE':
                return WatchersMethods.delete(request, pk, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        details = getattr(e, 'detail', str(e))
        return Response(crud.generateError([e, details], "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def watchers_list(request, type, format=None):
    """
        List all  tasks for type of request
    """
    selectors = ['tid', 'description', 'creator_id', 'tupdate_time', 'status', 'visibility', 'assignor_id']
    conditions = {
        'tdelete_time': 'is Null',
        'assignee_id': 1  # @todo readd: request.user.id,
    }

    #misc.log(request.user, 'Investigating why assignee is not making it to query in rest.tasks.list()', 2)

    try:
        pgntn = pagination.assembleParamsForView(request.query_params)
        
        records = Comments().read(selectors, conditions, limit=[str(pgntn['offset']), str(pgntn['page_size'])])
        serialized = WatcherSerializerGeneric(records, many=True)
        
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        details = getattr(e, 'detail', str(e))
        return Response(crud.generateError([e, details], "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

