#!/bin/sh
echo "Starting the sys_watcher daemon"
python sys_watcher.py &

echo "Starting Django Devleopment Web Server
python manage.py runserver &

echo "Starting Firefox"
firefox 127.0.0.1:8000/watchtower/api?
