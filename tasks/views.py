from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponse

from .models import Task

def dashboard(request):
    """
    Render the tasks dashboard (tabbed view).

    Provides a small initial `tasks` queryset in the context so templates that
    still iterate `tasks` continue to work. The tab-specific data is fetched
    by the client via the REST endpoints.
    """
    return render(request, 'tasks/index.html', {'greating': 'Hello'})

def viewTaskDetails(request, id):
    pass

def editTask(request, id = None):
    pass

"""

Future code for the create task form..

pk = self.kwargs['pk']
if not isinstance(pk, int) or pk < 1:
    raise Exception(f'Record\'s ID missing. Cannot edit.')

initial = {}
records = CRUD().fetchFullRecordForUpdate(pk)
if records:
    taskRecord = records[0]  # we only need the first (?) @todo should this be re-visited?
    # Map model data to form fields
    initial['tid'] = taskRecord.id
    initial['task_id'] = taskRecord.id
    initial['did'] = taskRecord.did
    initial['lid'] = taskRecord.lid
    initial['sid'] = taskRecord.sid
    initial['vid'] = taskRecord.vid
    initial['aid'] = taskRecord.aid

    initial['description'] = taskRecord.description
    initial['status'] = taskRecord.status
    initial['visibility'] = taskRecord.visibility

    initial['details'] = taskRecord.details

    initial['deadline'] = taskRecord.deadline
    initial['parent_id'] = taskRecord.parent_id

    initial['assignor_id'] = taskRecord.assignor_id
    initial['assignee_id'] = taskRecord.assignee_id

TasksEditForm(initial)

#POST
if crud.isValidId(form.cleaned_data, 'tid'):
    CRUD().update(form.cleaned_data)
else:
    CRUD().create(form.cleaned_data)

# proceed with the original plans..
return super().form_valid(form)

"""
