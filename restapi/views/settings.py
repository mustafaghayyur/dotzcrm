"""
    Any nodes sendiing back settings/confirgurations can be defined here.
"""
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from restapi.lib.helpers import *
from core.helpers import crud, misc

@api_view(['GET'])
@permission_classes([AllowAny])
def retrieveAppSettings(request):
    """
    Retrieve API settings based on authentication status.
    - Accessible to both authenticated and anonymous users
    - Returns userSettings if valid JWT token is present
    - Returns anonymousSettings if no valid token or anonymous user
    """
    try:
        # Try to authenticate user from JWT cookie
        user = isUserAuthenticated(request)

        # User is authenticated - return user settings
        userSettings = {
            'is_authenticated': True,
            'username': user.username,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'user_level': user.user_level,
            'allowed_routes': {
                'api': {
                    'auth': {
                        'login': '/accounts/rest/token/',
                        'refresh': '/accounts/rest/token/refresh/',
                        'settings': '/rest/settings-general/',
                        'logout': '/accounts/rest/logout/',
                        'change_password': '/accounts/rest/change-password/',
                    },
                    'tasks': {
                        'crud': '/rest/tasks/crud/{input1}/',
                        'list': '/rest/tasks/{input1}/',
                        'comments_crud': '/rest/tasks/comment/{input1}/',
                        'comments_list': '/rest/tasks/comments/{input1}/',
                        'watchers_crud': '/rest/tasks/watcher/{input1}/',
                        'watchers_list': '/rest/tasks/watchers/{input1}/',
                    },
                    'terminal': {
                        'crud': '/rest/all/crud/',
                        'list': '/rest/all/',
                    },
                },
                'ui': {
                    'auth': {
                        'login': '/accounts/login/',
                        'register': '/accounts/register/',
                    },
                    'apps': {
                        'tasks': '/tasks/',
                    }
                }
            }
        }
        
        return Response(crud.generateResponse(userSettings))
        
    except (InvalidToken, Exception) as e:        
        # User is not authenticated or token is invalid - return anonymous settings
        return Response(crud.generateResponse({
            'messages': "Authentication failed. If this seems to be an error, please contact support.",
            'errprs': str(e),  # @todo make ui notification for this error msg, should be non-invasive
            'is_authenticated': False,
            'allowed_routes': {
                'api': {
                    'auth': {
                        'login': '/accounts/rest/token/',
                        'refresh': '/accounts/rest/token/refresh/',
                        'settings': '/rest/settings-general/'
                    },
                },
                'ui': {
                    'auth': {
                        'login': '/accounts/login/',
                        'register': '/accounts/register/'
                    },
                    'apps': {
                        'tasks': '/tasks/',
                    }
                }
            }
        }))

