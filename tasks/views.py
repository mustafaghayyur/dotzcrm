from django.shortcuts import render

# Create your views here.

def index(request):
    data = {
        'name': "HomePage",
    }

    return render(request, 'index.html', {'data': data})
