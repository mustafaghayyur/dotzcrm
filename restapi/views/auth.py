from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from core.helpers import crud
from core.lib.authentication import CustomTokenObtainPairSerializer
from restapi.lib.helpers import *


class ObtainTokenView(TokenObtainPairView):
    """
        Token issuance view.
        Uses custom serializer to include additional user claims in the token.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Override post to add access and refresh tokens as HTTP-only cookies.
        Tokens are set with HttpOnly, Secure, and SameSite flags for security.
        Wraps response in 'results' property for frontend compatibility.
        """
        try:
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
                        max_age=6 * 60 * 60,  # 6 hours (matches JWT_ACCESS_TOKEN_LIFETIME)
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
        except Exception as e:
            return Response(crud.generateError(e, "Token generation failure."), status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(TokenRefreshView):
    """
        Token Refresh view.
        Uses custom token to include additional user claims in the refreshed access token.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Override post to add refreshed access token as HTTP-only cookie.
        Token is set with HttpOnly, Secure, and SameSite flags for security.
        Wraps response in 'results' property for frontend compatibility.
        """
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                access_token = response.data.get('access')
                
                secureFlag = False if settings.DEBUG else True  # sets secure=false flag if debug is on.
                
                # Set new access token cookie
                if access_token:
                    response.set_cookie(
                        key='access_token',
                        value=access_token,
                        max_age=6 * 60 * 60,  # 6 hours (matches JWT_ACCESS_TOKEN_LIFETIME)
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
        except Exception as e:
            return Response(crud.generateError(e, "Token refresh failure."), status=status.HTTP_400_BAD_REQUEST)
            
            return response
        except Exception as e:
            return Response(crud.generateError(e, "Token refresh failiure."), status=status.HTTP_400_BAD_REQUEST)


