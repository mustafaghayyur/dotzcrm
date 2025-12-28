from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponse

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView  # , DeleteView
# from django.views.generic.dates import YearArchiveView

from core.modules.TasksEditForm import TasksEditForm
from .DRM.crud import CRUD
from core.helpers import misc, crud

class TasksListView(ListView):
    context_object_name = "tasks"
    template_name = "index.html"
    user_id = None
    
    def get(self, request, *args, **kwargs):
        #try:
        self.user_id = request.user.id
        return super().get(request, *args, **kwargs)
        #except Exception as e:
        #    raise Http404(f'Error: {e}')
        
    # QuerySet refers to the ORM QuerySet object returned by any model query made in Django.
    # Which in our case is a RawQuerySet.
    def get_queryset(self):
        results = CRUD().read(['tid', 'description', 'tupdate_time', 'status', 'visibility'], {"creator_id": self.user_id, "visibility": 'private'})
        misc.log(results, 'RAW SQL OUTPUT [List]')
        return results

class TaskDetailView(DetailView):
    context_object_name = "record"
    template_name = "record.html"
    
    def get(self, request, *args, **kwargs):
        """
            This GET call will retrieve a full record for the Task's Primary Key in question.
            Does not retrieve deleted records.
        """
        #try:
        return super().get(request, *args, **kwargs)
        #except Exception as e:
        #    raise Http404(f'Error: {e}')

    def post(self, request, *args, **kwargs):
        """
            This POST call will delete the Primary Key in question
        """
        try:
            if 'pk' in self.kwargs:
                CRUD().delete(self.kwargs['pk'])
            return redirect(reverse('tasks_index'))
        except Exception as e:
            raise Http404(f'Error: {e}')
    
    # object refers to the first 'object' found in the results' QuerySet
    # which in our case is a RawQuerySet

    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            record = CRUD().read(['all'], {'tid': self.kwargs['pk'], 'tdelete_time': 'is NULL'})
            # misc.log(record, 'RAW SQL OUTPUT [Details]')

            if record:
                return record[0]  # extract the Model instance from the RawQuerySet
        
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
        initial = {}

        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            if not isinstance(pk, int) or pk < 1:
                raise Exception(f'Record\'s ID missing. Cannot edit.')

            records = CRUD().fetchFullRecordForUpdate(pk)

            # taskRecord is a RawQuerySet; which can be evaluated with a simple if
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
            
        self.initial = initial
        return self.initial.copy()
    
    def form_valid(self, form):
        """
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        """
        if crud.isValidId(form.cleaned_data, 'tid'):
            CRUD().update(form.cleaned_data)
        else:
            CRUD().create(form.cleaned_data)

        # proceed with the original plans..
        return super().form_valid(form)

