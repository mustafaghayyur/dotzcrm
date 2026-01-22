from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import tasks

urlpatterns = [
    path('tasks/<str:type>/', tasks.task_list),
    path('tasks/crud/<int:id>/', tasks.task_crud),
    path('tasks/comments/<int:taskId>/', tasks.comments_list),
    path('tasks/comment/<int:id>/', tasks.comment_crud),
    path('tasks/watchers/<int:taskId>/', tasks.watchers_list),
    path('tasks/watcher/<int:taskId>/', tasks.watcher_crud),
]

urlpatterns = format_suffix_patterns(urlpatterns)