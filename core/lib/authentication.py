"""
    This class extends RestFramework's original JWTAuthentication.
    We introduce check for HTTPOnly cookies carrying access_token and refresh_token.
    Falls back to session authentication and Authorization header if cookies not present.
    Adds custom user claims to JWT tokens.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.settings import api_settings
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
from typing import Optional, Tuple
from rest_framework.request import Request
from core.helpers import misc

User = get_user_model()


class CustomUserToken(Token):
    """
    Custom token class that adds user details to the token payload.
    Includes: user_id, username, email, first_name, last_name, is_active, user_level, user_settings
    """
    token_type = 'access'
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME  # Will use default from settings
    
    @classmethod
    def for_user(cls, user):
        """
        Create token for user with custom claims.
        """
        misc.log(lifetime, 'inisde CustomUserToken.for_user(), checking lifetime value')
        token = super().for_user(user)
        
        # Add custom user claims
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_active'] = user.is_active
        token['user_level'] = user.user_level
        
        # Add user_settings if it exists and is not too long
        misc.log(token, 'token before user_settings')
        user_settings = getattr(user, 'user_settings', '')
        if user_settings and len(str(user_settings)) <= 750:
            token['user_settings'] = user_settings

        misc.log(token, 'token after user_settings')
        
        return token


class JWTAuthenticationCookies(JWTAuthentication):
    """
    Custom JWT authentication that extracts tokens from HTTP-only cookies.
    Falls back to standard Authorization header if cookie not present.
    Also supports session authentication as final fallback.
    Includes custom user claims in token validation.
    """
    
    def authenticate(self, request: Request) -> Optional[Tuple]:
        """
        Extract JWT token from 'access_token' cookie first, then fall back to
        Authorization header, then session authentication.
        """
        # Try to get token from cookie first
        cookie_name = 'access_token'
        raw_token = request.COOKIES.get(cookie_name)
        
        # If no cookie, try Authorization header (standard JWT Bearer)
        if raw_token is None:
            auth_header = self.get_header(request)
            if auth_header is not None:
                raw_token = self.get_raw_token(auth_header)
        
        # If still no token, try session authentication
        if raw_token is None:
            try:
                session_auth = SessionAuthentication()
                return session_auth.authenticate(request)
            except Exception:
                return None
        
        # Validate the token and return the user
        try:
            validated_token = self.get_validated_token(raw_token)
            misc.log(validated_token, 'Checking to see validated token for user.')
            user = self.get_user(validated_token)
            return user, validated_token
        except InvalidToken as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

