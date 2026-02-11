from rest_framework.response import Response
from rest_framework import status

from core.helpers import crud
from core.lib.state import State


class RLCOperations():
    def __init__(self, state: State):
        self.state = state

    def create(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        
        serializer = GenericSerializer(data=self.state.get('data'))
        if serializer.is_valid():
            dictionary = serializer.validated_data
            dictionary['creator_user_id'] = self.state.get('user').id
            result = CrudClass().create(dictionary)
            if result:
                try:
                    record = CrudClass().read({'cid': result.id})
                    retrievedSerialized = GenericSerializer(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve created record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(crud.generateError("Could not determine create response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors, "Validation errors occured."), status=status.HTTP_400_BAD_REQUEST)
        
    def update(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')

        serializer = GenericSerializer(data=self.state.get('data'))
        if serializer.is_valid():
            dictionary = serializer.validated_data
            dictionary['creator_user_id'] = self.state.get('user').id
            result = CrudClass().update(dictionary)
            if result:
                try:
                    record = CrudClass().read({'cid': result.id})
                    retrievedSerialized = GenericSerializer(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_200_OK) # @todo: correct response?
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve updated record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(crud.generateError("Could not determine update response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')

        if crud.isValidId({'id': id}, 'id'):
            crud = CrudClass().delete(id)
            return Response(crud.generateResponse([]), status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Comment id not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 

    def read(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')

        if crud.isValidId({'id': id}, 'id'):
            record = CrudClass().read(['all'], {'task_id': id, 'delete_time': 'is NULL'})
            if record:
                serialized = GenericSerializer(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateResponse([]))
        return Response(crud.generateError('Comment Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
        
  