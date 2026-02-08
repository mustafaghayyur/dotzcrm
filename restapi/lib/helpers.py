"""
    This file will hold functions necessary for api views operations.
"""
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from core.authorization.authentication import JWTAuthenticationCookies

def isUserAuthenticated(request):
    """
        Confirms user has a valid token.
        Token carries all non-sensitive user data.
        Returns User model object.
    """
    try:
        jwt_auth = JWTAuthenticationCookies()
        user, tokenData = jwt_auth.authenticate(request)
        
        if user is None or tokenData is None:
            raise InvalidToken('Token missing essential data. Cannot proceed.')
        return user
    except (InvalidToken, TokenError) as e:
        raise InvalidToken(f'Token validation failed: {str(e)}')
