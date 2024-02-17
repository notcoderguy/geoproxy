import re
import cloudscraper
from colorama import init, Fore, Style
from rich.progress import track, Progress, BarColumn, TextColumn
from rich.console import Console
from time import sleep

init()
console = Console()

def checker(FILE, DATA):
    """
    Function to check for the presence of each item in DATA within the file specified by FILE, and append it to the file if not present.
    
    Parameters:
    FILE (str): The file to be checked and potentially updated.
    DATA (list): The list of data items to be checked within the file.
    
    Returns:
    None
    """
    with open(FILE, 'r') as f:
        proxies = f.readlines()
    proxies = [x.strip() for x in proxies]

    for proxy in DATA:
        if proxy not in proxies:
            with open(FILE, 'a') as f:
                f.write(f'{proxy}\n')
        else:
            continue

def monosansGithub():
    try:
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
                socks4= f'{socks4_host}:{socks4_port}'
                SOCKS4.append(socks4)
            elif proxy['protocol'] == 'socks5':
                socks5_host = proxy['host']
                socks5_port = proxy['port']
                socks5= f'{socks5_host}:{socks5_port}'
                SOCKS5.append(socks5)
            elif proxy['protocol'] == 'http':
                http_host = proxy['host']
                http_port = proxy['port']
                http= f'{http_host}:{http_port}'
                HTTP.append(http)

        checker('data/HTTP.txt', HTTP)
        checker('data/SOCKS4.txt', SOCKS4)
        checker('data/SOCKS5.txt', SOCKS5)

        print(Fore.GREEN + '[+] Scraping from monosans.github.io done.' + Fore.RESET)
    except:
        print(Fore.RED + '[-] Scraping from monosans.github.io failed.' + Fore.RESET)

def spysMe():
    try:
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

        checker('data/HTTP.txt', HTTP)
        checker('data/SOCKS5.txt', SOCKS5)

        print(Fore.GREEN + '[+] Scraping from spys.me done.' + Fore.RESET)
    except:
        print(Fore.RED + '[-] Scraping from spys.me failed.' + Fore.RESET)

def proxyScrape():
    try:
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

        checker('data/HTTP.txt', HTTP)
        checker('data/SOCKS4.txt', SOCKS4)
        checker('data/SOCKS5.txt', SOCKS5)

        print(Fore.GREEN + '[+] Scraping from proxyscrape.com done.' + Fore.RESET)
    except:
        print(Fore.RED + '[-] Scraping from proxyscrape.com failed.' + Fore.RESET)
        
def geoNode():
    try:
        URL = "https://proxylist.geonode.com/api/proxy-list"
        PROXY_SUMMARY = "https://proxylist.geonode.com/api/proxy-summary"

        PARAMS = {
            "limit": "100",
            "page": "1",
            "sort_by": "lastChecked",
            "sort_type": "desc"
        }

        HEADERS = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://geonode.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        SOCKS4 = []
        SOCKS5 = []
        HTTP = []

        scraper = cloudscraper.create_scraper()
        r = scraper.get(PROXY_SUMMARY, headers=HEADERS)
        data = r.json()
        
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(
            complete_style="green",
            pulse_style="dim",
            ),
            TextColumn("[progress.completed]{task.completed}/{task.total}"),
            transient=True,
            console=console
        ) as progress:

            total_pages = data['summary']['proxiesOnline'] // 100 + 1

            fetch_page_task = progress.add_task("Scraping GeoNode...", total=total_pages)

            for page in range(1, total_pages + 1):
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
                progress.update(fetch_page_task, advance=1)

        checker('data/HTTP.txt', HTTP)
        checker('data/SOCKS4.txt', SOCKS4)
        checker('data/SOCKS5.txt', SOCKS5)

        print(Fore.GREEN + '[+] Scraping from geonode.com done.' + Fore.RESET)
    except:
        print(Fore.RED + '[-] Scraping from geonode.com failed.' + Fore.RESET)

def app():
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Starting Scraping..." + Style.RESET_ALL)
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
    
    monosansGithub()
    spysMe()
    proxyScrape()
    geoNode()
    
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Scraping Complete!" + Style.RESET_ALL)
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)