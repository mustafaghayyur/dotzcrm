from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from tasks.validators.tasks import *
from tasks.drm.crud import CRUD, Comments, Watchers
from core.helpers import pagination, crud, misc

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
            # attempt to serialize the newly created consolidated record
            if result:
                try:
                    rec = result[0] if isinstance(result, (list, tuple)) else result
                    serialized = TaskO2ORecord(rec)
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': serialized.data,
                    }, status=status.HTTP_201_CREATED)
                except Exception:
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': result,
                    }, status=status.HTTP_201_CREATED)
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': result,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)

        if serializer.is_valid():
            result = CRUD().update(serializer.validated_data)
            # attempt to serialize the updated consolidated record
            if result:
                try:
                    rec = result[0] if isinstance(result, (list, tuple)) else result
                    serialized = TaskO2ORecord(rec)
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': serialized.data,
                    }, status=status.HTTP_200_OK)
                except Exception:
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': result,
                    }, status=status.HTTP_200_OK)
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': result,
            }, status=status.HTTP_200_OK)
        else:
            misc.log(serializer.errors, 'serializer.errors')
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request, pk, format=None):
        """
            Delete single task record (with all it's related child-tables).
        """
        crud = CRUD().delete(pk)
        return Response({
            'page': 1,
            'page_size': 1,
            'has_more': False,
            'results': crud,
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def detail(request, pk, format=None):
        """
            Retrieve single task record (with all it's related child-tables).
        """
        record = CRUD().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
        if record:
            serialized = TaskO2ORecord(record[0])
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': serialized.data,
            })
        
class CommentMethods():
    @staticmethod
    def create(request, format=None):
        """
            Create single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = Comments().create(serializer.validated_data)
            # attempt to return the created comment record consolidated through serializer
            if result:
                try:
                    rec = result[0] if isinstance(result, (list, tuple)) else result
                    serialized = TaskO2ORecord(rec)
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': serialized.data,
                    }, status=status.HTTP_201_CREATED)
                except Exception:
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': result,
                    }, status=status.HTTP_201_CREATED)
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': result,
            }, status=status.HTTP_201_CREATED) # @todo: make 200/201(?) response WITH the created comment returned
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            Edit single task record (with all it's related child-tables).
        """
        serializer = TaskO2ORecord(data=request.data)
        if serializer.is_valid():
            result = Comments().update(serializer.validated_data)
            # attempt to return the updated comment consolidated through serializer
            if result:
                try:
                    rec = result[0] if isinstance(result, (list, tuple)) else result
                    serialized = TaskO2ORecord(rec)
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': serialized.data,
                    }, status=status.HTTP_200_OK)
                except Exception:
                    return Response({
                        'page': 1,
                        'page_size': 1,
                        'has_more': False,
                        'results': result,
                    }, status=status.HTTP_200_OK)
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': result,
            }, status=status.HTTP_200_OK) # @todo: make 200 response with the updated comment
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def delete(request, pk, format=None):
        """
            Delete single task record (with all it's related child-tables).
        """
        crud = Comments().delete(pk)
        return Response({
            'page': 1,
            'page_size': 1,
            'has_more': False,
            'results': crud,
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def detail(request, pk, format=None):
        """
            Retrieve single task record (with all it's related child-tables).
        """
        record = Comments().read(['all'], {'tid': pk, 'tdelete_time': 'is NULL'})
        if record:
            serialized = TaskO2ORecord(record[0])
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': serialized.data,
            })
        
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
            # attempt to return created watcher consolidated through serializer
            if result:
                try:
                    rec = result[0] if isinstance(result, (list, tuple)) else result
                    serialized = TaskO2ORecord(rec)
                    return Response({
                            'page': 1,
                            'page_size': 1,
                            'has_more': False,
                            'results': serialized.data,
                        }, status=status.HTTP_201_CREATED)
                except Exception:
                    return Response({
                            'page': 1,
                            'page_size': 1,
                            'has_more': False,
                            'results': result,
                        }, status=status.HTTP_201_CREATED)
            return Response({
                    'page': 1,
                    'page_size': 1,
                    'has_more': False,
                    'results': result,
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def edit(request, format=None):
        """
            no updates allowed for watcher
        """
        pass
    
    @staticmethod
    def delete(request, pk, format=None):
        """
            Delete single watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': pk}, 'pk'):
            crud = Watchers().delete(pk)
            return Response({
                'page': 1,
                'page_size': 1,
                'has_more': False,
                'results': crud,
            }, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}) # @todo - fill in other options.

    @staticmethod
    def detail(request, pk, format=None):
        """
            Retrieve single watcher record.
            @current_user focussed
        """
        if crud.isValidId({'id': pk}, 'pk'):
            record = Watchers().read(['wid'], {'task_id': pk, 'watcher_id': 1, 'wdelete_time': 'is NULL', 'wlatest': 1})  # @todo replace watcher_id value with proper logic
            if record:
                serialized = TaskO2ORecord(record[0])
                return Response({
                    'page': 1,
                    'page_size': 1,
                    'has_more': False,
                    'results': serialized.data,
                })
        return Response({}) # @todo - fill in other options.
        