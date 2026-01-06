from django.shortcuts import render, redirect
from django.urls import reverse
# from django.http import Http404, HttpResponse

from .drm.crud import *
from core.helpers.crud import isValidId
from core.helpers import misc
from core.modules.TasksEditForm import *

def dashboard(request):
    """
    Render the tasks dashboard (tabbed view).

    Provides a small initial `tasks` queryset in the context so templates that
    still iterate `tasks` continue to work. The tab-specific data is fetched
    by the client via the REST endpoints.
    """
    form = TasksEditForm()
    return render(request, 'tasks/index.html', {'form': form})

def viewTaskDetails(request, id):
    if isValidId({'id': id}, 'id'):
        records = CRUD().read(['all'], { 'tid': id, 'tdelete_time': 'is Null'})
        misc.log(records[0].id, 'Inside task details, why record not showing?', 2)
        if records:
            return render(request, 'tasks/record.html', {'record': records[0]})
    
    return render(request, "core/404.html", { 'Message': 'Hello', 'exception': 'Task ID invalid or record not found.' }, status=404)

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
