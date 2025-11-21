from django.shortcuts import render
from django.contrib.auth import views as auth_views

# Only Auth section Views defined here.


class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    next_page = 'tasks_index'
    authentication_form = 'AuthenticationForm'
    extra_context = None


class LogoutView(auth_views.LogoutView):
    next_page = 'login'
    template_name = 'logout.html'
    extra_context = None
        
class PWChangeView(auth_views.PasswordChangeView):
    def __init__(self, kwargs):
        pass

class PWChangeViewComplete(auth_views.PasswordChangeDoneView):
    def __init__(self, kwargs):
        pass
        
class PWResetView(auth_views.PasswordResetView):
    def __init__(self, kwargs):
        pass
        
class PWResetViewComplete(auth_views.PasswordResetDoneView):
    def __init__(self, kwargs):
        pass
        
class ResetTokenView(auth_views.PasswordResetConfirmView):
    def __init__(self, kwargs):
        pass
        
class ResetView(auth_views.PasswordResetCompleteView):
    def __init__(self, kwargs):
        pass
        
