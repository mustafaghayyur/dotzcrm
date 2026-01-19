from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

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


