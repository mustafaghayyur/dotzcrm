from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.helpers import pagination, crud

@api_view(['POST'])
def list(request, type, format=None):
    """
        List all records based on paramerters in POST request's body.
    """
    postData = {}
    postData['params'] = request.data
    postData['current_user'] + request.user

    """
        postData could look like:
        {
            tbl: 'tata',
            mapper: 'Tasks',
            selectors: ['tata_id', 'tata_update_time', 'visibility'],
            conditions: {
                'tata_delete_time': 'is null',
                'deadline': '2026-03-26 09:09:00',
                'visibility': 'workspaces',
                'wota_workspace_id': 21 
            },
            joins: {
                'inner|wota_task_id': 'tata_id'
            },
            order: [
                {
                    'tbl': 'tata',
                    'col': 'description',
                    'order': 'desc'
                }
            ],
            limit: ['all']
        }
    """

    try:
        pgntn = pagination.assembleParamsForView(postData['params']['limit'])
        paginated_limit = [str(pgntn['offset']), str(pgntn['page_size'])]
        serializer = loadedMapper.serializer(tblKey]

        records = loadedModel.objects.fetch(**postData['params'])
        serialized = serializer(records, many=True)
        hasMore = pagination.determineHasMore(records, pgntn['page_size'])
        return Response(crud.generateResponse(serialized.data, pgntn['page'], pgntn['page_size'], hasMore))
    
    except ValidationError as e:
        return Response(crud.generateError(e, "Validation errors have been caught."), status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(crud.generateError(e, "Some errors have occured."), status=status.HTTP_400_BAD_REQUEST)


