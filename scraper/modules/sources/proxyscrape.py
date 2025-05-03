import logging
import cloudscraper
from ..db import ProxyDB

logger = logging.getLogger(__name__)
db = ProxyDB()

def scrape(progress=None, parent_task=None):
    if progress is None:
        # Fallback to creating own progress if not provided
        from rich.console import Console
        from rich.progress import Progress, BarColumn, TextColumn
        console = Console()
        progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(complete_style="green"),
            TextColumn("[progress.completed]{task.completed}/{task.total}"),
            transient=True,
            console=console
        )
        own_progress = True
    else:
        own_progress = False

    try:
        if own_progress:
            progress.start()
        
        # Create a subtask if we have a parent task
        if parent_task:
            task = progress.add_task("ProxyScrape Scraping", parent=parent_task)
        else:
            task = progress.add_task("ProxyScrape Scraping", total=1)
        # Update progress before starting
        progress.update(task, advance=0, description="Starting ProxyScrape scrape")
        URL = 'https://api.proxyscrape.com/?request=getproxies&proxytype={type}&timeout=10000&country=all&ssl=all&anonymity=all'

        SOCKS4 = []
        SOCKS5 = []
        HTTP = []

        scraper = cloudscraper.create_scraper()
        r = scraper.get(URL.format(type='socks4'))
        socks4_data = r.text
        r = scraper.get(URL.format(type='socks5'))
        socks5_data = r.text
        r = scraper.get(URL.format(type='http'))
        http_data = r.text

        for proxy in socks4_data.splitlines():
            SOCKS4.append(proxy)
        for proxy in socks5_data.splitlines():
            SOCKS5.append(proxy)
        for proxy in http_data.splitlines():
            HTTP.append(proxy)

        for proxy in HTTP:
            db.insert_proxy({
                'proxy': proxy,
                'protocol': 'http',
                'status': 'unchecked',
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1]
            })
        for proxy in SOCKS4:
            db.insert_proxy({
                'proxy': proxy,
                'protocol': 'socks4',
                'status': 'unchecked',
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1]
            })
        for proxy in SOCKS5:
            db.insert_proxy({
                'proxy': proxy,
                'protocol': 'socks5',
                'status': 'unchecked',
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1]
            })

        logger.info('Scraping from proxyscrape.com completed')
        if own_progress:
            progress.stop()
        return True
    except Exception as e:
        logger.error(f'Scraping from proxyscrape.com failed: {str(e)}')
        if own_progress:
            progress.stop()
        return False
