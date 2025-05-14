#!/bin/bash

# Start mmdb pull
php artisan app:pull:mmdb

php artisan app:link:database
php artisan app:link:mmdb
php artisan app:link:proxy

# Run Python scraper in background, showing logs in console
(
  cd scraper
  source .venv/bin/activate
  python main.py
) &

# Run Laravel server, showing logs in console
php artisan serve --host=0.0.0.0 --port=80
