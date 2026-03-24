from django.db import models
from django.conf import settings as sysconf

from ..drm.querysets import *
from users.models import User, Department


### WorkSpace Models ###

class WorkSpace(models.Model):
    """
        O2O Model.
    """
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=6000)
    type = models.CharField(max_length=30)  # enum of ['private' | 'open']
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = WorkSpaceQuerySet.as_manager()


class WorkSpaceCycle(models.Model):
    """
        O2O Model.
    """
    amount = models.IntegerField(null=False, blank=False)
    interval = models.CharField(null=False, blank=False, max_length=50)  # enum of [day | week | month | year]
    type = models.CharField(null=False, blank=False, max_length=50)  # enum of [reset | continuance]
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]

    objects = TaskCTQuerySet.as_manager()

class WorkSpaceDepartment(models.Model):
    """
        M2M Model.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]

    objects = WorkSpaceM2MQuerySet.as_manager()


class WorkSpaceUser(models.Model):
    """
        M2M Model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]

    objects = WorkSpaceM2MQuerySet.as_manager()