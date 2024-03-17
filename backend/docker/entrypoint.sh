#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# run system check
python manage.py check
python manage.py makemigrations


# run database migrations
(flock 200; python manage.py migrate --skip-checks --no-input; echo "") 200>/app/migration.lock

# collect static files
python manage.py collectstatic --clear --link --no-input

# add superuser
python manage.py createsuperuser --no-input

# let's go!
exec "$@"
