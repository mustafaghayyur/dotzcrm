from django.shortcuts import render, redirect
from django.urls import reverse
# from django.http import Http404, HttpResponse

from .drm.crud import *
from core.helpers.crud import isValidId
from core.helpers import misc
from core.lib.TasksEditForm import *

def dashboard(request):
    """
        Render the tasks dashboard (tabbed view).
    """
    context = {
        'form': TasksEditForm(),
    }
    return render(request, 'tasks/index.html', context)

