"""
    Holds SimpleJWT Classes overwrite for token authentication system.
    We introduce check for HTTPOnly cookies carrying access_token and refresh_token.
    Adds custom user claims to JWT tokens during token generation.
    Removes database queries for token validation, instead using token claims' data for artificial user model generation.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
# from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from typing import Optional, Tuple
from rest_framework.request import Request
from users.models import User

class CustomIsAuthenticated(IsAuthenticated):
    """
    Custom permission class that verifies user is authenticated via JWT tokens.
    Works with JWTAuthenticationCookies authentication backend.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        is_auth = bool(request.user and request.user.is_authenticated)
        return is_auth


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that adds custom user claims to tokens.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add your custom claims here
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_active'] = user.is_active
        token['user_level'] = user.user_level        
        return token


class JWTAuthenticationCookies(JWTAuthentication):
    """
    Custom JWT authentication that extracts tokens from HTTP-only cookies.
    Falls back to standard Authorization header if cookie not present.
    Includes custom user claims in token validation.
    User Model is artificially created with token claims' data.
    """
    
    def authenticate(self, request: Request) -> Optional[Tuple]:
        """
        Extract JWT token from 'access_token' cookie first, then fall back to
        Authorization header.
        """
        # Try to get token from cookie first
        cookie_name = 'access_token'
        raw_token = request.COOKIES.get(cookie_name)
        
        # If no cookie, try Authorization header (standard JWT Bearer)
        if raw_token is None:
            auth_header = self.get_header(request)
            if auth_header is not None:
                raw_token = self.get_raw_token(auth_header)
        
        if raw_token is None:
            return None, None
        
        try:  # Validate the token and return the user
            validated_token = self.get_validated_token(raw_token)
            
            # Create a user instance from token claims without database query
            dictionary = {
                'id': validated_token['user_id'],
                'username': validated_token['username'],
                'email': validated_token['email'],
                'first_name': validated_token['first_name'],
                'last_name': validated_token['last_name'],
                'is_active': validated_token['is_active'],
                'user_level': validated_token['user_level'],
            }
            
            # Create User instance from dictionary
            user = User(**dictionary)
            return user, validated_token
        except InvalidToken as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Exception raised during Authentication: {str(e)}')
