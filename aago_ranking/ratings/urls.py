from django.conf.urls import url

from . import views

urlpatterns = [url(r'run-ratings-update', views.run_ratings_updates, name='run_ratings_update'), ]
