from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render
from django.contrib.auth import views as auth_views
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
    }
    return render(request, 'core/generic.html', context)

class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'
    next_page = 'task_index'
    authentication_form = AuthenticationForm
    extra_context = None


class LogoutView(auth_views.LogoutView):
    next_page = 'login'
    template_name = 'auth/logged_out.html'
    extra_context = None
        
class PWChangeView(auth_views.PasswordChangeView):
    template_name = 'auth/password_change_form.html'


class PWChangeViewComplete(auth_views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'

        
class PWResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset_form.html'

        
class PWResetViewComplete(auth_views.PasswordResetDoneView):
    template_name = 'auth/password_reset_email.html'

        
class ResetTokenView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'

        
class ResetView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password_reset_done.html'

        

