<?php

namespace App\Http\Controllers;

use App\Models\Proxy;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Str;

class ProxyController extends Controller
{
    public function index()
    {
        return response()->json([
            'message' => 'Welcome to the GeoIP API!',
            'version' => '1.1.0',
            'website' => 'https://geoproxy.in',
            'documentation' => 'https://docs.geoproxy.in/',
            'github' => 'https://github.com/notcoderguy/geoproxy-db',
            'author' => 'https://notcoderguy.com',
        ]);
    }

    public function getProxy($type, Request $request)
    {
        $validated = $request->validate([
            'format' => 'sometimes|in:json,txt',
            'google_pass' => 'sometimes|boolean',
            'anonymous' => 'sometimes|boolean',
            'amount' => 'sometimes|integer|min:1|max:50',
        ]);

        $type = strtoupper($type);
        if (! in_array($type, ['HTTP', 'SOCKS4', 'SOCKS5'])) {
            return response()->json(['error' => 'Invalid proxy type. Choose HTTP, SOCKS4, or SOCKS5'], 400);
        }

        $amount = $validated['amount'] ?? 1;
        $googlePass = $validated['google_pass'] ?? '0';
        $anonymous = $validated['anonymous'] ?? 'Anonymous';
        $format = $validated['format'] ?? 'txt';

        $query = Proxy::query()
            ->where('status', 'active')
            ->where('protocol', strtolower($type))
            ->when($googlePass, fn ($q) => $q->withGooglePass('0'))
            ->when($anonymous, fn ($q) => $q->withAnonymity('Anonymous'));

        $proxies = $query->inRandomOrder()
            ->limit($amount)
            ->get(['ip', 'port', 'country', 'anonymity'])
            ->map(function ($proxy) {
                return [
                    'ip' => $proxy->ip,
                    'port' => $proxy->port,
                    'country' => $proxy->country,
                    'anonymous' => Str::lower($proxy->anonymity) === 'elite',
                ];
            });

        if ($proxies->isEmpty()) {
            return response()->json(['error' => 'No proxies found matching criteria'], 404);
        }

        if ($format === 'json') {
            return response()->json($proxies);
        }

        $txtOutput = $proxies->map(fn ($p) => "{$p['ip']}:{$p['port']}")->implode("\n");

        return new Response($txtOutput, 200, ['Content-Type' => 'text/plain']);
    }
}
