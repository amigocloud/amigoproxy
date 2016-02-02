#!/bin/bash

if [ "$1" = "celery" ]; then
    cd /srv/amigoproxy/
    exec "$@"
fi

exec "$@"
