#!/bin/bash

if [ "$1" = "flower" ]; then
    exec "$@" --broker=$BROKER_URL --broker_api=$BROKER_API
fi

exec "$@"
