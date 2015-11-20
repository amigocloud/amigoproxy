#!/bin/sh

# Installation
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo apt-get install redis-server
sudo apt-get install nginx
sudo apt-get install supervisor
sudo apt-get install gunicorn
sudo apt-get install git
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade virtualenv

# Users and folders
sudo adduser amigobuild
sudo mkdir -p /srv/proxy.amigocloud.com
chown amigobuild:amigobuild /srv/proxy.amigocloud.com

# Repo
sudo -u amigobuild ssh-keygen -t rsa
# Copy ~/.ssh/id_rsa.pub to amigobuild GitHub SSH keys
cd /srv/proxy.amigocloud.com
sudo -u amigobuild virtualenv virtual_env
sudo -u amigobuild source virtual_env/bin/activate
sudo -u amigobuild git clone git@github.com:amigocloud/amigoproxy.git
cd amigoproxy
sudo -u amigobuild pip install -r REQUIREMENTS.txt

# RabbitMQ
sudo service rabbitmq-server start
sudo rabbitmq-plugins enable rabbitmq_management
sudo service rabbitmq-server restart
sudo rabbitmqctl add_user proxy_rabbitmq <password>
sudo rabbitmqctl set_user_tags proxy_rabbitmq administrator
sudo rabbitmqctl set_permissions -p / proxy_rabbitmq ".*" ".*" ".*"
sudo rabbitmqctl delete_user guest

# Redis
sudo /etc/init.d/redis-server start

# Nginx
cd /etc/nginx/sites-available
sudo ln -s /srv/proxy.amigocloud.com/amigoproxy/conf/nginx/proxy.amigocloud.com
cd ../sites-enabled
sudo ln -s ../sites-available/proxy.amigocloud.com
sudo /etc/init.d/nginx start

# Supervisor
cd /etc/supervisor/conf.d
sudo ln -s /srv/proxy.amigocloud.com/amigoproxy/conf/supervisor/proxy.amigocloud.conf
sudo service supervisor start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart proxy:
