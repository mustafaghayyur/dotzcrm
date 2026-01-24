from django.urls import path
from . import views
from restapi.views import auth, users

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('register/', views.register, name='register'),
    path('password_change/', views.changePassword, name = 'password_change'),
    path('password_change/done/', views.changePasswordDone, name = 'password_change_done'),
    path('password_reset/', views.passwordReset1, name = 'password_reset'),
    path('password_reset/done/', views.passwordReset2, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.passwordReset3, name = 'password_reset_confirm'),
    path('reset/done/', views.passwordReset4, name = 'password_reset_complete'),

    # API Endpoints partaining to accounts
    path('rest/token/', auth.ObtainTokenView.as_view()),
    path('rest/token/refresh/', auth.RefreshTokenView.as_view()),
    
    # API endpoints partaining to user records
    path('rest/password/change', users.changeUserPassword),
    path('rest/password/reset', users.changeUserPassword),
]
