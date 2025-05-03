import logging
import cloudscraper
from ..db import ProxyDB

logger = logging.getLogger(__name__)
db = ProxyDB()

def scrape(progress=None, parent_task=None):
    # We should never create our own progress - always use the provided one
    if progress is None:
        logger.error("No progress bar provided to Monosans scraper")
        return False

    try:
        
        # Create a subtask if we have a parent task
        if parent_task:
            task = progress.add_task("Monosans Scraping", parent=parent_task)
        else:
            task = progress.add_task("Monosans Scraping", total=1)
        # Update progress before starting
        progress.update(task, advance=0, description="Starting Monosans scrape")
        URL = 'https://github.com/monosans/proxy-list/raw/main/proxies.json'
        scraper = cloudscraper.create_scraper()
        r = scraper.get(URL)
        data = r.json()

        SOCKS4 = []
        SOCKS5 = []
        HTTP = []

        for proxy in data:
            if proxy['protocol'] == 'socks4':
                socks4_host = proxy['host']
                socks4_port = proxy['port']
                socks4 = f'{socks4_host}:{socks4_port}'
                SOCKS4.append(socks4)
            elif proxy['protocol'] == 'socks5':
                socks5_host = proxy['host']
                socks5_port = proxy['port']
                socks5 = f'{socks5_host}:{socks5_port}'
                SOCKS5.append(socks5)
            elif proxy['protocol'] == 'http':
                http_host = proxy['host']
                http_port = proxy['port']
                http = f'{http_host}:{http_port}'
                HTTP.append(http)

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

        logger.info('Scraping from monosans.github.io completed')
        return True
    except Exception as e:
        logger.error(f'Scraping from monosans.github.io failed: {str(e)}')
        return False
