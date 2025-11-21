from django.shortcuts import render

def index (request):
    context = {
        'heading': 'Welcome',
        'content': 'This is a initial view for the CRM + PM Software',
    }

    return render(request, 'generic.html', context)

def notFoundError(request, exception):
    context = {
        'Message': 'Hello',
        'exception': exception
    }
    return render(request, "404.html", context, status=404)
