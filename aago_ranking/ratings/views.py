from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse

# Create your views here.

from . import tasks

def runRatingsUpdates(request):
    if request.method == "POST":
        json = tasks.run_ratings_update()
        return JsonResponse(json)
    else:
        raise Http404() # Meh, seria 405
