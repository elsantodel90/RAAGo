from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'run-ratings-update', views.runRatingsUpdates, name='runRatingsUpdate'),
]

