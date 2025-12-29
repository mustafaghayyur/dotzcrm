from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tasks.models import *
from tasks.validators.tasks import *

@api_view(['GET'])
def task_list(request, format=None):
    """
    List all snippets, or create a new snippet.
    """
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def task_create(request, format=None):
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def task_edit(request, pk, format=None):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def task_delete(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def task_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)