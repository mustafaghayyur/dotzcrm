from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legal_first_name = models.CharField(max_length=150, blank=True, null=True)
    legal_last_name = models.CharField(max_length=150, blank=True, null=True)
    office_phone = models.CharField(max_length=15, blank=True, null=True)
    office_ext = models.CharField(max_length=10, blank=True, null=True)
    cell_phone = models.CharField(max_length=15, blank=True, null=True)
    home_phone = models.CharField(max_length=15, blank=True, null=True)
    office_location = models.CharField(max_length=150, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)
    # Add other fields here

    def __str__(self):
        return self.user.username

class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    settings = models.JSONField(
        null=True, 
        blank=True
    )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class Department(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=1000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(null=True, blank=True)


class UserBelongsToDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class DepartmentHead(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

class UserReportsTo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    reports_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_to')
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)


