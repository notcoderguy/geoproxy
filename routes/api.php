<?php

use App\Http\Controllers\ProxyController;
use Illuminate\Support\Facades\Route;

Route::get('/', [ProxyController::class, 'index']);
Route::get('/{type}', [ProxyController::class, 'getProxy']);
