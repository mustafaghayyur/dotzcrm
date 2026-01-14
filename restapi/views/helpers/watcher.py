from rest_framework.response import Response
from rest_framework import status

from tasks.validators.tasks import *
from tasks.drm.crud import Watchers
from core.helpers import crud, misc

"""
    These Static Classes are meant to help views with CRUD operations
"""  
class WatchersMethods():
    @staticmethod
    def create(request, format=None):
        """
            Create watcher record.
            @current_user focussed
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = Watchers().create(serializer.validated_data)
            if result:
                misc.log(result, 'peaking into Watcher create result')
                return Response(crud.generateResponse({'wid': result.id}), status=status.HTTP_201_CREATED) # @todo: can 201 responses carry payloads?
            return Response(crud.generateError('Created record could not be fetched.'), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(crud.generateError(serializer.errors, 'Request could not be processed due to validation errors.'), status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            no updates allowed for watcher
        """
        return Response(crud.generateError('Watcher records cannot be updated.'), status=status.HTTP_400_BAD_REQUEST) 
    
    @staticmethod
    def delete(request, id, format=None):
        """
            Delete single watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': id}, 'id'):
            crud = Watchers().delete(id)
            # @todo: confirm if crud is showing deletion
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(crud.generateError('Watcher ID not valid. Delete aborted.'), status=status.HTTP_400_BAD_REQUEST) 

    @staticmethod
    def detail(request, id, format=None):
        """
            Retrieve single watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': id}, 'id'):
            record = Watchers().read(['wid'], {'task_id': id, 'watcher_id': request.user.id, 'wdelete_time': 'is NULL', 'wlatest': 1})
            if record:
                serialized = TaskO2ORecord(record[0])
                return Response(crud.generateResponse(serialized.data))
            return Response(crud.generateError('No watcher record found.'), status=status.HTTP_400_BAD_REQUEST)
        return Response(crud.generateError('Watcher Record ID not valid.'), status=status.HTTP_400_BAD_REQUEST)
        