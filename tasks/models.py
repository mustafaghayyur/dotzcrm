from django.db import models
from django.conf import settings as sysconf

from .drm.querysets import *  # import our QuerySets
from users.models import *


### Tasks Mapper Models ###

# The main task table
class Task(models.Model):
    """
        O2O Model.
    """
    description = models.CharField(max_length=2000)
    creator = models.ForeignKey(
        sysconf.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = TaskQuerySet.as_manager()


class Details(models.Model):
    """
        O2O Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    details = models.TextField()  # look into > difflib SequenceMatcher.quick_ratio()
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = DetailQuerySet.as_manager()


class Deadline(models.Model):
    """
        O2O Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = DeadlineQuerySet.as_manager()


class Status(models.Model):
    """
        O2O Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # enum of ['assigned' | 'viewed' | 'queued' | 'started' | 'onhold' | 'abandoned' | 'reassigned' | 'awaitingfeedback' | 'completed' | 'failed']
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = StatusQuerySet.as_manager()


class Visibility(models.Model):
    """
        O2O Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20)  # enum of ['private' | 'assigned' | 'organization' | 'stakeholders']
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = VisibilityQuerySet.as_manager()

# The table to manage assignor/assignee for each task
class Assignment(models.Model):
    """
        O2O Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignor = models.ForeignKey(
        sysconf.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
        related_name='asasignor_user'
    )
    assignee = models.ForeignKey(
        sysconf.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
        related_name='asasignee_user'
    )
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = AssignmentQuerySet.as_manager()


class Watcher(models.Model):
    """
        M2M Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    watcher = models.ForeignKey(
        sysconf.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = WatcherQuerySet.as_manager()


class Comment(models.Model):
    """
        RLC Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.CharField(max_length=6000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parent_comment')
    creator_user = models.ForeignKey(sysconf.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = CommentQuerySet.as_manager()



### WorkSpace Mapper Models ###


class WorkSpace(models.Model):
    """
        O2O Model.
    """
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=6000)
    type = models.CharField(max_length=30)  # enum of ['private' | 'open']
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)


class WorkSpaceDepartment(models.Model):
    """
        M2M Model.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class WorkSpaceUser(models.Model):
    """
        M2M Model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class WorkSpaceTasks(models.Model):
    """
        M2M Model.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

