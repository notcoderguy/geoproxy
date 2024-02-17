import React from 'react'

function Downloads() {
    return (
        <section id="downloads" className="w-full py-12 md:py-24 lg:py-32">
            <div className="container px-4 flex flex-col items-center gap-4 text-center md:gap-6 md:flex-row md:justify-center lg:gap-10">
                <div className="space-y-3 text-center md:text-left">
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">Download the proxies</h2>
                    <p className="mx-auto max-w-[700px] md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed text-gray-400">Get started with the resources you need. Simply click to download.</p>
                </div>
                <div className="grid w-full grid-cols-1 gap-4 md:grid-cols-3 md:gap-6 lg:gap-4">
                    <div className="flex flex-col gap-2">
                        <a href={process.env.PUBLIC_URL + '/proxies/HTTP.txt'} target="_blank" rel="noopener noreferrer" className="inline-flex h-10 items-center rounded-md border px-4 text-sm font-medium shadow-sm gap-2 transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 border-base-300 bg-base-300 hover:bg-secondary hover:text-base-300 focus-visible:ring-gray-300">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <path d="M9 13v-1h6v1"></path>
                                <path d="M11 18h2"></path>
                                <path d="M12 12v6"></path>
                            </svg>
                            <span>HTTP.txt</span>
                        </a>
                    </div>
                    <div className="flex flex-col gap-2">
                        <a href={process.env.PUBLIC_URL + '/proxies/SOCKS4.txt'} target="_blank" rel="noopener noreferrer" className="inline-flex h-10 items-center rounded-md border px-4 text-sm font-medium shadow-sm gap-2 transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 border-base-300 bg-base-300 hover:bg-secondary hover:text-base-300 focus-visible:ring-gray-300">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <path d="M9 13v-1h6v1"></path>
                                <path d="M11 18h2"></path>
                                <path d="M12 12v6"></path>
                            </svg>
                            <span>SOCKS4.txt</span>
                        </a>
                    
                    </div>
                    <div className="flex flex-col gap-2">
                        <a href={process.env.PUBLIC_URL + '/proxies/SOCKS5.txt'} target="_blank" rel="noopener noreferrer" className="inline-flex h-10 items-center rounded-md border px-4 text-sm font-medium shadow-sm gap-2 transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 border-base-300 bg-base-300 hover:bg-secondary hover:text-base-300 focus-visible:ring-gray-300">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
                                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                                <polyline points="14 2 14 8 20 8"></polyline>
                                <path d="M9 13v-1h6v1"></path>
                                <path d="M11 18h2"></path>
                                <path d="M12 12v6"></path>
                            </svg>
                            <span>SOCKS5.txt</span>
                        </a>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default Downloads