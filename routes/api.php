<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProxyController;

Route::get('/', [ProxyController::class, 'index']);
Route::get('/{type}', [ProxyController::class, 'getProxy']);
