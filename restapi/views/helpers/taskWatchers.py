from rest_framework.response import Response
from rest_framework import status

from tasks.validators.taskM2Ms import WatcherSerializerGeneric
from tasks.drm.crud import Watchers
from core.helpers import crud, misc

"""
    These Static Classes are meant to help views with CRUD operations
"""  
class WatchersMethods():
    @staticmethod
    def create(request, taskId, format=None):
        """
            Create watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': taskId}, 'id'):
            dictinary = {
                'task_id': taskId,
                'watcher_id': request.user.id #@todo: remove 1 and add user id.
            }
            result = Watchers().create(dictinary)
            if result:
                return Response(crud.generateResponse({'wid': result.id}), status=status.HTTP_201_CREATED) # @todo: can 201 responses carry payloads?
            return Response(crud.generateError('Created record could not be fetched.'), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(None, 'Request could not be processed due to invalid task ID.'), status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            no updates allowed for watcher
        """
        return Response(crud.generateError('Watcher records cannot be updated.'), status=status.HTTP_400_BAD_REQUEST) 
    
    @staticmethod
    def delete(request, taskId, format=None):
        """
            Delete single watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': taskId}, 'id'):
            dictinary = {
                'task_id': taskId,
                'watcher_id': request.user.id
            }
            Watchers().delete(dictinary)
            # @todo: confirm if crud is showing deletion
            return Response(crud.generateResponse([]), status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Watcher ID not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    def detail(request, taskId, format=None):
        """
            Retrieve single watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': taskId}, 'id'):
            dictinary = {
                'task_id': taskId,
                'watcher_id': request.user.id 
            }
            record = Watchers().read(dictinary)
            if record:
                serialized = WatcherSerializerGeneric(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateResponse([]))
        return Response(crud.generateError('Watcher Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
        