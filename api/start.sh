#!/bin/bash

# Start the cron script in the background
python main.py &

# Start the Uvicorn server
uvicorn app:app --host 0.0.0.0 --port 8000