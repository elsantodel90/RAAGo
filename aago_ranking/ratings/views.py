from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from . import tasks


@staff_member_required
def run_ratings_update(_request):
    json = tasks.run_ratings_update()
    return JsonResponse(json)
