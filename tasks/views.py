from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, DeleteView
from core.modules.TasksEditForm import TasksEditForm
from django import forms
from django.shortcuts import get_object_or_404


#from django.views.generic.dates import YearArchiveView

from .models import Task
from core.Models import Tasks
from core.helpers import misc

class TasksListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "index.html"

    # QuerySet refers to the ORM QuerySet object returned by any model query made in Django.
    # Which in our case is a RawQuerySet.
    def get_queryset(self):
        results = Tasks.read(['id', 'description', 'create_time', 'update_time', 'status', 'visibility'])
        return results

class TaskDetailView(DetailView):
    model = Task
    context_object_name = "record"
    template_name = "record.html"

    # object refers to the first 'object' found in the results' QuerySet
    # which in our case is a RawQuerySet
    def get_object(self, query_set = None):
        record = Tasks.read(['id', 'description', 'create_time', 'update_time', 'status', 'visibility', 'details', 'assignor_id'])
        misc.log(record, 'results[detailed]')
        
        if record:
            return record[0]
        else:
            from django.http import Http404
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

    # Handles GET HTTPD method requests:
    def get_initial(self):
        """
            We will modify the get() operations as such:
            If there is an id provided (i.e. update operation)
            We will retrieve relevant records & prefill form with that data
        """

        initial = super().get_initial().copy
        pk = self.kwargs['pk']

        if pk is not None:
            taskRecord = Tasks.read(['all'], {id: pk})

            # taskRecord is a RawQuerySet; which can be evaluated with a simple
            # if statement to carry valid results:
            if taskRecord:
                # do somethings...
                # Map model data to form fields
                initial['field1'] = taskRecord.field1
                initial['field2'] = taskRecord.field2
            
        # Return the populated dictionary
        return initial


        # DEBUG CODE:
        # info1 = [attr for attr in dir(TaskEditView) if callable(getattr(TaskEditView, attr)) and not attr.startswith('__')]
        # info2 = [attr for attr in dir(TasksEditForm) if callable(getattr(TasksEditForm, attr)) and not attr.startswith('__')]
        # misc.log(info1, 'FormView Details:')
        # misc.log(info2, 'TasksEditForm Details:')

    
    def form_valid(self, form):
        """
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # If the validation for the submitted form passes.
        # This function is called. Save the models.
        """

        # Step 1: do some final checks:

        # Step 2: create seperate objects for each model:


        # Step 3: save the models:
        

        



        # proceed with the original plans..
        return super().form_valid(form)

