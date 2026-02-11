from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import tasks, settings, list, crud

urlpatterns = [
    path('all/', list.list),
    path('all/crud/', crud.crud),
    path('all/rlc/', list.list),
    path('all/rlc/crud/', crud.crud),
    path('all/m2m/', list.list),
    path('all/m2m/crud/', crud.crud),
    
    path('tasks/<str:type>/', tasks.task_list),
    path('tasks/crud/<int:id>/', tasks.task_crud),
    path('tasks/comments/<int:taskId>/', tasks.comments_list),
    path('tasks/comment/<int:id>/', tasks.comment_crud),
    path('tasks/watchers/<int:taskId>/', tasks.watchers_list),
    path('tasks/watcher/<int:taskId>/', tasks.watcher_crud),
    path('settings-general/', settings.retrieveAppSettings),
]

urlpatterns = format_suffix_patterns(urlpatterns)