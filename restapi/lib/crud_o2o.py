from rest_framework.response import Response
from rest_framework import status

from core.helpers import crud
from core.lib.state import State


class O2OOperations():
    def __init__(self, state: State):
        self.state = state

    def create(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        serializer = GenericSerializer(data=self.state.get('data'))
        if serializer.is_valid():
            result = CrudClass().create(serializer.validated_data)

            if result:
                try:
                    record = CrudClass().fullRecord(result.id)
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
            result = CrudClass().update(serializer.validated_data)
            # attempt to serialize the updated consolidated record
            if result:
                try:
                    record = CrudClass().fullRecord(result['tid'])
                    retrievedSerialized = GenericSerializer(record[0])
                    return Response(crud.generateResponse(retrievedSerialized.data), status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(crud.generateError(e, "Could not retrieve updated record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(crud.generateError("Could not determine update response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)


    def delete(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        
        if crud.isValidId({'id': id}, 'id'):
            rec = CrudClass().delete(id)
            return Response(crud.generateResponse([]), status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Task id not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 


    def read(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')

        self.state.set('operation', 'read')
        if crud.isValidId({'id': id}, 'id'):
            record = CrudClass().fullRecord(id)
            if record:
                serialized = GenericSerializer(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateResponse([]), status=status.HTTP_400_BAD_REQUEST)
        return Response(crud.generateError('Task Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
     