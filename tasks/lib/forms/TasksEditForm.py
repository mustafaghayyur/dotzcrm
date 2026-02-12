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
        

    tata_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    tade_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    tadl_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    tast_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    tavi_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    taas_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
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

    