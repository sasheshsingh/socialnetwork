#!/bin/bash
# start.sh

# Wait for PostgreSQL to be ready

# Apply Django migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Start Django server
python manage.py runserver 0.0.0.0:8000
