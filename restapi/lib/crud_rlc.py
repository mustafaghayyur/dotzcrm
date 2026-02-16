from rest_framework.response import Response
from rest_framework import status

from core.helpers.crud import generateError, generateResponse, isValidId
from core.helpers.pagination import assembleParamsForView, determineHasMore
from core.lib.state import State


class RLCOperations():
    def __init__(self, state: State):
        self.state = state

    def create(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        cruder = CrudClass()
        data = self.satte.get('data')
        idKey = self.state.get('tbl') + '_' + cruder.getMapper().column('id')
        
        serialized = GenericSerializer(data=data)
        if serialized.is_valid():
            dictionary = serialized.validated_data
            dictionary['creator_user_id'] = self.state.get('user').id
            result = cruder.create(dictionary)
            if result:
                try:
                    record = cruder.read({idKey: result.id})
                    retrievedSerialized = GenericSerializer(record[0])
                    return Response(generateResponse(retrievedSerialized.data), status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(generateError(e, "Could not retrieve created record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(generateError("Could not determine create response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(generateError(serialized.errors, "Validation errors occured."), status=status.HTTP_400_BAD_REQUEST)
        
    def update(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        cruder = CrudClass()
        data = self.satte.get('data')
        idKey = self.state.get('tbl') + '_' + cruder.getMapper().column('id')

        serialized = GenericSerializer(data=data)
        if serialized.is_valid():
            result = cruder.update(serialized.validated_data)
            if result:
                try:
                    record = cruder.read({idKey: result.id})
                    retrievedSerialized = GenericSerializer(record[0])
                    return Response(generateResponse(retrievedSerialized.data), status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(generateError(e, "Could not retrieve updated record."), status=status.HTTP_400_BAD_REQUEST)
            return Response(generateError("Could not determine update response."), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(generateError(serialized.errors), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self):
        """
            Delete RLC record bet its ID.
        """
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        cruder = CrudClass()
        data = self.satte.get('data')
        idKey = self.state.get('tbl') + '_' + cruder.getMapper().column('id')

        if isValidId({idKey: id}, idKey):
            results = cruder.delete(data.get(idKey))
            return Response(generateResponse({
                'results': results,
                'messages': 'Rows affected shown in results.'
            }), status=status.HTTP_200_OK)
        
        return Response(generateError('Comment id not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 

    def read(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        cruder = CrudClass()
        data = self.satte.get('data')
        fk_name = cruder.getMapper().master('foreignKeyName')
        request = self.state.get('request')

        pgntn = assembleParamsForView(request.query_params)

        records = cruder.read({
            fk_name: data.get(fk_name),
        })
        serialized = GenericSerializer(records, many=True)
        hasMore = determineHasMore(records, pgntn['page_size'])

        return Response(generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
