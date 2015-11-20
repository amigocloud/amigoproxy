# AmigoProxy
#
# Copyright (c) 2011-2015 AmigoCloud Inc., All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library.

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.decorators.csrf import csrf_exempt

from proxy.forms import LoginForm
from proxy.views import DashboardView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', csrf_exempt(DashboardView.as_view()), name='dashboard'),
    url(r'^login/?$', login,
        {'template_name': 'login.html', 'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/?$',
        logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^proxy/', include('proxy.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
