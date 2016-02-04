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

import redis
import requests
import time

from django.conf import settings

LAST_SECOND_DATA_IN = 'lsdi_%s'
LAST_SECOND_DATA_OUT = 'lsdo_%s'
LAST_MINUTE_DATA_IN = 'lmdi_%s'
LAST_MINUTE_DATA_OUT = 'lmdo_%s'

LAST_SECOND_COUNT_IN = 'lsci_%s'
LAST_SECOND_COUNT_OUT = 'lsco_%s'
LAST_MINUTE_COUNT_IN = 'lmci_%s'
LAST_MINUTE_COUNT_OUT = 'lmco_%s'


IN_KEYS = (LAST_SECOND_DATA_IN, LAST_SECOND_COUNT_IN,
           LAST_MINUTE_DATA_IN, LAST_MINUTE_COUNT_IN)
OUT_KEYS = (LAST_SECOND_DATA_OUT, LAST_SECOND_COUNT_OUT,
            LAST_MINUTE_DATA_OUT, LAST_MINUTE_COUNT_OUT)


def get_redis():
    return redis.Redis(host=settings.REDIS_HOST or 'localhost')


def update_counters(body_length,
                    second_data_key, second_count_key,
                    minute_data_key, minute_count_key, r=None):
    if r is None:
        r = get_redis()
    second = int(time.time())
    minute = second - (second % 60)
    # last second (data)
    r.incr(second_data_key % second, body_length)
    r.expire(second_data_key % second, 5)
    # last second (count)
    r.incr(second_count_key % second, 1)
    r.expire(second_count_key % second, 5)
    # last minute (data)
    r.incr(minute_data_key % minute, body_length)
    r.expire(minute_data_key % minute, 65)
    # last minute (count)
    r.incr(minute_count_key % minute, 1)
    r.expire(minute_count_key % minute, 65)


def update_input_counters(body_length, r=None):
    update_counters(body_length, *IN_KEYS, r=r)


def update_output_counters(body_length, r=None):
    update_counters(body_length, *OUT_KEYS, r=r)


def get_io_counters(r=None):
    if r is None:
        r = get_redis()
    last_second = int(time.time()) - 1
    last_minute = last_second - (last_second % 60) - 60
    return (r.get(LAST_SECOND_DATA_IN % last_second) or '0',
            r.get(LAST_SECOND_COUNT_IN % last_second) or '0',
            r.get(LAST_SECOND_DATA_OUT % last_second) or '0',
            r.get(LAST_SECOND_COUNT_OUT % last_second) or '0',
            r.get(LAST_MINUTE_DATA_IN % last_minute) or '0',
            r.get(LAST_MINUTE_COUNT_IN % last_minute) or '0',
            r.get(LAST_MINUTE_DATA_OUT % last_minute) or '0',
            r.get(LAST_MINUTE_COUNT_OUT % last_minute) or '0')


def update_url_responsiveness(url, reached_timeout, r=None):
    if r is None:
        r = get_redis()
    increment = 1 if reached_timeout else -1
    value = r.incr(url, increment)
    if (value > 10 * settings.EXPECTED_CONCURRENCY or
            value < - 10 * settings.EXPECTED_CONCURRENCY):
        r.incr(url, -increment)
    r.expire(url, int(10 * settings.POST_TIMEOUT))


def get_url_responsiveness(url, r=None):
    if r is None:
        r = get_redis()
    return int(r.get(url) or 0)


def resend(url, request_body, timeout, logger=None):
    r = get_redis()
    try:
        requests.post(url, data=request_body, timeout=timeout)
        update_output_counters(len(request_body), r)
        update_url_responsiveness(url, True, r)
        if logger:
            logger.debug("POSTed successfully to '%s'", url)
    except requests.exceptions.Timeout:
        update_output_counters(len(request_body), r)
        update_url_responsiveness(url, False, r)
        if logger:
            logger.warning("Timeout reached when POSTing data to '%s'", url)
    except requests.exceptions.RequestException as exc:
        if logger:
            logger.error("Failed to POST data to '%s': %s", url, exc)
        raise
