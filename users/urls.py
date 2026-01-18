from django.urls import path
from . import views
from .views import *
from restapi.views.users import *

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('password_change/', views.changePassword, name = 'password_change'),
    path('password_change/done/', views.changePasswordDone, name = 'password_change_done'),
    path('password_reset/', views.passwordReset1, name = 'password_reset'),
    path('password_reset/done/', views.passwordReset2, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.passwordReset3, name = 'password_reset_confirm'),
    path('reset/done/', views.passwordReset4, name = 'password_reset_complete'),
    path('register/', views.register, name='register'),
    
    # API Endpoints pertaining to accounts
    path('token/', ObtainTokenView.as_view()),
    path('token/refresh/', RefreshTokenView.as_view()),
    path('password/change', changeUserPassword),
    path('password/reset', changeUserPassword),
]
