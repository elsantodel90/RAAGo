from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from . import tasks


@staff_member_required
def runRatingsUpdates(request):
    if request.method == "POST":
        json = tasks.run_ratings_update()
        return JsonResponse(json)
    else:
        raise Http404()  # Meh, seria 405
