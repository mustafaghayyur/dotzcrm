"""
    This file will hold functions necessary for api views operations.
"""
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from core.lib.authentication import JWTAuthenticationCookies
from core.helpers import misc

def isUserAuthenticated(request):
    """
        Confirms user has a valid token.
        Token carries all non-sensitive user data.
        Returns token [key] => value pairs.
    """
    try:
        jwt_auth = JWTAuthenticationCookies()
        _, tokenData = jwt_auth.authenticate(request)
        misc.log(tokenData, 'inspecting user_auth in helpers.isUserAuthenticated()')
        if tokenData is None:
            raise InvalidToken('Token missing essential data. Cannot proceed.')
        
        return tokenData
    except (InvalidToken, TokenError) as e:
        raise InvalidToken(f'Token validation failed: {str(e)}')
