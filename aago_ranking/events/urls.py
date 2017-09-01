from django.conf.urls import url

from . import views

urlpatterns = [url(r'upload-event-file', views.upload_event_file, name='upload_event_file'), ]
