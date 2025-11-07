from django.contrib import admin

from .models import Task, TaskDetails, TaskDeadline, TaskStatus, TaskWatcher, TaskUserAssignment

admin.site.register(Task)
admin.site.register(TaskDetails)
admin.site.register(TaskDeadline)
admin.site.register(TaskStatus)
admin.site.register(TaskWatcher)
admin.site.register(TaskUserAssignment)
