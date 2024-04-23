#!/bin/sh

set -e

# Set superuser credentials as environment variables
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@mail.com
export DJANGO_SUPERUSER_PASSWORD=password

# Collect static files
python manage.py collectstatic --noinput --clear

# Make and apply migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create the superuser non-interactively
python manage.py createsuperuser --noinput

# Start the server
gunicorn cmp.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
