from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView  #, DeleteView
from core.modules.TasksEditForm import TasksEditForm
from django import forms
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse



#from django.views.generic.dates import YearArchiveView

from core.Models.Tasks import CRUD
from core.Models import Tasks
from core.helpers import misc

class TasksListView(ListView):
    context_object_name = "tasks"
    template_name = "index.html"
    """
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            HttpResponse("<h3>Error: {e}</h3>")
    """
    # QuerySet refers to the ORM QuerySet object returned by any model query made in Django.
    # Which in our case is a RawQuerySet.
    def get_queryset(self):
        selectors = ['tid', 'description', 'tcreate_time', 'tupdate_time', 'status', 'visibility']
        results = CRUD().read(selectors)
        return results

class TaskDetailView(DetailView):
    context_object_name = "record"
    template_name = "record.html"
    """
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            HttpResponse("<h3>Error: {e}</h3>")
    """
    # object refers to the first 'object' found in the results' QuerySet
    # which in our case is a RawQuerySet
    def get_object(self, query_set):
        record = CRUD.read(['tid', 'description', 'tcreate_time', 'tupdate_time', 'status', 'visibility', 'details', 'assignor_id'])
        misc.log(record, 'results[detailed]')
        
        if record:
            return record[0]  # extract the Model instance from the RawQuerySet
        else:
            raise Http404("No record found matching the query")
        

"""
    The topology I have gathered so far:
     - FormView inherits forms.edit.ProcessFormView()
     - in ProcessFormView().get() the django.views.generic.base.TemplateResponseMixin
       .render_to_response() method is called.
     - render_to_response() is the key function that uses django.templates.response.TemplateResponse()
       to send back a view for the form in a GET request
     - In POST request ProcessFormView().post() is used


    I think forms.Form() handles validating the submitted form (before it gets sent via HTTP).
    If there are any errors, they are stored in the Form() class's error properties.
    Therefore, all rules setting should be done in the forms.Form() class.

    It is django.views.generic.base.View() class that determines the HTTP request type:
     - the View.dispatch() method attempts to call the existing view method named same
       as the HTTP method to render the response to the http request.
     - ProcessFormView() (referenced above) is the one which inherits from View()
     - Therefore, to generate a new view while using FormView(), one simply must
       overwrite a HTTP request method (in lowercase) like ProcessFormView() does.

"""
class TaskEditView(FormView):
    template_name = "edit.html"
    form_class = TasksEditForm
    success_url = "/tasks/"
    """
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            HttpResponse("<h3>Error: {e}</h3>")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            HttpResponse("<h3>Error: {e}</h3>")
    """
    def get_initial(self):
        initial = super().get_initial().copy
        pk = self.kwargs['pk']

        if pk is not None:
            taskRecord = CRUD.fetchFullRecordForUpdate(pk)

            # taskRecord is a RawQuerySet; which can be evaluated with a simple if
            if taskRecord:
                # Map model data to form fields
                initial['tid'] = taskRecord.task_id
                initial['task_id'] = taskRecord.task_id
                initial['did'] = taskRecord.details_id
                initial['lid'] = taskRecord.deadline_id
                initial['sid'] = taskRecord.status_id
                initial['vid'] = taskRecord.visibility_id
                initial['aid'] = taskRecord.assignment_id

                initial['description'] = taskRecord.description
                initial['status'] = taskRecord.status
                initial['visibility'] = taskRecord.visibility

                initial['details'] = taskRecord.details

                initial['deadline'] = taskRecord.deadline
                initial['parent_id'] = taskRecord.parent_id

                initial['assignor_id'] = taskRecord.assignor_id
                initial['assignee_id'] = taskRecord.assigne_id
            
        return initial  # Return the populated dictionary
    
    def form_valid(self, form):
        """
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        """
        if 'tid' in form and form['tid'] is not None:
            CRUD.update(form)
        else:
            CRUD.create(form)

        # proceed with the original plans..
        return super().form_valid(form)

