#!/bin/bash

# Azure Web App startup script for PerfBurger Chatbot
echo "Starting PerfBurger Chatbot with new monorepo structure..."

# Navigate to backend directory
cd /home/site/wwwroot/backend

# Set Python path to include backend directory
export PYTHONPATH="${PYTHONPATH}:/home/site/wwwroot/backend"

# Create tmp directory for SQLite if it doesn't exist
mkdir -p /tmp

# Log environment info for debugging
echo "Python path: $PYTHONPATH"
echo "Current directory: $(pwd)"
echo "OpenAI API Key configured: $([ -n "$OPENAI_API_KEY" ] && echo "Yes" || echo "No")"

# Start gunicorn server (database tables will be created automatically on first request)
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --log-level info run:app
