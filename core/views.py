from django.contrib.auth.decorators import login_not_required
from django.shortcuts import render

@login_not_required
def index (request):
    context = {
        'heading': 'Welcome',
        'content': 'This is a initial view for the CRM + PM Software',
    }

    return render(request, 'generic.html', context)

# For class based views use the method_decorator with the name='dispatch' 
# argument to apply the decorator to the main view logic:
# from django.contrib.auth.decorators import login_not_required
# @method_decorator(login_not_required, name='dispatch')

@login_not_required
def notFoundError(request, exception):
    context = {
        'Message': 'Hello',
        'exception': exception
    }
    return render(request, "404.html", context, status=404)
