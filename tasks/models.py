from django.db import models
from django.conf import settings


# The main task table
class Task(models.Model):
    description = models.CharField(max_length=255)
    creator_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20)  # enum of ['private' | 'assigned' | 'organization' | 'stakeholders']
    deadline = models.DateTimeField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    delete_time = models.DateTimeField()


class TaskDetails(models.Model):
    Task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    delete_time = models.DateTimeField()


class TaskDeadline(models.Model):
    Task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField()
    delete_time = models.DateTimeField()

class TaskStatus(models.Model):
    Task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # enum of ['assigned' | 'viewed' | 'queued' | 'started' | 'onhold' | 'abandoned' | 'reassigned' | 'awaitingfeedback' | 'completed' | 'failed']
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField()
    delete_time = models.DateTimeField()

class TaskWatcher(models.Model):
    Task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    watcher_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField()
    delete_time = models.DateTimeField()


# The table to manage assignor/assignee for each task
class TaskUserAssignment(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    assignor_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )
    assignee_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference the user model defined in settings
        on_delete=models.CASCADE,  # Define what happens when the related user is deleted
    )

    # note: updates are banned on this table.
    # application level control to be implemented.
    create_time = models.DateTimeField()
    delete_time = models.DateTimeField()


# @todo - link tasks with tickets
# This model allows tickets to be mentioned in tasks
#class TaskTicketAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#    linked_on = models.DateTimeField()
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with Customers
# This model allows customers to be mentioned in tasks
#class TaskCustomerAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
#    linked_on = models.DateTimeField()
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with documents
# This model allows documents to be mentioned in tasks
#class TaskCustomerAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
#    linked_on = models.DateTimeField()
    # note: updates are banned on this table.
    # application level control to be implemented.


# @todo - link tasks with comments
# This model allows documents to be mentioned in tasks
#class TaskCommentAssignment(models.Model):
#    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
#    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
#    linked_on = models.DateTimeField()
    # note: updates are banned on this table.
    # application level control to be implemented.



#################################################################
## ADDING MYiSAM Engine to some tables...
#################################################################

# run:
#  > python manage.py makemigrations --empty <app_name>
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
