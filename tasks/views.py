from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.views.generic.dates import YearArchiveView

from .models import Task
from .models import TaskDetails
from .models import TaskDeadline
from .models import TaskStatus
from .models import TaskWatcher
from .models import TaskUserAssignment

# Create your views here.

class TasksListView(ListView):
    model = Task
    context_object_name = "data"
    template_name = "index.html"


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "records"
    template_name = "record.html"

    def get_context_data(self, **kwargs):      
        """Insert the single object into the context dict."""
        context = {}
        
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            
            if context_object_name:
                context[context_object_name] = {}
                context[context_object_name]["task"] = self.object
                context[context_object_name]["details"] = TaskDetails.objects.all()
                context[context_object_name]["deadlines"] = TaskDeadline.objects.all()
                context[context_object_name]["status"] = TaskStatus.objects.all()
                context[context_object_name]["watchers"] = TaskWatcher.objects.all()
                context[context_object_name]["assignments"] = TaskUserAssignment.objects.all()
        

        # context['status'][0].status gets you the status
        context.update(kwargs)
        return super().get_context_data(**context)
        


# Create your views here.
#def index(request):
#    data = {
#        'name': "HomePage",
#    }
#
#    return render(request, 'index.html', {'data': data})
