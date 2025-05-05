<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}" @class(['dark'=> ($appearance ?? 'system') == 'dark'])>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    {{-- Inline script to detect system dark mode preference and apply it immediately --}}
    <script>
        (function() {
            const appearance = '{{ $appearance ?? "system" }}';

            if (appearance === 'system') {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

                if (prefersDark) {
                    document.documentElement.classList.add('dark');
                }
            }
        })();
    </script>

    {{-- Inline style to set the HTML background color based on our theme in app.css --}}
    <style>
        html {
            background-color: oklch(1 0 0);
        }

        html.dark {
            background-color: oklch(0.145 0 0);
        }
    </style>

    <title inertia>{{ config('app.name', 'GeoProxy') }}</title>


    <link rel="icon" type="image/svg+xml" href="/logo.svg">
    <meta name="msapplication-TileImage" content="/logo.svg">

    <meta name="title" content="GeoProxy">
    <meta name="description"
        content="🌐 GeoProxy: Level up your web scraping with Geoproxy's proxy API! 💻 HTTP, SOCKS4, SOCKS5 data at your fingertips. 😉 Stay anonymous, bypass restrictions." />

    <meta property="og:type" content="website">
    <meta property="og:url" content="https://geoproxy.in/">
    <meta property="og:title" content="GeoProxy">
    <meta property="og:description"
        content="🌐 GeoProxy: Level up your web scraping with Geoproxy's proxy API! 💻 HTTP, SOCKS4, SOCKS5 data at your fingertips. 😉 Stay anonymous, bypass restrictions." />
    <meta property="og:image" content="/banner.png">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://geoproxy.in/">
    <meta property="twitter:title" content="GeoProxy">
    <meta property="twitter:description"
        content="🌐 GeoProxy: Level up your web scraping with Geoproxy's proxy API! 💻 HTTP, SOCKS4, SOCKS5 data at your fingertips. 😉 Stay anonymous, bypass restrictions.">
    <meta property="twitter:image" content="/banner.png">

    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=instrument-sans:400,500,600" rel="stylesheet" />

    @routes
    @viteReactRefresh
    @vite(['resources/js/app.tsx', "resources/js/pages/{$page['component']}.tsx"])
    @inertiaHead
</head>

<body class="font-sans antialiased">
    @inertia
</body>

</html>