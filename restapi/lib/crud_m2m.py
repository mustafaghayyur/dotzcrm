from rest_framework.response import Response
from rest_framework import status

from core.helpers import crud
from core.lib.state import State


class M2MOperations():
    def __init__(self, state: State):
        self.state = state

    def create(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        cruder = CrudClass()
        idKey = self.state.get('tbl') + '_' + cruder.getMapper().column('id')
        mtIdKey = cruder.getMapper().master('foreignKeyName')
        data = self.satte.get('data')

        if crud.isValidId({'id': data.get(mtIdKey, None)}, 'id'):
            dictinary = {
                mtIdKey: data.get(mtIdKey, None),  # @todo: crud system should add current users to relevent fields defined in mapper.
            }
            result = CrudClass().create(dictinary)
            if result:
                return Response(crud.generateResponse({idKey: result.id}), status=status.HTTP_201_CREATED) # @todo: can 201 responses carry payloads?
            return Response(crud.generateError('Created record could not be fetched.'), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(None, 'Request could not be processed due to invalid task ID.'), status=status.HTTP_400_BAD_REQUEST)
    

    def update(self):
        return Response(crud.generateError('Watcher records cannot be updated.'), status=status.HTTP_400_BAD_REQUEST) 


    def delete(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        itemId = self.state.get('data').get('item_id', None)
        cruder = CrudClass()
        mtIdKey = cruder.getMapper().master('foreignKeyName')
        idKey = self.state.get('tbl') + '_' + cruder.getMapper().column('id')
        data = self.satte.get('data')
        
        if crud.isValidId({'id': itemId}, 'id'):
            dictinary = {
                'task_id': itemId,
                'watcher_id': self.state.get('user').id
            }
            CrudClass().delete(dictinary)
            # @todo: confirm if crud is showing deletion
            return Response(crud.generateResponse([]), status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Watcher ID not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 


    def read(self):
        GenericSerializer = self.state.get('serializerClass')
        CrudClass = self.state.get('crudClass')
        itemId = self.state.get('data').get('item_id', None)

        if crud.isValidId({'id': itemId}, 'id'):
            dictinary = {
                'task_id': itemId,
                'watcher_id': self.state.get('user').id 
            }
            record = CrudClass().read(dictinary)
            if record:
                serialized = GenericSerializer(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateResponse([]))
        return Response(crud.generateError('Watcher Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
        