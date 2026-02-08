from django.shortcuts import render
from tasks.lib.forms.TasksEditForm import *

def dashboard(request):
    """
        Render the tasks dashboard (tabbed view).
    """
    context = {
        'form': TasksEditForm(),
    }
    return render(request, 'tasks/index.html', context)

