from django.db import models
from django.conf import settings as sysconf

# import our QuerySets:
from .drm.querysets import *


# The main task table
class Task(models.Model):
    description = models.CharField(max_length=255)
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
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    details = models.TextField()  # look into > difflib SequenceMatcher.quick_ratio()
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = DetailQuerySet.as_manager()


class Deadline(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = DeadlineQuerySet.as_manager()

class Status(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # enum of ['assigned' | 'viewed' | 'queued' | 'started' | 'onhold' | 'abandoned' | 'reassigned' | 'awaitingfeedback' | 'completed' | 'failed']
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = StatusQuerySet.as_manager()

class Visibility(models.Model):
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

# NOTE: Comments model must ALWAYS be named Comment
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.CharField(max_length=6000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(sysconf.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = CommentQuerySet.as_manager()


class EditLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(sysconf.AUTH_USER_MODEL, on_delete=models.CASCADE)
    changed_cols = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

# @todo - link tasks with tickets
# This model allows tickets to be mentioned in tasks
#class TaskTicketAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(auto_now_add=True)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with Customers
# This model allows customers to be mentioned in tasks
#class TaskCustomerAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(auto_now_add=True)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with documents
# This model allows documents to be mentioned in tasks
#class TaskCustomerAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(auto_now_add=True)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.
