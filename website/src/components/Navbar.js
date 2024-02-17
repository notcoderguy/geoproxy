import { React, useState } from 'react'
import { Link } from 'react-router-dom';

function Navbar() {

    const [isOpen, setIsOpen] = useState(false);

    return (
        <header className="flex flex-none md:items-center py-4 md:py-8">
            <div className="flex flex-col text-center md:flex-row md:items-center md:justify-between space-y-6 md:space-y-0 container xl:max-w-7xl mx-auto px-4 lg:px-8">
                <div className="flex justify-between w-full md:w-auto text-base-content hover:text-secondary">
                    <Link to="/" className="inline-flex items-center space-x-2 font-bold text-lg tracking-wide">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5"
                            stroke="currentColor"
                            className="text-base-content hover:text-secondary hi-outline inline-block w-6 h-6">
                            <path strokeLinecap="round" strokeLinejoin="round"
                                d="M12.75 3.03v.568c0 .334.148.65.405.864l1.068.89c.442.369.535 1.01.216 1.49l-.51.766a2.25 2.25 0 0 1-1.161.886l-.143.048a1.107 1.107 0 0 0-.57 1.664c.369.555.169 1.307-.427 1.605L9 13.125l.423 1.059a.956.956 0 0 1-1.652.928l-.679-.906a1.125 1.125 0 0 0-1.906.172L4.5 15.75l-.612.153M12.75 3.031a9 9 0 0 0-8.862 12.872M12.75 3.031a9 9 0 0 1 6.69 14.036m0 0-.177-.529A2.25 2.25 0 0 0 17.128 15H16.5l-.324-.324a1.453 1.453 0 0 0-2.328.377l-.036.073a1.586 1.586 0 0 1-.982.816l-.99.282c-.55.157-.894.702-.8 1.267l.073.438c.08.474.49.821.97.821.846 0 1.598.542 1.865 1.345l.215.643m5.276-3.67a9.012 9.012 0 0 1-5.276 3.67m0 0a9 9 0 0 1-10.275-4.835M15.75 9c0 .896-.393 1.7-1.016 2.25" />
                        </svg>
                        <span>GeoProxy</span>
                    </Link>

                    <button onClick={() => setIsOpen(!isOpen)} className='text-base-content hover:text-secondary md:hidden'>
                        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" className="h-6 w-6">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7">
                            </path>
                        </svg>
                    </button>
                </div>

                <nav className={` ${isOpen ? 'block' : 'hidden'} relative w-full md:flex md:items-center md:w-auto md:space-x-6`}>
                    <ul className="w-full space-x-0 md:space-x-6 md:flex md:justify-between">
                        <li><Link to="/" className='block py-2 px-3 md:py-0 md:px-0 mt-4 md:inline-block bg-base-300 rounded md:mt-0 text-base-content md:bg-transparent hover:text-secondary'>Home</Link></li>
                        <li><a href="/#downloads" className='block py-2 px-3 md:py-0 md:px-0 mt-4 md:inline-block bg-base-300 rounded md:mt-0 text-base-content md:bg-transparent hover:text-secondary'>Download</a></li>
                        <li><a href="https://api.geoproxy.in/" className='block py-2 px-3 md:py-0 md:px-0 mt-4 md:inline-block bg-base-300 rounded md:mt-0 text-base-content md:bg-transparent hover:text-secondary'>API</a></li>
                        <li><Link to="/docs" className='block py-2 px-3 md:py-0 md:px-0 mt-4 md:inline-block bg-base-300 rounded md:mt-0 text-base-content md:bg-transparent hover:text-secondary'>Docs</Link></li>
                    </ul>

                    <a href="https://github.com/notcoderguy/geoproxy-db" target="_blank" rel="noopener noreferrer">
                        <button className="btn btn-outline btn-secondary w-full md:w-auto mt-4 md:mt-0">Github</button>
                    </a>
                </nav>
            </div>
        </header>
    )
}

export default Navbar