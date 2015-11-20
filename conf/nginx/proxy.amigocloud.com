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

server {
    listen                 80;
    server_name            proxy.amigocloud.com;

    root                   /srv/proxy.amigocloud.com;
    client_max_body_size   8M;
    access_log             /var/log/nginx/proxy.amigocloud.com.access.log;
    error_log              /var/log/nginx/proxy.amigocloud.com.error.log;

    error_page             404   /srv/proxy.amigocloud.com/amigoproxy/templates/404.html;
    error_page             500   /srv/proxy.amigocloud.com/amigoproxy/templates/500.html;

    location / {
        proxy_pass            http://127.0.0.1:9000;
        proxy_set_header      Host              $host;
        proxy_set_header      X-Real-IP         $remote_addr;
        proxy_set_header      X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_connect_timeout 30s;
        proxy_read_timeout    30s;
    }

    location /static/ {
        autoindex  off;
        alias      /srv/proxy.amigocloud.com/amigoproxy/static/;
        expires    30d;
        add_header Pragma public;
        add_header Cache-Control   "public";
    }
}
