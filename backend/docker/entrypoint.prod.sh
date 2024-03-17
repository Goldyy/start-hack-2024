#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z $API_DATABASE_HOST $API_DATABASE_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

exec "$@"