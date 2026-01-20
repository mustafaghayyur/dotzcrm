#from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from core.lib.authentication import JWTAuthentication


def getUserFromJwtCookie(request):
    """
    Extract and validate JWT token from cookies and return authenticated user.
    
    Returns:
        User object if token is valid, raises InvalidToken if not valid or missing.
    """
    access_token = request.COOKIES.get('access_token')
    
    if not access_token:
        raise InvalidToken('No access token found in cookies.')
    
    try:
        jwt_auth = JWTAuthentication()
        # Create a fake request object for JWT authentication
        class FakeRequest:
            def __init__(self, token):
                self.META = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        
        fake_request = FakeRequest(access_token)
        user_auth = jwt_auth.authenticate(fake_request)
        
        if user_auth is None:
            raise InvalidToken('Invalid token.')
        
        user, _ = user_auth
        return user
    except (InvalidToken, TokenError) as e:
        raise InvalidToken(f'Token validation failed: {str(e)}')
