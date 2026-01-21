"""
    This class extends RestFramework's original JWTAuthentication.
    We introduce check for HTTPOnly cookies carrying access_token and refresh_token.
    Falls back to session authentication and Authorization header if cookies not present.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
from core.helpers import misc

User = get_user_model()


class JWTAuthenticationCookies(JWTAuthentication):
    """
    Custom JWT authentication that extracts tokens from HTTP-only cookies.
    Falls back to standard Authorization header if cookie not present.
    Also supports session authentication as final fallback.
    """
    
    def authenticate(self, request: Request) -> Optional[tuple[AuthUser, Token]]:
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
            user = self.get_user(validated_token)
            return user, validated_token
        except InvalidToken as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

