#!/bin/bash

# Start mmdb pull
php artisan app:pull:mmdb

php artisan app:link:database
php artisan app:link:mmdb
php artisan app:link:proxy

# Activate Python venv and run scraper in background
cd scraper && \
source .venv/bin/activate && \
python main.py &

# Start Laravel server
cd ..
php artisan serve --host=0.0.0.0 --port=80
