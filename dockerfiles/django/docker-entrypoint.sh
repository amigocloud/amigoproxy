#!/bin/bash

if [ "$1" = "gunicorn" ]; then
    cd /srv/amigoproxy/
    exec "$@"
fi

exec "$@"
