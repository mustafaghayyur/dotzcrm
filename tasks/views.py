from django.views.generic import ListView, DetailView
#from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
#from django.views.generic.dates import YearArchiveView

from .models import Task

from core.helpers import misc

# Create your views here.

class TasksListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "index.html"

    def get_queryset(self):
        results = Task.rawobjects.fetchTasks('1', ['id', 'description', 'create_time', 'update_time', 'status', 'visibility'])
        misc.log(results, 'results')
        
        return results


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "records"
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
        

# Create your views here.
#def index(request):
#    data = {
#        'name': "HomePage",
#    }
#
#    return render(request, 'index.html', {'data': data})
