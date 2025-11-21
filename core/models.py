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
    # Add other fields here

    def __str__(self):
        return self.user.username

class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    settings = models.JSONField(
        null=True, 
        blank=True
    )
