# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.urls import include
from django.urls import re_path as url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    #url(settings.ADMIN_URL, include(admin.site.urls)),
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('aago_ranking.users.urls', namespace='users')),
    url(r'^games/', include('aago_ranking.games.urls', namespace='games')),
    url(r'^ratings/', include('aago_ranking.ratings.urls', namespace='ratings')),
    url(r'^events/', include('aago_ranking.events.urls', namespace='events')),
    url(r'^accounts/', include('allauth.urls')),

    # This should go last
    url(r'^', include('aago_ranking.web.urls', namespace='web')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
