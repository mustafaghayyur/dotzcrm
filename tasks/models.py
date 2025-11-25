from django.db import models
from django.conf import settings

# get our querysets (the core of our RDMS logic)
from core.Models.querysets.tasks import *


# The main task table
class Task(models.Model):
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = TasksQuerySet.as_manager()


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

class Watcher(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    watcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = WatacherQuerySet.as_manager()


# The table to manage assignor/assignee for each task
class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
        related_name='asasignor_user'
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
        related_name='asasignee_user'
    )
    latest = models.SmallIntegerField(default=1, db_default=1)  # enum of [1 | 2]
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = AssignmentQuerySet.as_manager()

# NOTE: Comments model must ALWAYS be named Comment
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.CharField(max_length=6000)
    parent = models.ForeignKey('self', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
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


# @todo - link tasks with comments
# This model allows documents to be mentioned in tasks
#class TaskCommentAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
#    create_time = models.DateTimeField(auto_now_add=True)
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
