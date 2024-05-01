#!/bin/sh

set -e

# Set superuser credentials as environment variables
export DJANGO_SUPERUSER_USERNAME=admin2
export DJANGO_SUPERUSER_EMAIL=wekesa360@outlook.com
export DJANGO_SUPERUSER_PASSWORD=password

# Collect static files
python manage.py collectstatic --noinput --clear

# Make and apply migrations
python manage.py makemigrations --noinput
python manage.py makemigrations notifications --noinput
python manage.py migrate notifications --noinput
python manage.py migrate --noinput

# Create the superuser non-interactively
python manage.py createsuperuser --noinput

# Start the server
gunicorn cmp.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
