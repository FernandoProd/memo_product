#!/bin/sh
# applying migrations
set -e

echo "Running database migrations for user_service..."
alembic upgrade head

echo "Starting user_service..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000