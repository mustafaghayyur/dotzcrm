from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name = 'task_index'),
    path('details/<int:id>/', viewTaskDetails, name = 'task_info'),
    path('edit/<int:id>/', editTask, name = 'task_edit'),
    path('edit/', editTask, name = 'task_create'),
]
