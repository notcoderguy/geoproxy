import { AppShell } from '@/components/app-shell';
import { AppSidebar } from '@/components/app-sidebar';
import { Head } from '@inertiajs/react';
import Heading from '@/components/heading';
import { Button } from '@/components/ui/button';
import { MobileNavbar } from '@/components/mobile-navbar'; // <-- Add this import

const downloadOptions = [
    {
        type: 'HTTP',
        formats: ['txt', 'json', 'csv'],
        links: ['/proxies/http_proxies.txt', '/proxies/http_proxies.json', '/proxies/http_proxies.csv'],
    },
    {
        type: 'SOCKS4',
        formats: ['txt', 'json', 'csv'],
        links: ['/proxies/socks4_proxies.txt', '/proxies/socks4_proxies.json', '/proxies/socks4_proxies.csv'],
    },
    {
        type: 'SOCKS5',
        formats: ['txt', 'json', 'csv'],
        links: ['/proxies/socks5_proxies.txt', '/proxies/socks5_proxies.json', '/proxies/socks5_proxies.csv'],
    },
];

export default function Downloads() {
    return (
        <>
            <Head title="Downloads"></Head>

            <AppShell variant="sidebar">
                <AppSidebar />
                <div className="bg-background text-foreground relative flex min-h-screen w-full snap-y snap-mandatory flex-col items-center overflow-y-auto px-4 [-ms-overflow-style:none] [scrollbar-width:none] sm:px-6 lg:px-8 [&::-webkit-scrollbar]:hidden">
                    <section
                        className="flex min-h-screen w-full max-w-7xl snap-start flex-col justify-center py-20 text-center"
                    >

                        <Heading title="Download the proxies" description="Get started with the resources you need. Simply click to download." />

                        <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-3">
                            {downloadOptions.map((option) => (
                                <div key={option.type} className="flex flex-col gap-2">
                                    <h3 className="text-lg font-medium">{option.type} Proxies</h3>
                                    <div className="flex flex-col gap-2">
                                        {option.formats.map((format) => (
                                            <Button
                                                key={format}
                                                variant="outline"
                                                size="lg"
                                                className="w-full hover:cursor-pointer hover:shadow-lg transition-shadow duration-300"
                                                onClick={() => {
                                                    const link = option.links.find((link) => link.endsWith(format));
                                                    if (link) {
                                                        // window.location.href = link;
                                                        window.open(link, '_blank');
                                                    }
                                                }}
                                            >
                                                {option.type.toLowerCase()}.{format}
                                            </Button>
                                        ))}
                                    </div>
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
