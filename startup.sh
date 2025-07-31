#!/bin/bash

# Azure Web App startup script
echo "Starting PerfBurger Chatbot..."

# Initialize database
python init_db.py

# Start gunicorn server
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 run:app
