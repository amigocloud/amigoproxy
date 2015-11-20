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

from django.conf.urls import patterns, url

from .views import io_counters, TargetsView, SourcesView, GroupsView


urlpatterns = patterns(
    '',
    url(r'^io_counters/?$', io_counters, name='io_counters'),
    url(r'^targets/?$', TargetsView.as_view(), name='targets'),
    url(r'^sources/?$', SourcesView.as_view(), name='sources'),
    url(r'^groups/?$', GroupsView.as_view(), name='groups'),
)
