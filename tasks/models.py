from django.db import models
from django.conf import settings
from django.utils import timezone

from . import QuerySets


# The main task table
class Task(models.Model):
    description = models.CharField(max_length=255)
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TasksQuerySet.as_manager()


class TaskDetails(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(null=True, blank=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TaskDetailQuerySet.as_manager()


class TaskDeadline(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(default=timezone.now)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TaskDeadlineQuerySet.as_manager()

class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # enum of ['assigned' | 'viewed' | 'queued' | 'started' | 'onhold' | 'abandoned' | 'reassigned' | 'awaitingfeedback' | 'completed' | 'failed']
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(default=timezone.now)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TaskStatusQuerySet.as_manager()

class TaskVisibility(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20)  # enum of ['private' | 'assigned' | 'organization' | 'stakeholders']
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(default=timezone.now)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TaskVisibilityQuerySet.as_manager()

class TaskWatcher(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    watcher_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(default=timezone.now)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TaskWatacherQuerySet.as_manager()


# The table to manage assignor/assignee for each task
class TaskUserAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
        related_name='asasignor_user'
    )
    assignee_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
        related_name='asasignee_user'
    )

    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(default=timezone.now)
    delete_time = models.DateTimeField(null=True, blank=True)

    rawobjects = QuerySets.TaskAssignmentQuerySet.as_manager()


# @todo - link tasks with tickets
# This model allows tickets to be mentioned in tasks
#class TaskTicketAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(default=timezone.now)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with Customers
# This model allows customers to be mentioned in tasks
#class TaskCustomerAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(default=timezone.now)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with documents
# This model allows documents to be mentioned in tasks
#class TaskCustomerAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(default=timezone.now)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with comments
# This model allows documents to be mentioned in tasks
#class TaskCommentAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(default=timezone.now)
#    delete_time = models.DateTimeField(null=True, blank=True)
    # note: updates are banned on this table.
    # application level control to be implemented.



#################################################################
## ADDING MYiSAM Engine to some tables...
#################################################################

# run:
#  > python manage.py makemigrations --empty <app_name>  # empty option makes an empty Migration file that you can fill in manually
#
# Edit the generated migration file: (e.g., 0002_alter_my_table_engine.py)
# and add a RunSQL operation within the operations list. 
# Replace myapp_mytable with your actual table name:
# from django.db import migrations, models
#
#     class Migration(migrations.Migration):
#
#         dependencies = [
#             ('myapp', '0001_initial'), # Replace with your app's initial migration
#         ]
#
#         operations = [
#             migrations.RunSQL(
#                 "ALTER TABLE myapp_mytable ENGINE=MyISAM;",
#                 reverse_sql="ALTER TABLE myapp_mytable ENGINE=InnoDB;" # Or your desired default
#             ),
#         ]
#
# Then apply the  migration
#  > python manage.py migrate
