#!/bin/sh

yes | python manage.py makemigrations --merge
python manage.py migrate

exec "$@"