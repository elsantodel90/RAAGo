from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.http import JsonResponse

from . import tasks


@staff_member_required
def run_ratings_updates(request):
    if request.method == "POST":
        json = tasks.run_ratings_update()
        return JsonResponse(json)
    else:
        raise Http404()  # Meh, seria 405
