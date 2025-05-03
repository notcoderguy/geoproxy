import time
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
            task = progress.add_task("GeoNode Scraping", parent=parent_task)
        else:
            task = progress.add_task("GeoNode Scraping", total=1)

        URL = "https://proxylist.geonode.com/api/proxy-list"
        PROXY_SUMMARY = "https://proxylist.geonode.com/api/proxy-summary"

        PARAMS = {
            "limit": "100",
            "page": "1",
            "sort_by": "lastChecked",
            "sort_type": "desc"
        }

        HEADERS = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }

        SOCKS4 = []
        SOCKS5 = []
        HTTP = []

        scraper = cloudscraper.create_scraper()
        r = scraper.get(PROXY_SUMMARY, headers=HEADERS)
        data = r.json()
        
        total_pages = data['summary']['proxiesOnline'] // 100 + 1
        progress.update(task, total=total_pages)

        for page in range(1, total_pages + 1):
            try:
                PARAMS['page'] = page
                r = scraper.get(URL, params=PARAMS, headers=HEADERS)
                data = r.json()
                for proxy in data['data']:
                    if proxy['protocols'] == ['http']:
                        HTTP.append(f"{proxy['ip']}:{proxy['port']}")
                    elif proxy['protocols'] == ['socks4']:
                        SOCKS4.append(f"{proxy['ip']}:{proxy['port']}")
                    elif proxy['protocols'] == ['socks5']:
                        SOCKS5.append(f"{proxy['ip']}:{proxy['port']}")
                time.sleep(3)  # Sleep to avoid hitting the server too hard
                progress.update(task, advance=1, description=f"GeoNode Scraping (page {page}/{total_pages})")
            except Exception as e:
                logger.error(f'Error scraping page {page}: {str(e)}')
                progress.update(task, advance=1)

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

        if own_progress:
            progress.stop()
        logger.info('Scraping from geonode.com completed')
        return True
    except Exception as e:
        logger.error(f"Error in GeoNode scraper: {str(e)}")
        if own_progress:
            progress.stop()
        return False
