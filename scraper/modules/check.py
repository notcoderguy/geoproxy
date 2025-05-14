import os
import maxminddb
import requests
import time
import socks
import socket
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from .db import ProxyDB

# Initialize logging
load_dotenv()
logging.basicConfig(
    level=logging.DEBUG if os.getenv('APP_DEBUG', 'false').lower() == 'true' else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database
db = ProxyDB()
console = Console()

    
def check_proxy_anonymity(headers):
    """
    Check the anonymity level of a proxy based on the given headers.

    Parameters:
    - headers: dictionary of HTTP headers

    Returns:
    - A string indicating the anonymity level of the proxy ('Transparent', 'Anonymous', 'Elite')
    """
    is_transparent = 'X-Forwarded-For' in headers or 'X-Real-IP' in headers
    uses_proxy_headers = 'Via' in headers or 'Proxy-Connection' in headers
    
    if is_transparent:
        return 'Transparent'
    elif uses_proxy_headers:
        return 'Anonymous'
    else:
        return 'Elite'
    
def check_http_proxy(proxy, readers):
    """
    Check HTTP proxy and return its details.
    
    Args:
        proxy (str): The HTTP proxy to be checked.
        readers: Tuple of (city_reader, asn_reader) MaxMind database readers.
        
    Returns:
        dict: A dictionary containing details of the proxy, including average ping time, accessibility to Google, anonymity, country, and status.
    """
    proxy_url = f"http://{proxy}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        start_time = time.time()
        response = requests.get("https://geoip.in/api", proxies=proxies, timeout=5)
        if response.status_code != 200:
            raise requests.exceptions.RequestException
        end_time = time.time()
        avg_ping = (end_time - start_time) * 1000
        
        try:
            google_response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
            can_access_google = google_response.status_code == 200
        except requests.exceptions.RequestException:
            can_access_google = False
        
        try:
            header_response = requests.get("https://httpbin.org/get", proxies=proxies, timeout=5)
            headers = header_response.json()['headers']
            anonymity = check_proxy_anonymity(headers)
        except requests.exceptions.RequestException:
            anonymity = "Anonymous"
        
        ip = proxy.split(':')[0]
        # Get country/city from city database
        city_match = readers[0].get(ip)
        country = city_match['country']['iso_code'] if city_match and 'country' in city_match else "Unknown"
        city = city_match['city']['names']['en'] if city_match and 'city' in city_match and 'names' in city_match['city'] else "Unknown"
        
        # Get ISP from ASN database
        asn_match = readers[1].get(ip)
        isp = asn_match['autonomous_system_organization'] if asn_match and 'autonomous_system_organization' in asn_match else "Unknown"

        return {
            "proxy": proxy, 
            "avg_ping": avg_ping, 
            "can_access_google": can_access_google, 
            "anonymity": anonymity, 
            "country": country,
            "city": city,
            "isp": isp,
            "status": "OK"
        }

    except requests.exceptions.RequestException as e:
        ip = proxy.split(':')[0]
        city_match = readers[0].get(ip)
        country = city_match['country']['iso_code'] if city_match and 'country' in city_match else "Unknown"
        city = city_match['city']['names']['en'] if city_match and 'city' in city_match and 'names' in city_match['city'] else "Unknown"
        
        asn_match = readers[1].get(ip)
        isp = asn_match['autonomous_system_organization'] if asn_match and 'autonomous_system_organization' in asn_match else "Unknown"
        return {
            "proxy": proxy,
            "error": "Proxy not reachable: " + str(e),
            "status": "Error",
            "country": country,
            "city": city,
            "isp": isp
        }
    except Exception as e:
        ip = proxy.split(':')[0]
        city_match = readers[0].get(ip)
        country = city_match['country']['iso_code'] if city_match and 'country' in city_match else "Unknown"
        city = city_match['city']['names']['en'] if city_match and 'city' in city_match and 'names' in city_match['city'] else "Unknown"
        
        asn_match = readers[1].get(ip)
        isp = asn_match['autonomous_system_organization'] if asn_match and 'autonomous_system_organization' in asn_match else "Unknown"
        return {
            "proxy": proxy,
            "error": "Error: " + str(e),
            "status": "Error",
            "country": country,
            "city": city,
            "isp": isp
        }

def check_http_proxies(proxy_type, READER):
    """
    Check HTTP proxies and store results in database.
    Args:
        proxy_type (str): The proxy type ('http')
        READER: The MaxMind reader object
    Returns:
        None
    """
    results = []
    now = datetime.now()
    
    # Get proxies from database
    proxies = db.get_proxies_by_protocol(proxy_type)
    if not proxies or not isinstance(proxies, list):
        logger.error(f"No valid proxies found for protocol {proxy_type}")
        return
        
    # Debug log first few proxies
    logger.debug(f"First 3 proxies for {proxy_type}: {proxies[:3]}")
        
    # Validate proxy structure
    valid_proxies = []
    for proxy in proxies:
        if isinstance(proxy, dict):
            if 'proxy' in proxy:
                valid_proxies.append(proxy)
            else:
                logger.warning(f"Proxy missing 'proxy' field: {proxy}")
        else:
            logger.warning(f"Invalid proxy type: {type(proxy)} - {proxy}")
    
    num_threads = 50
    
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(complete_style="green"),
        TextColumn("[progress.completed]{task.completed}/{task.total}"),
        transient=True,
        console=console
    ) as progress:
        task_description = f"Checking {proxy_type.upper()} proxies"
        http_task = progress.add_task(task_description, total=len(valid_proxies))
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_proxy = {executor.submit(check_http_proxy, proxy['proxy'], READER): proxy for proxy in valid_proxies}
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    logger.error(f"Proxy {proxy['proxy']} generated exception: {exc}")
                progress.update(http_task, advance=1)

    logger.info(f"Completed {proxy_type.upper()} proxy checks")
    
    for result in results:
        if result['status'] == 'OK':
            db.insert_proxy({
                'proxy': result['proxy'],
                'response_time': result['avg_ping'],
                'google_pass': result['can_access_google'],
                'anonymity': result['anonymity'],
                'country': result['country'],
                'city': result['city'],
                'isp': result['isp'],
                'status': 'active'
            })
        else:
            db.insert_proxy({
                'proxy': result['proxy'],
                'status': 'inactive',
                'error': result.get('error', ''),
                'country': result.get('country', 'Unknown'),
                'city': result.get('city', 'Unknown'),
                'isp': result.get('isp', 'Unknown')
            })

def check_sock_proxy(proxy, version, readers):
    """
    Check the given SOCK proxy by making a request to a geoip API and returning the proxy details.

    Args:
        proxy (str): The SOCK proxy to be checked.
        version (int): The SOCK protocol version (4 or 5).
        readers: Tuple of (city_reader, asn_reader) MaxMind database readers.
    Returns:
        dict: A dictionary containing the proxy details, including proxy, avg_ping, can_access_google, anonymity, country, and status.
    """
    proxy_url = f"socks{version}://{proxy}"
    parsed_proxy = urlparse(proxy_url)
    socks_type = socks.SOCKS4 if version == 4 else socks.SOCKS5
    
    original_socket = socket.socket
    
    try:
        start_time = time.time()
        
        socks.set_default_proxy(socks_type, parsed_proxy.hostname, parsed_proxy.port)
        socket.socket = socks.socksocket

        response = requests.get("https://geoip.in/api", timeout=5)
        if response.status_code != 200:
            raise requests.exceptions.RequestException
        
        end_time = time.time()
        avg_ping = (end_time - start_time) * 1000
        
        try:
            google_response = requests.get("https://www.google.com", timeout=5)
            can_access_google = google_response.status_code == 200
        except requests.exceptions.RequestException:
            can_access_google = False
        
        try:
            header_response = requests.get("https://httpbin.org/get", timeout=5)
            headers = header_response.json()['headers']
            anonymity = check_proxy_anonymity(headers)
        except requests.exceptions.RequestException:
            anonymity = "Anonymous"
        
        ip = proxy.split(':')[0]
        # Get country/city from city database
        city_match = readers[0].get(ip)
        country = city_match['country']['iso_code'] if city_match and 'country' in city_match else "Unknown"
        city = city_match['city']['names']['en'] if city_match and 'city' in city_match and 'names' in city_match['city'] else "Unknown"
        
        # Get ISP from ASN database
        asn_match = readers[1].get(ip)
        isp = asn_match['autonomous_system_organization'] if asn_match and 'autonomous_system_organization' in asn_match else "Unknown"

        return {
            "proxy": proxy, 
            "avg_ping": avg_ping, 
            "can_access_google": can_access_google, 
            "anonymity": anonymity, 
            "country": country,
            'city': city,
            'isp': isp,
            "status": "OK"
        }

    except requests.exceptions.RequestException as e:
        ip = proxy.split(':')[0]
        city_match = readers[0].get(ip)
        country = city_match['country']['iso_code'] if city_match and 'country' in city_match else "Unknown"
        city = city_match['city']['names']['en'] if city_match and 'city' in city_match and 'names' in city_match['city'] else "Unknown"
        
        asn_match = readers[1].get(ip)
        isp = asn_match['autonomous_system_organization'] if asn_match and 'autonomous_system_organization' in asn_match else "Unknown"
        
        return {
            "proxy": proxy,
            "error": "Proxy not reachable: " + str(e),
            "status": "Error",
            "country": country,
            "city": city,
            "isp": isp
        }
    except Exception as e:
        ip = proxy.split(':')[0]
        city_match = readers[0].get(ip)
        country = city_match['country']['iso_code'] if city_match and 'country' in city_match else "Unknown"
        city = city_match['city']['names']['en'] if city_match and 'city' in city_match and 'names' in city_match['city'] else "Unknown"
        
        asn_match = readers[1].get(ip)
        isp = asn_match['autonomous_system_organization'] if asn_match and 'autonomous_system_organization' in asn_match else "Unknown"
        
        return {
            "proxy": proxy,
            "error": "Error: " + str(e),
            "status": "Error",
            "country": country,
            "city": city,
            "isp": isp
        }
    finally:
        socks.set_default_proxy()
        socket.socket = original_socket
    
def check_socks_proxies(proxy_type, version, READER):
    """
    Check SOCKS proxies and store results in database.
    
    Args:
        proxy_type (str): The proxy type ('socks4' or 'socks5')
        version (int): The SOCKS protocol version (4 or 5)
        READER: The MaxMind reader object
    
    Returns:
        None
    """
    results = []
    now = datetime.now()
    
    # Get proxies from database
    proxies = db.get_proxies_by_protocol(proxy_type)
    if not proxies or not isinstance(proxies, list):
        logger.error(f"No valid proxies found for protocol {proxy_type}")
        return
        
    # Validate proxy structure
    valid_proxies = []
    for proxy in proxies:
        if isinstance(proxy, dict) and 'proxy' in proxy:
            valid_proxies.append(proxy)
        else:
            logger.warning(f"Invalid proxy structure: {proxy}")
    
    num_threads = 50

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(complete_style="green"),
        TextColumn("[progress.completed]{task.completed}/{task.total}"),
        transient=True,
        console=console
    ) as progress:
        task_description = f"Checking {proxy_type.upper()} proxies"
        sock_task = progress.add_task(task_description, total=len(valid_proxies))

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_proxy = {executor.submit(check_sock_proxy, proxy['proxy'], version, READER): proxy for proxy in valid_proxies}
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    logger.error(f"Proxy {proxy['proxy']} generated exception: {exc}")
                progress.update(sock_task, advance=1)
        
    logger.info(f"Completed {proxy_type.upper()} proxy checks")
    
    for result in results:
        if result['status'] == 'OK':
            db.insert_proxy({
                'proxy': result['proxy'],
                'response_time': result['avg_ping'],
                'google_pass': result['can_access_google'],
                'anonymity': result['anonymity'],
                'country': result['country'],
                'city': result['city'],
                'isp': result['isp'],
                'status': 'active'
            })
        else:
            db.insert_proxy({
                'proxy': result['proxy'],
                'status': 'inactive',
                'error': result.get('error', ''),
                'country': result.get('country', 'Unknown'),
                'city': result.get('city', 'Unknown'),
                'isp': result.get('isp', 'Unknown')
            })
    
def app():
    """
    Initialize the application, load MMDB database, and start proxy checks.
    """
    logger.info("Initializing proxy checker")
    
    MMDB_DIRECTORY = 'mmdb'
    if not os.path.exists(MMDB_DIRECTORY):
        os.mkdir(MMDB_DIRECTORY)
        logger.info(f"Created MMDB directory: {MMDB_DIRECTORY}")

    # Load city database for country/city info
    city_db_path = os.path.join(os.getcwd(), MMDB_DIRECTORY, 'city.mmdb')
    if not os.path.exists(city_db_path):
        logger.error('city.mmdb not found')
        logger.info('Please download the city.mmdb file manually')
        return
        
    logger.info("Loading city.mmdb")
    city_reader = maxminddb.open_database(city_db_path, mode=maxminddb.MODE_MEMORY)
    
    if not city_reader:
        logger.error('Failed to load city.mmdb')
        return

    # Load ASN database for ISP info
    asn_db_path = os.path.join(os.getcwd(), MMDB_DIRECTORY, 'asn.mmdb')
    if not os.path.exists(asn_db_path):
        logger.error('asn.mmdb not found')
        logger.info('Please download the asn.mmdb file manually')
        return
        
    logger.info("Loading asn.mmdb")
    asn_reader = maxminddb.open_database(asn_db_path, mode=maxminddb.MODE_MEMORY)
    
    if not asn_reader:
        logger.error('Failed to load asn.mmdb')
        return
        
    logger.info("Starting proxy checks")
    
    try:
        check_http_proxies('http', (city_reader, asn_reader))
        check_socks_proxies('socks4', 4, (city_reader, asn_reader))
        check_socks_proxies('socks5', 5, (city_reader, asn_reader))
    except Exception as e:
        logger.error(f"Error during proxy checks: {str(e)}")
    
    logger.info("Proxy checks completed")
        

if __name__ == '__main__':
    app()
