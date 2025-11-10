from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, DeleteView
from core.modules.TasksEditForm import TasksEditForm
from django import forms

#from django.views.generic.dates import YearArchiveView

from .models import Task
from core.helpers import misc

class TasksListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "index.html"

    def get_queryset(self):
        results = Task.rawobjects.fetchTasks('1', ['id', 'description', 'create_time', 'update_time', 'status', 'visibility'])
        return results

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "record"
    template_name = "record.html"

    def get_object(self, query_set = None):
        results = Task.rawobjects.fetchTasks('1', ['id', 'description', 'create_time', 'update_time', 'status', 'visibility', 'details', 'assignor_id'])
        misc.log(results, 'results[detailed]')
        try:
            obj = results[0]
        except IndexError:
            # Handle the case where the object is not found
            from django.http import Http404
            raise Http404("No record found matching the query")
        return obj
        
class TaskEditView(FormView):
    template_name = "edit.html"
    form_class = TasksEditForm
    success_url = "/thanks/"

    # Delete this method once you're done testing!
    def get_form(self, form_class=None):
        info1 = [attr for attr in dir(TaskEditView) if callable(getattr(TaskEditView, attr)) and not attr.startswith('__')]
        info2 = [attr for attr in dir(TasksEditForm) if callable(getattr(TasksEditForm, attr)) and not attr.startswith('__')]
        misc.log(info1, 'FormView Details:')
        misc.log(info2, 'TasksEditForm Details:')
        
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super().form_valid(form)
