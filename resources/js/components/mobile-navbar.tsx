import { Home, LayoutGrid, Download } from 'lucide-react';
import { Link } from '@inertiajs/react';

export function MobileNavbar() {
    return (
        <nav className="fixed bottom-0 left-0 right-0 z-50 flex h-14 items-center justify-around bg-background border-t sm:hidden">
            <Link href="/" className="flex flex-col items-center text-xs">
                <Home size={20} />
                Home
            </Link>
            <Link href="/features" className="flex flex-col items-center text-xs">
                <LayoutGrid size={20} />
                Features
            </Link>
            <Link href="/downloads" className="flex flex-col items-center text-xs">
                <Download size={20} />
                Downloads
            </Link>
        </nav>
    );
}