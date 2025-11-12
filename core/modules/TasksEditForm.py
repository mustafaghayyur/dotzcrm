from django import forms
from django.contrib.auth import get_user_model

from tasks.models import *


class TasksEditForm(forms.Form):
    User = get_user_model()

    task_id = forms.CharField(queryset=Task.rawobjects, widget=forms.HiddenInput())
    details_id = forms.CharField(queryset=Details.rawobjects, widget=forms.HiddenInput())
    deadline_id = forms.CharField(queryset=Deadline.rawobjects, widget=forms.HiddenInput())
    status_id = forms.CharField(queryset=Status.rawobjects, widget=forms.HiddenInput())
    visibility_id = forms.CharField(queryset=Visibility.rawobjects, widget=forms.HiddenInput())
    watcher_id = forms.CharField(queryset=Watcher.rawobjects, widget=forms.HiddenInput())
    assignment_id = forms.CharField(queryset=Assignment.rawobjects, widget=forms.HiddenInput())
    
    description = forms.CharField(max_length=255, empty_value="What's your task?")
    status = forms.CharField(max_length=20)
    visibility = forms.CharField(max_length=20)

    details = forms.CharField(widget=forms.Textarea, empty_value="Enter long description here...")

    deadline = forms.DateTimeField()
    parent = forms.ModelChoiceField(queryset=Task.rawobjects)

    assignor = forms.ModelChoiceField(queryset=User.objects, empty_label="Select One")
    assignee = forms.ModelChoiceField(queryset=User.objects, empty_label="Select One")

    