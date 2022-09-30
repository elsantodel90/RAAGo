#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import re_path as url
from django.views.generic import TemplateView

from . import views

app_name = 'web'

urlpatterns = [
    url(r'^$', views.homepage, name='home'),
    url(r'^active$', views.homepage_active, name='homeactive'),
    url(r'^ranking\.csv$', views.csv_ranking, name='ranking'),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'),
]
