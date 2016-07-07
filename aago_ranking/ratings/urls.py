from django.conf.urls import url

from . import views

urlpatterns = [url(r'run-ratings-update', views.run_ratings_update, name='run_ratings_update'), ]
