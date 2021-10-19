from django.shortcuts import render
from django.conf import settings

# Create your views here.
def index(request):
    context = {
        'greetings': getattr(settings, 'GREETINGS') or 'Hello, world!'
    }
    return render(request, "core/index.html", context=context)
