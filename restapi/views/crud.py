from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.helpers.crud import * 
from restapi.lib.crud import Operations

@api_view(['POST'])
def crud(request, format=None):
    method = request.method
    operations = Operations()
    try:
        match method:
            case 'POST':
                if request.data.get('reqType', None) == 'read':
                    return operations.read(request)
                if request.data.get('reqType', None) == 'delete':
                    return operations.delete(request)
                if request.data.get('reqType', None) == 'create':
                    return operations.create(request)
                if request.data.get('reqType', None) == 'update':
                    return operations.update(request)
            case _:
                return Response(status=status.HTTP_400_BAD_REQUEST)
    
    except ValidationError as e:
        return Response(generateError(e, "Error 840: Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(generateError(e, "Error 841: Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)




