from rest_framework.response import Response
from rest_framework import status

from tasks.validators.tasks import *
from tasks.drm.crud import CRUD
from core.helpers import crud, misc

"""
    These Static Classes are meant to help views with CRUD operations
"""

class OneToOnes():
    @staticmethod
    def create(request, format=None):
        """
            Create single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecordSerializerGeneric(data=request.data)
        if serializer.is_valid():
            result = CRUD().create(serializer.validated_data)

            if result:
                try:
                    record = CRUD().fetchFullRecordForUpdate(result.id)
                    retrievedSerialized = TaskO2ORecordSerializerGeneric(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve created record."), status=status.HTTP_400_BAD_REQUEST)
            
            return Response(crud.generateError("Could not determine create response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors, "Validation errors occured."), status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecordSerializerGeneric(data=request.data)

        if serializer.is_valid():
            result = CRUD().update(serializer.validated_data)
            # attempt to serialize the updated consolidated record
            if result:
                try:
                    record = CRUD().fetchFullRecordForUpdate(result['tid'])
                    retrievedSerialized = TaskO2ORecordSerializerGeneric(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve updated record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(crud.generateError("Could not determine update response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
                
    @staticmethod
    def delete(request, id, format=None):
        """
            Delete single task record (with all it's related child-tables).
        """
        if crud.isValidId({'id': id}, 'id'):
            rec = CRUD().delete(id)
            return Response(crud.generateResponse([]), status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Task id not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    def detail(request, id, format=None):
        """
            Retrieve single task record (with all it's related child-tables).
        """
        if crud.isValidId({'id': id}, 'id'):
            record = CRUD().fetchFullRecordForUpdate(id)
            if record:
                serialized = TaskO2ORecordSerializerGeneric(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateResponse([]), status=status.HTTP_400_BAD_REQUEST)
        return Response(crud.generateError('Task Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
        
