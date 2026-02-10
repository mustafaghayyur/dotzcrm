from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.helpers import crud, misc
from restapi.lib.helpers import *
from tasks.drm.crud import *
from .helpers.tasksO2Os import OneToOnes


@api_view(['POST', 'PUT', 'GET', 'DELETE'])
def crud(request, id, format=None):
    """
        Tasks operations for individual Task O2O records.
    """
    method = request.method
    try:
        match method:
            case 'GET':
                return OneToOnes.detail(request, id, format)
            case 'POST':
                return OneToOnes.create(request, format)
            case 'PUT':
                return OneToOnes.edit(request, format)
            case 'DELETE': # @todo: add response message on success
                return OneToOnes.delete(request, id, format)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)
