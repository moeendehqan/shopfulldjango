#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Check if database exists, create if not
psql -h $DB_HOST -U $DB_USER -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    psql -h $DB_HOST -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME"

# Run Django migrations
python manage.py migrate

# Start the Django application
exec python manage.py runserver 0.0.0.0:8000 