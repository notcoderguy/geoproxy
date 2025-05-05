import { AppShell } from '@/components/app-shell';
import { AppSidebar } from '@/components/app-sidebar';
import Heading from '@/components/heading';
import { Button } from '@/components/ui/button';
import { Head } from '@inertiajs/react';
import { useEffect, useRef, useState } from 'react';

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

export default function Home() {
    const [activeSection, setActiveSection] = useState(0);
    const sectionsRef = useRef<(HTMLElement | null)[]>([]);

    useEffect(() => {
        // Hide scrollbar but allow scrolling
        document.documentElement.style.overflowY = 'scroll';
        document.documentElement.style.scrollbarWidth = 'none';
        // @ts-expect-error - msOverflowStyle is IE specific
        document.documentElement.style.msOverflowStyle = 'none';

        let isScrolling = false;
        let scrollTimeout: NodeJS.Timeout;

        const handleScroll = () => {
            if (isScrolling) return;

            clearTimeout(scrollTimeout);

            const scrollPosition = window.scrollY;
            const windowHeight = window.innerHeight;
            const currentSection = Math.round(scrollPosition / windowHeight);

            // Only snap if we're close to a section boundary
            if (Math.abs(scrollPosition - currentSection * windowHeight) < windowHeight * 0.3) {
                isScrolling = true;
                window.scrollTo({
                    top: currentSection * windowHeight,
                    behavior: 'smooth',
                });

                scrollTimeout = setTimeout(() => {
                    isScrolling = false;
                }, 500);
            }

            // Update active section indicator
            sectionsRef.current.forEach((section, index) => {
                if (
                    section &&
                    section.offsetTop <= scrollPosition + windowHeight / 2 &&
                    section.offsetTop + section.offsetHeight > scrollPosition + windowHeight / 2
                ) {
                    setActiveSection(index);
                }
            });
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <>
            <Head title="Home"></Head>

            <AppShell variant="sidebar">
                <AppSidebar />

                <div className="bg-background text-foreground relative flex min-h-screen w-full snap-y snap-mandatory flex-col items-center overflow-y-auto px-4 py-12 [-ms-overflow-style:none] [scrollbar-width:none] sm:px-6 lg:px-8 [&::-webkit-scrollbar]:hidden">
                    {/* Section Navigation */}
                    <div className="fixed top-1/2 right-8 hidden -translate-y-1/2 transform lg:block">
                        <div className="flex flex-col items-center space-y-4">
                            {[0, 1, 2].map((index) => (
                                <button
                                    key={index}
                                    onClick={() => {
                                        sectionsRef.current[index]?.scrollIntoView({ behavior: 'smooth' });
                                    }}
                                    className={`h-3 w-3 rounded-full transition-all ${activeSection === index ? 'bg-primary scale-125' : 'bg-neutral-300'}`}
                                    aria-label={`Go to section ${index + 1}`}
                                />
                            ))}
                        </div>
                    </div>
                    {/* Hero Section */}
                    <section
                        ref={(el) => {
                            if (el) sectionsRef.current[0] = el;
                        }}
                        className="flex min-h-screen w-full max-w-7xl snap-start flex-col justify-center py-20 text-center"
                    >
                        <h1 className="mb-10 text-5xl font-bold tracking-tight sm:text-6xl">GeoProxy</h1>
                        <p className="text-muted-foreground mx-auto mb-16 max-w-3xl text-xl">
                            Level up your location game with GeoProxy. Proxies at your fingertips. Stay anonymous, bypass restrictions.
                        </p>
                    </section>

                    {/* Features Section */}
                    <section
                        id="features"
                        ref={(el) => {
                            if (el) sectionsRef.current[1] = el;
                        }}
                        className="flex min-h-screen w-full max-w-7xl snap-start flex-col justify-center py-20"
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

                    {/* Download Section */}
                    <section
                        id="download"
                        ref={(el) => {
                            if (el) sectionsRef.current[2] = el;
                        }}
                        className="flex min-h-screen w-full max-w-7xl snap-start flex-col justify-center py-12"
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
                                                className="w-full"
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
            </AppShell>
        </>
    );
}
