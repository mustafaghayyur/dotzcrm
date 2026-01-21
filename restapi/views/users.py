from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from restapi.lib.helpers import getUserFromJwtCookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from core.helpers import crud
from users.models import User

# @todo: revisit these account endpoints and get accounts section working
@api_view(['PUT'])
def changeUserPassword(request, format=None):
    """
        API Endpoint to update authenticated user's password to the newly submitted password.
        - Retrieves and validates access_token from HTTP cookies
        - Changes password to submitted 'newPassword' value
        - Generates new JWT tokens and updates cookies
        - Returns confirmation with new tokens
    """
    try:
        # Extract and validate JWT token from cookies
        user = getUserFromJwtCookie(request)
        
        # Get new password from request data
        new_password = request.data.get('newPassword') or request.POST.get('newPassword')
        
        if not new_password:
            return Response(crud.generateError("Missing 'newPassword' in request.", "Validation error."), status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password strength
        try:
            validate_password(new_password, user)
        except DjangoValidationError as e:
            return Response(crud.generateError(e.messages, "Password validation failed."), status=status.HTTP_400_BAD_REQUEST)
        
        # Update user's password
        user.set_password(new_password)
        user.save()
        
        # Generate new JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        # Add custom claims
        refresh['user_id'] = user.id
        refresh['user_name'] = user.username
        access['user_id'] = user.id
        access['user_name'] = user.username
        
        # Create response with new tokens in JSON
        context = {
            'message': 'Password changed successfully. Access tokens updated.',
            'access_token': str(access),
            'refresh_token': str(refresh),
        }
        response = Response(crud.generateResponse(context))
        
        # Set tokens in cookies
        response.set_cookie(
            key='access_token',
            value=str(access),
            max_age=6 * 60 * 60,
            httponly=True,
            secure=True,
            samesite='Strict',
            path='/'
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            max_age=24 * 60 * 60,
            httponly=True,
            secure=True,
            samesite='Strict',
            path='/'
        )
        
        return response
        
    except InvalidToken as e:
        return Response(crud.generateError(str(e), "Authentication failed."), status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(crud.generateError(e, "Errors have occurred."), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def resetUserPassword(request, format=None):
    """
        API Endpoint to update unauthenticated user's password to the newly submitted password.
        - Does NOT require a valid JWT token
        - Takes username/email and new password
        - Optionally generates JWT tokens for auto-login
        - Returns confirmation with optional tokens
    """    
    try:
        # Get username/email and new password from request data
        username_or_email = request.data.get('username') or request.data.get('email') or request.POST.get('username') or request.POST.get('email')
        new_password = request.data.get('newPassword') or request.POST.get('newPassword')
        
        if not username_or_email:
            return Response(crud.generateError("Missing 'username' or 'email' in request.", "Validation error."), status=status.HTTP_400_BAD_REQUEST)
        
        if not new_password:
            return Response(crud.generateError("Missing 'newPassword' in request.", "Validation error."), status=status.HTTP_400_BAD_REQUEST)
        
        # Find user by username or email
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return Response(crud.generateError("User not found.", "User lookup failed."), status=status.HTTP_404_NOT_FOUND)
        
        # Validate password strength
        try:
            validate_password(new_password, user)
        except DjangoValidationError as e:
            return Response(crud.generateError(e.messages, "Password validation failed."), status=status.HTTP_400_BAD_REQUEST)
        
        # Update user's password
        user.set_password(new_password)
        user.save()
        
        # Check if user requested auto-login (optional)
        auto_login = request.data.get('autoLogin') or request.POST.get('autoLogin')
        
        context_data = {
            'message': 'Password reset successfully.',
        }
        
        # Generate new JWT tokens if auto-login requested
        if auto_login:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            
            # Add custom claims
            refresh['user_id'] = user.id
            refresh['user_name'] = user.username
            access['user_id'] = user.id
            access['user_name'] = user.username
            
            context_data['access_token'] = str(access)
            context_data['refresh_token'] = str(refresh)
        
        context = {'results': context_data}
        response = Response(crud.generateResponse(context))
        
        # Set tokens in cookies if auto-login was requested
        if auto_login:
            response.set_cookie(
                key='access_token',
                value=str(access),
                max_age=6 * 60 * 60,
                httponly=True,
                secure=True,
                samesite='Strict',
                path='/'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                max_age=24 * 60 * 60,
                httponly=True,
                secure=True,
                samesite='Strict',
                path='/'
            )
        
        return response
        
    except Exception as e:
        return Response(crud.generateError(e, "Errors have occurred."), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def retrieveSettings(request):
    """
    Retrieve API settings based on authentication status.
    - Accessible to both authenticated and anonymous users
    - Returns userSettings if valid JWT token is present
    - Returns anonymousSettings if no valid token or anonymous user
    """
    try:
        # Try to authenticate user from JWT cookie
        user = getUserFromJwtCookie(request)
        
        # User is authenticated - return user settings
        userSettings = {
            'is_authenticated': True,
            'username': user.username,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_leader': user.is_leader,
            'authenticated': True,
            'allowed_routes': {
                'api': {
                    'auth': {
                        'login': '/accounts/rest/token/',
                        'refresh': '/accounts/rest/token/refresh/',
                        'settings': '/accounts/rest/settings/',
                        'logout': '/accounts/rest/logout/',
                        'change_password': '/accounts/rest/change-password/',
                    },
                    'tasks': {
                        'crud': '/rest/tasks/crud/{input1}/',
                        'list': '/rest/tasks/{input1}/',
                        'comments_crud': '/rest/tasks/comment/{input1}/',
                        'comments_list': '/rest/tasks/comments/',
                        'watchers_crud': '/rest/tasks/watcher/{input1}/',
                        'watchers_list': '/rest/tasks/watchers/{input1}/',
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
        
    except (InvalidToken, Exception):
        # User is not authenticated or token is invalid - return anonymous settings
        return Response(crud.generateResponse({
            'is_authenticated': False,
            'allowed_routes': {
                'api': {
                    'auth': {
                        'login': '/accounts/rest/token/',
                        'refresh': '/accounts/rest/token/refresh/',
                        'settings': '/accounts/rest/settings/'
                    },
                },
                'ui': {
                    'auth': {
                        'login': '/accounts/login/',
                        'register': '/accounts/register/'
                    },
                }
            }
        }))

