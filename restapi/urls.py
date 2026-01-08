from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import tasks

urlpatterns = [
    path('tasks/<str:type>', tasks.task_list),
    path('tasks/crud/<int:pk>/', tasks.task_crud),
    path('tasks/watch/<int:pk>/', tasks.watcher_crud),
    path('tasks/comment/<int:pk>/', tasks.comment_crud),
    path('tasks/comments/', tasks.comments_list),
    path('tasks/watchers/', tasks.watchers_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)