#!/bin/bash

# Start mmdb pull
php artisan app:pull:mmdb

php artisan app:link:database
php artisan app:link:mmdb
php artisan app:link:proxy

# Run Laravel server
php artisan serve --host=0.0.0.0 --port=80
