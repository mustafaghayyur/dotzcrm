from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import tasks

urlpatterns = [
    path('tasks/<str:type>', tasks.task_list),
    path('tasks/crud/<int:pk>/', tasks.task_crud),
]

urlpatterns = format_suffix_patterns(urlpatterns)