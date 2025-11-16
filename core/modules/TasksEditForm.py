from django import forms
from django.contrib.auth import get_user_model

from tasks.models import *


class TasksEditForm(forms.Form):
    User = get_user_model()

    tid = forms.CharField(widget=forms.HiddenInput())
    did = forms.CharField(widget=forms.HiddenInput())
    lid = forms.CharField(widget=forms.HiddenInput())
    sid = forms.CharField(widget=forms.HiddenInput())
    vid = forms.CharField(widget=forms.HiddenInput())
    aid = forms.CharField(widget=forms.HiddenInput())
    
    description = forms.CharField(max_length=255, empty_value="What's your task?")
    status = forms.CharField(max_length=20)
    visibility = forms.CharField(max_length=20)

    details = forms.CharField(widget=forms.Textarea, empty_value="Enter long description here...")

    deadline = forms.DateTimeField()
    parent_id = forms.ModelChoiceField(queryset=Task.objects)

    assignor = forms.ModelChoiceField(queryset=User.objects, empty_label="Select One")
    assignee = forms.ModelChoiceField(queryset=User.objects, empty_label="Select One")

    