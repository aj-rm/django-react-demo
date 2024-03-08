#!/bin/bash

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Start server
gunicorn django_react.wsgi:application --bind 0.0.0.0:8000


exec "$@"