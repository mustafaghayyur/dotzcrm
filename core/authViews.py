from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

# Only Auth section Views defined here.


class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    next_page = 'tasks_index'
    authentication_form = AuthenticationForm
    extra_context = None


class LogoutView(auth_views.LogoutView):
    next_page = 'login'
    template_name = 'logged_out.html'
    extra_context = None
        
class PWChangeView(auth_views.PasswordChangeView):
    template_name = 'password_change_form.html'


class PWChangeViewComplete(auth_views.PasswordChangeDoneView):
    template_name = 'password_change_done.html'

        
class PWResetView(auth_views.PasswordResetView):
    template_name = 'password_reset_form.html'

        
class PWResetViewComplete(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_email.html'

        
class ResetTokenView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

        
class ResetView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_done.html'

        
