#!/bin/bash
# start_backend.sh

cd "$(dirname "$0")"

pip install --no-cache-dir -r requirements.txt

echo "Starting FastAPI backend..."
uvicorn app:app --reload
