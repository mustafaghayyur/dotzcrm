from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tasks.models import *
from tasks.validators.tasks import *
from tasks.drm.crud import CRUD
from pydantic import ValidationError

"""
    Views starting with [_H_] are not directly accessible by django urls.
    They serve to handle (thus the 'H') a specific HTTP method request.

    _H_ usually acompany {someObject}_crud() views; and handle full crud operations.

    NOTE: the [request] argument being passed to views with the @api_view decorator,
        are not the conventional Django request objects. Rather, DRF's enhanced
        Request object.
"""
@api_view(['GET'])
def task_list(request, format=None):
    """
    List all  tasks for ____
    """
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def task_crud(request, format=None):
    method = request.method

    match method:
        case 'GET':
            return _H_task_detail(request, format)
        case 'POST':
            return _H_task_create(request, format)
        case 'PUT':
            return _H_task_edit(request, format)
        case 'DELETE':
            return _H_task_delete(request, format)
        case _:
            return Response(status=status.HTTP_400_BAD_REQUEST)

"""
======================== HANDLER FUNCTIONS ===============================
"""
def _H_task_create(request, format=None):
    """
        Create single task record (with all it's related child-tables).
    """
    try:
        serializer = TaskO2ORecord(**request.data)
        result = CRUD().create(serializer.model_dump())
        return Response(result, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'errors': e.errors()}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)

def _H_task_edit(request, pk, format=None):
    """
        Edit single task record (with all it's related child-tables).
    """
    try:
        serializer = TaskO2ORecord(**request.data)
        result = CRUD().update(serializer.model_dump())
        return Response(result)
    except ValidationError as e:
        return Response({'errors': e.errors()}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)

def _H_task_delete(request, pk, format=None):
    """
        Delete single task record (with all it's related child-tables).
    """
    try:
        crud = CRUD()
        crud.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)
    

def _H_task_detail(request, pk, format=None):
    """
        Retrieve single task record (with all it's related child-tables).
    """
    try:
        crud = CRUD()
        crud.read(pk)
        record = CRUD().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
        if record:
            return Response(record[0])
    except Exception as e:
        return Response(f'Error: {e}', status=status.HTTP_400_BAD_REQUEST)
    