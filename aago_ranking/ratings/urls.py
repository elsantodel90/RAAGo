from django.urls import re_path as url

from . import views

app_name = 'ratings'

urlpatterns = [url(r'run-ratings-update', views.run_ratings_update, name='run_ratings_update'), ]
