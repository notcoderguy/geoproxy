import { Head } from '@inertiajs/react';
import { useEffect, useRef, useState } from 'react';
import { AppShell } from '@/components/app-shell';
import { AppSidebar } from '@/components/app-sidebar';
import Heading from '@/components/heading';
import { Button } from '@/components/ui/button';

const features = [
    {
        title: 'Comprehensive Proxy Information',
        description: 'Detailed data on each proxy, including IP, port, and location'
    },
    {
        title: 'Google passed & Elite Proxies',
        description: 'High quality proxies that pass Google verification'
    },
    {
        title: 'Geolocation Insights',
        description: 'Detailed location data for each proxy'
    },
    {
        title: 'Developer-Friendly API',
        description: 'Easy integration with your applications'
    },
    {
        title: 'Regular Database Updates',
        description: 'Fresh proxies every 30 minutes'
    },
    {
        title: 'Multiple Protocols',
        description: 'HTTP, SOCKS4, SOCKS5 support'
    }
];

const downloadOptions = [
    {
        type: 'HTTP',
        formats: ['txt', 'json', 'csv'],
        links: ['/proxies/http_proxies.txt', '/proxies/http_proxies.json', '/proxies/http_proxies.csv']
    },
    {
        type: 'SOCKS4',
        formats: ['txt', 'json', 'csv'],
        links: ['/proxies/socks4_proxies.txt', '/proxies/socks4_proxies.json', '/proxies/socks4_proxies.csv']
    },
    {
        type: 'SOCKS5',
        formats: ['txt', 'json', 'csv'],
        links: ['/proxies/socks5_proxies.txt', '/proxies/socks5_proxies.json', '/proxies/socks5_proxies.csv']
    }
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
            if (Math.abs(scrollPosition - (currentSection * windowHeight)) < windowHeight * 0.3) {
                isScrolling = true;
                window.scrollTo({
                    top: currentSection * windowHeight,
                    behavior: 'smooth'
                });
                
                scrollTimeout = setTimeout(() => {
                    isScrolling = false;
                }, 500);
            }
            
            // Update active section indicator
            sectionsRef.current.forEach((section, index) => {
                if (section && section.offsetTop <= scrollPosition + (windowHeight / 2) && 
                    section.offsetTop + section.offsetHeight > scrollPosition + (windowHeight / 2)) {
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

                <div className="relative flex min-h-screen w-full flex-col items-center bg-background px-4 py-12 text-foreground sm:px-6 lg:px-8 overflow-y-auto snap-y snap-mandatory [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden">
                    {/* Section Navigation */}
                    <div className="fixed right-8 top-1/2 transform -translate-y-1/2 hidden lg:block">
                        <div className="flex flex-col items-center space-y-4">
                            {[0, 1, 2].map((index) => (
                                <button
                                    key={index}
                                    onClick={() => {
                                        sectionsRef.current[index]?.scrollIntoView({ behavior: 'smooth' });
                                    }}
                                    className={`w-3 h-3 rounded-full transition-all ${activeSection === index ? 'bg-primary scale-125' : 'bg-neutral-300'}`}
                                    aria-label={`Go to section ${index + 1}`}
                                />
                            ))}
                        </div>
                    </div>
                    {/* Hero Section */}
                    <section 
                        ref={el => { if (el) sectionsRef.current[0] = el }}
                        className="w-full min-h-screen max-w-7xl py-20 text-center flex flex-col justify-center snap-start"
                    >
                        <h1 className="mb-10 text-5xl font-bold tracking-tight sm:text-6xl">GeoProxy</h1>
                        <p className="mx-auto mb-16 max-w-3xl text-xl text-muted-foreground">
                            Level up your location game with GeoProxy. Proxies at your fingertips. Stay anonymous, bypass restrictions.
                        </p>
                    </section>

                    {/* Features Section */}
                    <section 
                        id="features"
                        ref={el => { if (el) sectionsRef.current[1] = el }}
                        className="w-full min-h-screen max-w-7xl py-20 flex flex-col justify-center snap-start"
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
                        ref={el => { if (el) sectionsRef.current[2] = el }}
                        className="w-full min-h-screen max-w-7xl py-12 flex flex-col justify-center snap-start"
                    >
                        <Heading
                            title="Download the proxies"
                            description="Get started with the resources you need. Simply click to download."
                        />

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
                                                }
                                                }
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
