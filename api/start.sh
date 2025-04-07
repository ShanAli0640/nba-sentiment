#!/bin/bash
# start_backend.sh

cd "$(dirname "$0")"

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | xargs)  # This reads the .env file and exports the variables
fi

pip install --no-cache-dir -r requirements.txt

echo "Starting FastAPI backend..."
uvicorn app:app --reload
