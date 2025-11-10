from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Task


class TasksEditForm(forms.Form):
    User = get_user_model()

    description = forms.CharField(max_length=255, empty_value="What's your task?")
    status = forms.CharField(max_length=20)
    visibility = forms.CharField(max_length=20)

    details = forms.CharField(widget=forms.Textarea, empty_value="Enter long description here...")

    deadline = forms.DateTimeField()
    parent = forms.ModelChoiceField(queryset=Task.rawobjects)

    assignor = forms.ModelChoiceField(queryset=User.objects, empty_label="Select One")
    assignee = forms.ModelChoiceField(queryset=User.objects, empty_label="Select One")

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
