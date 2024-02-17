import React from 'react'

function Footer() {
    return (
        <footer className="footer footer-center p-4 bg-base-300 text-base-content">
            <aside>
                <p>© GeoIP. {(new Date ().getFullYear ())} - Create with <span className="text-primary text-lg">&hearts;</span> by <a className="hover:text-secondary underline decoration-dashed" href="https://notcoderguy.com/">NotCoderGuy</a>  </p>
            </aside>
        </footer>
    )
}

export default Footer