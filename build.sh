#!/bin/sh
dir1=/var/www/homedash/
while inotifywait -qqre modify "$dir1"; do
	    sudo uwsgi --ini /var/www/homedash/uwsgi.ini && sudo service nginx restart
    done
