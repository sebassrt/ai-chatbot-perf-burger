#!/bin/bash

# Azure Web App startup script
echo "Starting PerfBurger Chatbot..."

# Set Python path
export PYTHONPATH="${PYTHONPATH}:/home/site/wwwroot"

# Create tmp directory for SQLite if it doesn't exist
mkdir -p /tmp

# Initialize database (suppress errors if already exists)
python init_db.py || echo "Database already initialized or init failed"

# Start gunicorn server
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --log-level info run:app
