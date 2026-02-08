from django.contrib.auth import get_user_model
from django import forms

from core.lib.FormsParent import Forms
from tasks.models import *
from users.models import *
from tasks.drm.crud import Tasks
from tasks.drm.mapper_values import Status, Visibility
from users.drm.crud import Users
from core.helpers import crud

class TasksEditForm(Forms):
    """
    ParametersMatrix:
     - workspace: int - wordspace idfor tasks to list
     - 
    """
    def performSetup(self, matrix = {}):
        self.setParams(matrix)
        
        taskToFetch = Tasks.read(
            ['id', 'description'], 
            {
                'visibility': 'workspaces', 
                'wowo_id': self.getParam('workspace'),
            }
        )

        if taskToFetch:
            self.setQuerySet('tasks', taskToFetch)

        usersToFetch = Tasks.read(
            ['id', 'first_name', 'last_name'],
            {
                'kid': self.getParam('workspace'),
                'is_active': True
            }
        )

        if usersToFetch:
            self.setQuerySet('users', usersToFetch)

        # finally, set the queryset paremeter of each ModelChoiceField in this form:
        self.fields['parent_id'].queryset = self.getQuerySet('tasks')
        self.fields['assignor_id'].queryset = self.getQuerySet('users')
        self.fields['assignee_id'].queryset = self.getQuerySet('users')
        

    tid = forms.CharField(widget=forms.HiddenInput(), required=False)
    did = forms.CharField(widget=forms.HiddenInput(), required=False)
    lid = forms.CharField(widget=forms.HiddenInput(), required=False)
    sid = forms.CharField(widget=forms.HiddenInput(), required=False)
    vid = forms.CharField(widget=forms.HiddenInput(), required=False)
    aid = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    description = forms.CharField(max_length=255, empty_value="What's your task?")
    
    # Use enums from mapper_values for status and visibility choices
    status = forms.ChoiceField(
        choices=[(item.value, item.name.replace('_', ' ').title()) for item in Status],
        help_text="Select the current status of the task"
    )
    visibility = forms.ChoiceField(
        choices=[(item.value, item.name.replace('_', ' ').title()) for item in Visibility],
        help_text="Select who can see this task"
    )
    
    details = forms.CharField(widget=forms.Textarea, empty_value="Enter long description here...")
    deadline = forms.DateTimeField(required=False, widget=crud.DateTimeLocalInput())

    parent_id = forms.ModelChoiceField(queryset=Task.objects.none(), required=False)
    assignor_id = forms.ModelChoiceField(queryset=User.objects.none(), empty_label="Select One")
    assignee_id = forms.ModelChoiceField(queryset=User.objects.none(), empty_label="Select One")

    