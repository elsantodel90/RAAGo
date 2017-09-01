
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from . import tasks

@staff_member_required
@require_http_methods(["POST"])
def upload_event_file(request):
    json = tasks.upload_event_file(request.FILES["event_file"])
    return JsonResponse(json)
