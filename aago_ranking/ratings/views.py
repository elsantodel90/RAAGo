from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from . import tasks


@staff_member_required
@require_http_methods(["POST"])
def run_ratings_update(_request):
    json = tasks.run_ratings_update()
    return JsonResponse(json)
