import logging
import re
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
            task = progress.add_task("Spys.me Scraping", parent=parent_task)
        else:
            task = progress.add_task("Spys.me Scraping", total=1)
        # Update progress before starting
        progress.update(task, advance=0, description="Starting Spys.me scrape")
        HTTP_URL = 'http://spys.me/proxy.txt'
        SOCKS_URL = 'http://spys.me/socks.txt'

        SOCKS5 = []
        HTTP = []

        scraper = cloudscraper.create_scraper()
        r = scraper.get(HTTP_URL)
        http_data = r.text
        r = scraper.get(SOCKS_URL)
        socks_data = r.text

        pattern = re.compile(r'\d{1,3}(?:\.\d{1,3}){3}:\d+')
        http_proxies = pattern.findall(http_data)
        socks_proxies = pattern.findall(socks_data)

        for proxy in http_proxies:
            HTTP.append(proxy)
        for proxy in socks_proxies:
            SOCKS5.append(proxy)

        for proxy in HTTP:
            db.insert_proxy({
                'proxy': proxy,
                'protocol': 'http',
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

        logger.info('Scraping from spys.me completed')
        if own_progress:
            progress.stop()
        return True
    except Exception as e:
        logger.error(f'Scraping from spys.me failed: {str(e)}')
        if own_progress:
            progress.stop()
        return False
