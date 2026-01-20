from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import permission_classes
# from rest_framework.permissions import AllowAny
from django.conf import settings
from core.helpers import crud, misc
# Only Auth section Views defined here.

class ObtainTokenView(TokenObtainPairView):
    # permission_classes = [AllowAny]  # @todo: needed?
    
    def post(self, request, *args, **kwargs):
        """
        Override post to add access and refresh tokens as HTTP-only cookies.
        Tokens are set with HttpOnly, Secure, and SameSite flags for security.
        Wraps response in 'results' property for frontend compatibility.
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            secureFlag = False if settings.DEBUG else True  # sets secure=false flag if debug is on.

            # Set access token cookie
            if access_token:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=1 * 60 * 60,  # 1 hours (matches JWT_ACCESS_TOKEN_LIFETIME)
                    httponly=True,
                    secure=secureFlag,
                    samesite='Strict',
                    path='/'
                )
            
            # Set refresh token cookie
            if refresh_token:
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    max_age=24 * 60 * 60,  # 24 hours (matches JWT_REFRESH_TOKEN_LIFETIME)
                    httponly=True,
                    secure=secureFlag,
                    samesite='Strict',
                    path='/'
                )
            
            # Wrap response data in 'results' property
            formattedData = {
                'results': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            }
            response.data = formattedData
        
        return response


class RefreshTokenView(TokenRefreshView):
    # permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Override post to add refreshed access token as HTTP-only cookie.
        Token is set with HttpOnly, Secure, and SameSite flags for security.
        Wraps response in 'results' property for frontend compatibility.
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            
            secureFlag = False if settings.DEBUG else True  # sets secure=false flag if debug is on.
            
            # Set new access token cookie
            if access_token:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=1 * 60 * 60,  # 6 hours (matches JWT_ACCESS_TOKEN_LIFETIME)
                    httponly=True,
                    secure=secureFlag,
                    samesite='Strict',
                    path='/'
                )
            
            formattedData = {
                'results': {
                    'access_token': access_token,
                }
            }
            response.data = formattedData
        
        return response

