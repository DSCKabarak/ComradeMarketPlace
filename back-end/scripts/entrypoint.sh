#!/bin/sh

set -e

# Set superuser credentials as environment variables
export DJANGO_SUPERUSER_USERNAME=username
export DJANGO_SUPERUSER_EMAIL=admin@email.com
export DJANGO_SUPERUSER_PASSWORD=password

# Collect static files
python manage.py collectstatic --noinput --clear

# Make and apply migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create the superuser non-interactively
python manage.py createsuperuser --noinput
