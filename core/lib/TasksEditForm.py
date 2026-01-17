from django import forms
from django.contrib.auth import get_user_model

from tasks.models import *
from core.helpers import crud

class TasksEditForm(forms.Form):
    User = get_user_model()

    tid = forms.CharField(widget=forms.HiddenInput(), required=False)
    did = forms.CharField(widget=forms.HiddenInput(), required=False)
    lid = forms.CharField(widget=forms.HiddenInput(), required=False)
    sid = forms.CharField(widget=forms.HiddenInput(), required=False)
    vid = forms.CharField(widget=forms.HiddenInput(), required=False)
    aid = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    description = forms.CharField(max_length=255, empty_value="What's your task?")
    status = forms.CharField(max_length=20)
    visibility = forms.CharField(max_length=20)

    details = forms.CharField(widget=forms.Textarea, empty_value="Enter long description here...")

    deadline = forms.DateTimeField(required=False, widget=crud.DateTimeLocalInput())

    parent_id = forms.ModelChoiceField(queryset=Task.objects.all(), required=False)

    assignor_id = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select One")
    assignee_id = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select One")

    