#!/bin/bash
# start_backend.sh

cd "$(dirname "$0")"

echo "Starting FastAPI backend..."
uvicorn app:app --reload
