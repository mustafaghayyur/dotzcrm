from rest_framework.response import Response
from rest_framework import status

from tasks.validators.comments import CommentSerializerGeneric
from tasks.drm.crud import Comments
from core.helpers import crud, misc

"""
    These Static Classes are meant to help views with CRUD operations
"""
class CommentMethods():
    @staticmethod
    def create(request, format=None):
        """
            Create single comment record (with all it's related child-tables).
        """
        serializer = CommentSerializerGeneric(data=request.data)
        if serializer.is_valid():
            dictionary = serializer.validated_data
            dictionary['creator_user_id'] = request.user.id
            result = Comments().create(dictionary)
            if result:
                try:
                    record = Comments().read({'cid': result.id})
                    retrievedSerialized = CommentSerializerGeneric(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve created record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(crud.generateError("Could not determine create response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors, "Validation errors occured."), status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single comment record (with all it's related child-tables).
        """
        serializer = CommentSerializerGeneric(data=request.data)
        if serializer.is_valid():
            dictionary = serializer.validated_data
            dictionary['creator_user_id'] = request.user.id
            result = Comments().update(dictionary)
            if result:
                try:
                    record = Comments().read({'cid': result.id})
                    retrievedSerialized = CommentSerializerGeneric(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_200_OK) # @todo: correct response?
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve updated record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(crud.generateError("Could not determine update response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request, id, format=None):
        """
            Delete single comment record (with all it's related child-tables).
        """
        if crud.isValidId({'id': id}, 'id'):
            crud = Comments().delete(id)
            return Response(crud.generateResponse([]), status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Comment id not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    def detail(request, id, format=None):
        """
            Retrieve single comment record (with all it's related child-tables).
        """
        if crud.isValidId({'id': id}, 'id'):
            record = Comments().read(['all'], {'task_id': id, 'delete_time': 'is NULL'})
            if record:
                serialized = CommentSerializerGeneric(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateResponse([]))
        return Response(crud.generateError('Comment Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
        
        
