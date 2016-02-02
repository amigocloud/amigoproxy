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
from django.http import HttpResponseRedirect


class SSLMiddleware(object):

    def process_request(self, request):
        if (not settings.DEBUG and not request.is_secure() and
                request.method == 'GET' and
                request.META.get('HTTP_X_FORWARDED_PROTO', '') != 'https'):
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace('http://', 'https://')
            response = HttpResponseRedirect(secure_url)
            response['Cache-Control'] = 'private'
            return response
