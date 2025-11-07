from django.db import models

class TasksQuerySet(models.QuerySet):
    def all_private_tasks(self, user_id):
        return self.raw('SELECT * FROM tasks_task AS t INNER JOIN tasks_taskdetails AS dtl ON t.id = dtl.foreign_key_column;', [user_id])

class TaskDetailQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskDeadlineQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskStatusQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])

class TaskVisibilityQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskWatacherQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])


class TaskAssignmentQuerySet(models.QuerySet):
    def by_author(self, user_id):
        return self.raw('SELECT * FROM tasks_task WHERE user_id = %s', [user_id])

