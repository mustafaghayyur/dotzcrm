from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views, authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.dotzSettings import dotzSettings

# Only Auth section Views defined here.

@login_not_required
def register(request):
    """
        @todo: add proper welcome message for new users.
    """
    context = {
        'heading': 'Onboarding',
        'content': 'Please see our technical staff for gaining access to the system.',
        'loginRequired': 'false',
    }
    return render(request, 'core/generic.html', context)

class ObtainTokenView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        """
        Override post to add access and refresh tokens as HTTP-only cookies.
        Tokens are set with HttpOnly, Secure, and SameSite flags for security.
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            # Set access token cookie
            if access_token:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=1 * 60 * 60,  # 1 hours (matches JWT_ACCESS_TOKEN_LIFETIME)
                    httponly=True,
                    secure=True,
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
                    secure=True,
                    samesite='Strict',
                    path='/'
                )
        
        return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        Override post to add refreshed access token as HTTP-only cookie.
        Token is set with HttpOnly, Secure, and SameSite flags for security.
        """
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            
            # Set new access token cookie
            if access_token:
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    max_age=1 * 60 * 60,  # 1 hours (matches JWT_ACCESS_TOKEN_LIFETIME)
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    path='/'
                )
        
        return response


def login(request):
    """
        Handle user login with JWT token generation.
        GET: Display login form
    """
    context ={
        'loginRequired': 'false',
    }
    form = AuthenticationForm()
    context = {
        'next': 'task_index',
        'form': form,
    }
    return render(request, 'auth/login.html', context)

def logout(request):
    """
        Handle user logout by destroying JWT tokens.
        GET: Display logout confirmation page
    """
    context ={
        'loginRequired': 'false',
    }
    # Create response with logout page
    response = render(request, 'auth/logged_out.html', {'logged_out': 'tTrue'})
    
    # Delete authentication cookies
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')
    
    return response

"""
    Password Change is an authenticated-user's operation. Login required.
"""
def changePassword(request):
    context ={
        'loginRequired': 'true',
    }
    render(request, 'auth/password_change_form.html', context)

def changePasswordDone(request):
    context ={
        'loginRequired': 'true',
    }
    render(request, 'auth/password_change_done.html', context)

"""
    All Password-Reset views allow for non-authenticated users to reset password.
"""
def passwordReset1(request):
    context ={
        'loginRequired': 'false',
    }
    render(request, 'auth/password_reset_form.html', context)

def passwordReset2(request):
    context ={
        'loginRequired': 'false',
    }
    render(request, 'auth/password_reset_done.html', context)

def passwordReset3(request):
    context ={
        'loginRequired': 'false',
    }
    render(request, 'auth/password_reset_confirm.html', context)

def passwordReset4(request):
    context ={
        'loginRequired': 'false',
    }
    render(request, 'auth/password_reset_comlplete.html', context)

