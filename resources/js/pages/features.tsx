import { AppShell } from '@/components/app-shell';
import { AppSidebar } from '@/components/app-sidebar';
import { Head } from '@inertiajs/react';
import Heading from '@/components/heading';
import { MobileNavbar } from '@/components/mobile-navbar'; // <-- Add this import

const features = [
    {
        title: 'Comprehensive Proxy Information',
        description: 'Detailed data on each proxy, including IP, port, and location',
    },
    {
        title: 'Google passed & Elite Proxies',
        description: 'High quality proxies that pass Google verification',
    },
    {
        title: 'Geolocation Insights',
        description: 'Detailed location data for each proxy',
    },
    {
        title: 'Developer-Friendly API',
        description: 'Easy integration with your applications',
    },
    {
        title: 'Regular Database Updates',
        description: 'Fresh proxies every 30 minutes',
    },
    {
        title: 'Multiple Protocols',
        description: 'HTTP, SOCKS4, SOCKS5 support',
    },
];

export default function Features() {
    return (
        <>
            <Head title="Features"></Head>

            <AppShell variant="sidebar">
                <AppSidebar />
                <div className="bg-background text-foreground relative flex min-h-screen w-full snap-y snap-mandatory flex-col items-center overflow-y-auto px-4 [-ms-overflow-style:none] [scrollbar-width:none] sm:px-6 lg:px-8 [&::-webkit-scrollbar]:hidden">
                    <section
                        className="flex min-h-screen w-full max-w-7xl snap-start flex-col justify-center py-20 text-center"
                    >
                        <Heading
                            title="Discover the Power of GeoProxy Service"
                            description="Level up your web scraping with Geoproxy's proxy API! 💻 HTTP, SOCKS4, SOCKS5 data at your fingertips. 😉 Stay anonymous, bypass restrictions."
                        />

                        <div className="mt-12 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                            {features.map((feature, i) => (
                                <div key={i} className="space-y-2 rounded-lg border p-6">
                                    <h3 className="text-lg font-medium">{feature.title}</h3>
                                    <p className="text-muted-foreground">{feature.description}</p>
                                </div>
                            ))}
                        </div>
                    </section>
                </div>
                <MobileNavbar />
            </AppShell>
        </>
    );
}
