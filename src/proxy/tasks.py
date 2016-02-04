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

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from raven import Client
from raven.contrib.celery import register_signal
import pika

from .utils import resend as _resend

logger = get_task_logger(__name__)


if settings.RAVEN_CONFIG:
    client = Client(settings.RAVEN_CONFIG['dsn'])
    register_signal(client)


@shared_task(name='resend', max_retries=3, default_retry_delay=60)
def resend(url, request_body):
    try:
        _resend(url, request_body, settings.POST_TIMEOUT)
        return 'Ok'
    except Exception as exc:
        resend.retry(exc=exc)
        return 'Fail'


@shared_task(name='resend_low', max_retries=2, default_retry_delay=60)
def resend_low(url, request_body):
    try:
        _resend(url, request_body, settings.POST_TIMEOUT * 2)
        return 'Ok'
    except Exception as exc:
        resend_low.retry(exc=exc)
        return 'Fail'


@shared_task(name='clean_low_queue')
def clean_low_queue():
    parameters = pika.URLParameters(settings.BROKER_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    try:
        channel.queue_purge('celery_low')
    except pika.exceptions.ChannelClosed as exc:
        pass
    finally:
        if channel.is_open:
            channel.close()
        if connection.is_open:
            connection.close()
