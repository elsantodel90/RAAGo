from django.urls import re_path as url

from . import views

app_name = 'events'

urlpatterns = [url(r'upload-event-file', views.upload_event_file, name='upload_event_file'), ]
