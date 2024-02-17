import React from 'react'

function Docs() {
    return (
        <div class="bg-base-200 flex min-h-screen">
            <nav class="bg-base-300 rounded-lg text-content-text font-medium p-4 w-64 hidden sm:block">
                <div class="sticky top-10 pl-3">
                    <ul>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#getting-started">Getting Started</a>
                        </li>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#api">API</a>
                        </li>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#rate-limiting">Rate Limiting</a>
                        </li>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#error-handling">Error Handling</a>
                        </li>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#privacy-policy">Privacy Policy</a>
                        </li>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#terms-of-service">Terms of Service</a>
                        </li>
                        <li
                            class="mb-2 transition-transform transform hover:text-secondary hover:underline hover:decoration-dashed">
                            <a href="#contact">Contact</a>
                        </li>
                    </ul>
                </div>
            </nav>

            <div class="flex-1 md:space-y-12 p-8">
                <h1 class="text-3xl font-medium sm:text-5xl mb-16">Documentation</h1>

                <section id="getting-started" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># Getting Started</h2>
                    <p>Welcome to our geoproxy API, designed specifically for webscrapers and developers. Our service enables you to get proxies, offering customized/ desired proxy for an enhanced browsing/ scraping experience. Start leveraging our API today to get proxy with different locations and best possible anonymity—no signup required.</p>
                </section>

                <section id="api" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># API</h2>
                    <p>Our API grants access to HTTP, SOCKS4/5 proxy data, including the country code, google_pass, and anonymity, to provide tailored content and services. Utilize our endpoints:</p>
                    <ul>
                        <li class="py-1"><code class="bg-base-content text-base-100 p-1">/[TYPE]</code> - Enter the desired type of proxy (HTTP, SOCKS4, or SOCKS5).</li>
                        <li class="py-1"><code class="bg-base-content text-base-100 p-1">/[TYPE]?format=[FORMAT]</code> - Retrieves proxy data for a specified query and requirement.</li>
                    </ul>
                    <p>There are other query parameters that can be added to the URL. Which contains google_pass, anonymity, and amount. For example, <code class="bg-base-content text-base-100 p-1">/[TYPE]?format=[FORMAT]&google_pass=[GOOGLE_PASS]&anonymity=[ANONYMITY]&amount=[AMOUNT]</code>. See README in Github for more details.</p>
                </section>

                <section id="rate-limiting" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># Rate Limiting</h2>
                    <p>Our API is designed to accommodate a wide range of requests without stringent rate limits. In the rare
                        event of excessive requests, such as a DDos attack, we ensure stability by rate limiting to protect our
                        services.</p>
                </section>

                <section id="error-handling" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># Error Handling</h2>
                    <p>Our system is built to manage errors efficiently, ensuring you receive optimal output. In case of an
                        incorrect IP format, the API will respond with an error, guiding you to correct the request.</p>
                </section>

                <section id="privacy-policy" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># Privacy Policy</h2>
                    <p>Your privacy is paramount. Our service does not log or collect any user data, ensuring full anonymity and
                        security in your use of our API.</p>
                </section>

                <section id="terms-of-service" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># Terms of Service</h2>
                    <p>By using our service, you agree to our terms, crafted to ensure a safe and reliable experience. While we
                        impose no specific restrictions, we encourage responsible use of our API.</p>
                </section>

                <section id="contact" class="mb-8">
                    <h2 class="text-secondary text-3xl font-medium mb-4"># Contact</h2>
                    <p>For support or inquiries, reach out directly on Discord (@notcoderguy). Please include all relevant
                        details in your initial message to ensure a swift and accurate response.</p>
                </section>

            </div>

        </div>
    )
}

export default Docs