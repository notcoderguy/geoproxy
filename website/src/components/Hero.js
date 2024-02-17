import React from 'react'

function Hero() {
    return (
        <div className="container min-h-screen xl:max-w-7xl mx-auto px-4 py-16 lg:px-8 lg:py-32">
            <div className="text-center">
                <h2 className="text-5xl md:text-6xl lg:text-7xl font-medium mt-6 text-white leading-normal md:leading-tight">
                    <span className="block tracking-normal">Level up your location game with <span className="text-secondary">GeoProxy</span>. Proxies at your fingertips.  <span className="text-secondary">Stay anonymous, bypass restrictions</span>.</span>
                </h2>
                <h3 className="text-xl md:text-2xl lg:text-3xl font-medium text-secondary lg:w-2/3 mx-auto mt-4 md:mt-6">
                </h3>
            </div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-center space-y-2 sm:space-y-0 sm:space-x-2 pt-10 pb-16">
            </div>
        </div>
    )
}

export default Hero