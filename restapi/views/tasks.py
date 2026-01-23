from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import authentication_classes, permission_classes

from core.helpers import pagination, crud, misc

from tasks.drm.crud import *
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

    Possible decorators:
        @authentication_classes([JWTAuthentication])
"""
@api_view(['GET'])
def task_list(request, type, format=None):
    """
        List all tasks for type of request.
    """
    selectors = ['tid', 'sid', 'description', 'tupdate_time', 'status']
    conditions = {
        'tdelete_time': 'is Null',
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
        
        records = CRUD().read(selectors, conditions, limit=[str(pgntn['offset']), str(pgntn['page_size'])])
        serialized = TaskO2ORecordSerializerGeneric(records, many=True)
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def task_crud(request, id, format=None):
    """
        CRUD operations for individual Task O2O records.
    """
    method = request.method
    try:
        match method:
            case 'GET':
                return OneToOnes.detail(request, id, format)
            case 'POST':
                return OneToOnes.create(request, format)
            case 'PUT':
                return OneToOnes.edit(request, format)
            case 'DELETE':
                return OneToOnes.delete(request, id, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def comment_crud(request, id, format=None):
    """
        CRUD operations for individual Comment records.
    """
    method = request.method
    
    try:
        match method:
            case 'GET':
                return CommentMethods.detail(request, id, format)
            case 'POST':
                return CommentMethods.create(request, format)
            case 'PUT':
                return CommentMethods.edit(request, format)
            case 'DELETE':
                return CommentMethods.delete(request, id, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def comments_list(request, taskId, format=None):
    """
        List all  tasks for type of request
    """
    selectors = ['tid', 'description', 'creator_id', 'tupdate_time', 'status', 'visibility', 'assignor_id']
    conditions = {
        #'delete_time': 'is Null',
        'task_id': taskId, # old: request.query_params.get('task_id', 0),
    }

    try:
        pgntn = pagination.assembleParamsForView(request.query_params)
        # limit=[str(pgntn['offset']), str(pgntn['page_size']
        records = Comments().read(conditions)
        misc.log(records, 'hello from comment lists')
        serialized = CommentSerializerGeneric(records, many=True)
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'DELETE'])
def watcher_crud(request, taskId, format=None):
    """
        CRUD operations for individual Watcher O2O records.
        Updates not allowed.
        Handles watcher requests with current-user as watcher only
    """
    method = request.method
    
    try:
        match method:
            case 'GET':
                return WatchersMethods.detail(request, taskId, format)
            case 'POST':
                return WatchersMethods.create(request, taskId, format)
            case 'DELETE':
                return WatchersMethods.delete(request, taskId, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def watchers_list(request, taskId, format=None):
    """
        List all watchers for task and current user
    """
    conditions = {
        'task_id': taskId,
        'latest': ValuesMapper().latest('latest')  # @todo readd: request.user.id,
    }
    try:
        records = Watchers().read(conditions)
        if records:
            serialized = WatcherSerializerGeneric(records, many=True)
            return Response(crud.generateResponse(serialized.data))
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)

