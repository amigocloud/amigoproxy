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

""" AmigoProxy Fabric project """

import os
import sys
import getpass

import hipchat

from fabric.api import cd, env, task
from fabric.contrib import console
from fabric.operations import sudo

from amigoproxy.secrets import HIPCHAT_TOKEN


print "Fab file is using : " + sys.executable


@task
def proxy():
    """ Set environment variables for proxy site """

    env.user = getpass.getuser()
    if not console.confirm("Connect as '%s'?" % env.user, default=True):
        env.user = raw_input('Type user: ')
    print "You are connecting as '%s'" % env.user
    env.hosts = ['proxy.amigocloud.com']
    env.SITE_ROOT = '/srv/proxy.amigocloud.com'
    env.VIRTUAL_ENV = os.path.join(env.SITE_ROOT, 'virtual_env')
    env.PROJECT_ROOT = os.path.join(env.SITE_ROOT, 'amigoproxy')
    env.PYTHON = os.path.join(env.VIRTUAL_ENV, 'bin/python')
    env.PIP = os.path.join(env.VIRTUAL_ENV, 'bin/pip')
    env.SUPERVISOR_GROUP = 'proxy:'
    env.SUPERVISOR_GUNICORN_NAME = 'proxy_gunicorn'
    env.SUPERVISOR_CELERY_WORKER_NAMES = ['proxy_celery', 'proxy_celery_low']
    env.SUPERVISOR_CELERY_BEAT_NAME = 'proxy_celerybeat'
    env.server_name = 'AmigoProxy'
    env.server_github_user = 'amigobuild'


@task
def deploy(upgrade_env=False, reload_nginx=False, soft=False):
    """
    Update Server to latest code revision.
    * `upgrade_env=True to update the virtual env
    * `reload_nginx=True` to reload nginx
    * `soft=True` if changes don't affect celery (usually just aesthetic
      changes: html, css)
    """

    print "Using Github User: %s" % env.server_github_user

    with cd(env.PROJECT_ROOT):
        sudo('git pull', user=env.server_github_user)

        if upgrade_env:
            sudo(env.PIP + ' install -r REQUIREMENTS.txt --upgrade',
                 user=env.server_github_user)
        else:
            sudo(env.PIP + ' install -r REQUIREMENTS.txt',
                 user=env.server_github_user)

        with cd('src'):
            # sudo(env.PYTHON_INTERPRETER + ' manage.py syncdb --migrate',
            #      user=env.server_github_user)
            sudo(env.PYTHON + ' manage.py collectstatic --noinput',
                 user=env.server_github_user)

    if soft:
        # Only restart gunicorn
        sudo('/usr/bin/supervisorctl stop %s%s' %
             (env.SUPERVISOR_GROUP, env.SUPERVISOR_GUNICORN_NAME))
        sudo('/usr/bin/supervisorctl start %s%s' %
             (env.SUPERVISOR_GROUP, env.SUPERVISOR_GUNICORN_NAME))
    else:
        for worker in env.SUPERVISOR_CELERY_WORKER_NAMES:
            sudo('/usr/bin/supervisorctl stop %s%s' %
                 (env.SUPERVISOR_GROUP, worker))
        sudo('/usr/bin/supervisorctl stop %s%s' %
             (env.SUPERVISOR_GROUP, env.SUPERVISOR_CELERY_BEAT_NAME))
        sudo('/usr/bin/supervisorctl stop %s'
             % env.SUPERVISOR_GROUP)
        sudo('/usr/bin/supervisorctl start %s'
             % env.SUPERVISOR_GROUP)

    if reload_nginx:
        sudo('/etc/init.d/nginx reload')

    # Send notification to HipChat
    if hasattr(env, 'server_name') and HIPCHAT_TOKEN:
        # Notification to HipChat
        hc = hipchat.HipChat(token=HIPCHAT_TOKEN)
        msg = 'Hey team, %s just deployed to %s' % (env.user, env.server_name)
        hc.method('rooms/message',
                  parameters={'room_id': 440862, 'from': 'Deployer',
                              'message': msg, 'message_format': 'text',
                              'notify': 1})
