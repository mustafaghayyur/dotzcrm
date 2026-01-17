from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

@csrf_exempt
@api_view(['GET'])
def index(request, format=None):
    response = {
        'messages': 'Welcome to the REST API system of Dotz CRM + PM Software',
    }
    return Response(crud.generateResponse(response))
