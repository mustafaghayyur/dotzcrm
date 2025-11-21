from django.urls import path
from . import views
from .authViews import *

urlpatterns = [
    # specific url: path("change-password/", auth_views.PasswordChangeView.as_view()),

    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('password_change/', PWChangeView.as_view(), name = 'password_change'),
    path('password_change/done/', PWChangeViewComplete.as_view(), name = 'password_change_done'),
    path('password_reset/', PWResetView.as_view(), name = 'password_reset'),
    path('password_reset/done/', PWResetViewComplete.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetTokenView.as_view(), name = 'password_reset_confirm'),
    path('reset/done/', ResetView.as_view(), name = 'password_reset_complete'),
]
