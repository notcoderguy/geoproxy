import { AppShell } from '@/components/app-shell';
import { AppSidebar } from '@/components/app-sidebar';
import { Head } from '@inertiajs/react';
import { MobileNavbar } from '@/components/mobile-navbar'; // <-- Add this import

export default function Home() {
    return (
        <>
            <Head title="Home"></Head>

            <AppShell variant="sidebar">
                <AppSidebar />
                <div className="bg-background text-foreground relative flex min-h-screen w-full snap-y snap-mandatory flex-col items-center overflow-y-auto px-4 [-ms-overflow-style:none] [scrollbar-width:none] sm:px-6 lg:px-8 [&::-webkit-scrollbar]:hidden">
                    <section
                        className="flex min-h-screen w-full max-w-7xl snap-start flex-col justify-center py-20 text-center"
                    >
                        <h1 className="mb-10 text-5xl font-bold tracking-tight sm:text-6xl">GeoProxy</h1>
                        <p className="text-muted-foreground mx-auto mb-16 max-w-3xl text-xl">
                            Level up your location game with GeoProxy. Proxies at your fingertips. Stay anonymous, bypass restrictions.
                        </p>
                    </section>
                </div>
                <MobileNavbar />
            </AppShell>
        </>
    );
}
