#!/bin/bash
while true; do
    current_hour=$(date +%H)
    if [ "$current_hour" = "02" ]; then
        cd /var/www/html/scraper && .venv/bin/python main.py
    fi
    sleep 3600 # Check every hour
done
