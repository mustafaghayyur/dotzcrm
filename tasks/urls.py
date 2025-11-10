from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name = 'tasks_index'),
    path('details/<int:pk>/', views.TaskDetailView.as_view(), name = 'task_info'),
    path('edit/', views.TaskEditView.as_view(), name = 'task_create'),
]