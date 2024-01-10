#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static
apt-get update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello World!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root   /var/www/html;
    index index.html index.htm;
    add_header X-Served-By $HOSTNAME;

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=cw8tuNZjIf4;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}" > /etc/nginx/sites-available/default

service nginx restart

