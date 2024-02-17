import React from 'react'

function Error() {
    return (
        <div className="relative flex items-top justify-center min-h-screen bg-base sm:items-center sm:pt-0">
            <div className="max-w-xl mx-auto sm:px-6 lg:px-8">
                <div className="flex items-center pt-8 sm:justify-start sm:pt-0">
                    <div className="px-4 text-lg text-base-content border-r border-white tracking-wider">
                        Error
                    </div>

                    <div className="ml-4 text-lg text-base-content uppercase tracking-wider">
                        Page Not Found
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Error