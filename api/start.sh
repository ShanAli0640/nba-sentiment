#!/bin/bash
# start_backend.sh

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found."
    echo "Please create it by running: python3 -m venv venv"
    exit 1
fi
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Starting FastAPI backend..."
uvicorn app:app --reload
