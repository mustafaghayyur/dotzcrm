from rest_framework.response import Response
from rest_framework import status
from restapi.validators.tasks import *
from tasks.drm.crud import CRUD
from core.helpers import pagination

"""
    These Static Classes are meant to help views with CRUD operations
"""

class OneToOnes():
    @staticmethod
    def create(request, format=None):
        """
            Create single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = CRUD().create(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError('Could not validate submitted data.')
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = CRUD().update(serializer.validated_data)
            return Response(result)
        else:
            raise ValidationError('Could not validate submitted data.')
    
    @staticmethod
    def delete(request, pk, format=None):
        """
            Delete single task record (with all it's related child-tables).
        """
        crud = CRUD().delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)    

    @staticmethod
    def detail(request, pk, format=None):
        """
            Retrieve single task record (with all it's related child-tables).
        """
        record = CRUD().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
        if record:
            serialized = TaskO2ORecord(record[0])
            return Response(serialized.data)
        
class Comments():
    @staticmethod
    def create(request, format=None):
        """
            Create single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = CRUD().create(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError('Could not validate submitted data.')
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = CRUD().update(serializer.validated_data)
            return Response(result)
        else:
            raise ValidationError('Could not validate submitted data.')
    
    @staticmethod
    def delete(request, pk, format=None):
        """
            Delete single task record (with all it's related child-tables).
        """
        crud = CRUD().delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)    

    @staticmethod
    def detail(request, pk, format=None):
        """
            Retrieve single task record (with all it's related child-tables).
        """
        record = CRUD().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
        if record:
            serialized = TaskO2ORecord(record[0])
            return Response(serialized.data)
        
class Watchers():
    @staticmethod
    def create(request, format=None):
        """
            Create single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = CRUD().create(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError('Could not validate submitted data.')
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = CRUD().update(serializer.validated_data)
            return Response(result)
        else:
            raise ValidationError('Could not validate submitted data.')
    
    @staticmethod
    def delete(request, pk, format=None):
        """
            Delete single task record (with all it's related child-tables).
        """
        crud = CRUD().delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)    

    @staticmethod
    def detail(request, pk, format=None):
        """
            Retrieve single task record (with all it's related child-tables).
        """
        record = CRUD().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
        if record:
            serialized = TaskO2ORecord(record[0])
            return Response(serialized.data)