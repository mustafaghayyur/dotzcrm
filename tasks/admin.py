from django.contrib import admin

from .models import *

admin.site.register(Task)
admin.site.register(Details)
admin.site.register(Deadline)
admin.site.register(Status)
admin.site.register(Visibility)
admin.site.register(Watcher)
admin.site.register(Assignment)
