import shutil
import os
import subprocess
import maxminddb
import requests
import time
import socks
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style 
from rich.progress import track, Progress, BarColumn, TextColumn
from rich.console import Console

init()
load_dotenv()
console = Console()

def checker(FILE, DATA, TYPE):
    """
    A function to check if the given data exists in the specified file and add it if it doesn't. 
    Parameters:
    - FILE: the file to be checked and potentially updated
    - DATA: the data to be checked and added to the file if not already present
    - TYPE: the type of operation to be performed on the file ('r' for reading, 'w' for writing, etc.)
    """
    with open(FILE, 'r') as f:
        proxies = f.readlines()
    proxies = [x.strip() for x in proxies]

    if TYPE == 'a':
        for proxy in DATA:
            if proxy not in proxies:
                with open(FILE, TYPE) as f:
                    f.write(f'{proxy}\n')
            else:
                continue
    elif TYPE == 'w':
        with open(FILE, TYPE) as f:
            for proxy in DATA:
                f.write(f'{proxy}\n')
        

def download_mmdb_files(LICENSE_KEY, MMDB_DIRECTORY):
    """
    Download MMDB files from MaxMind using the provided LICENSE_KEY and saving them to the specified MMDB_DIRECTORY.

    Parameters:
    - LICENSE_KEY: str, the license key for accessing the MaxMind API.
    - MMDB_DIRECTORY: str, the directory where the MMDB files will be saved.

    Returns:
    None
    """
    LINK = 'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={}&suffix=tar.gz'.format(LICENSE_KEY)

    download_dir = os.path.join(os.getcwd(), MMDB_DIRECTORY)
    os.makedirs(download_dir, exist_ok=True)
    
    response = requests.get(LINK, stream=True)
    if response.status_code == 200:
        filename = 'MaxMind-Country.tar.gz'
        filepath = os.path.join(download_dir, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
    else:
        print(Fore.RED + f"Failed to download {LINK}: HTTP {response.status_code} - {response.text}" + Fore.RESET)
        

def unzip_mmdb_files(MMDB_DIRECTORY):
    """
    Function to unzip .tar.gz files in the specified MMDB_DIRECTORY.

    Parameters:
    - MMDB_DIRECTORY: the directory containing the .tar.gz files to be extracted.

    Returns:
    - None
    """
    download_dir = os.path.join(os.getcwd(), MMDB_DIRECTORY)
    for filename in os.listdir(download_dir):
        if filename.endswith('.tar.gz'):
            subprocess.run(
                ['tar', '-xzf', os.path.join(download_dir, filename), '-C', download_dir],
                check=True
            )

def clean_up_mmdb_files(MMDB_DIRECTORY):
    """
    Function to clean up MMDB files in the specified directory.

    Parameters:
    MMDB_DIRECTORY (str): The directory containing the MMDB files to be cleaned up.

    Returns:
    None
    """
    download_dir = os.path.join(os.getcwd(), MMDB_DIRECTORY)
    for filename in os.listdir(download_dir):
        if filename.endswith('.tar.gz'):
            os.remove(os.path.join(download_dir, filename))

def move_mmdb_files(MMDB_DIRECTORY):
    """
    Move .mmdb files from the specified MMDB_DIRECTORY to the current working directory.
    """
    search_dir = os.path.join(os.getcwd(), MMDB_DIRECTORY)
    for folder in os.listdir(search_dir):
        if folder.startswith('GeoLite2'):
            folder_path = os.path.join(search_dir, folder)
            for file in os.listdir(folder_path):
                if file.endswith('.mmdb'):
                    source_path = os.path.join(folder_path, file)
                    destination_path = os.path.join(search_dir, file)
                    shutil.move(source_path, destination_path)
                else:
                    os.remove(os.path.join(folder_path, file))
            shutil.rmtree(folder_path)
            
def mmdb_controller(LICENSE_KEY, MMDB_DIRECTORY):
    """
    This function controls the process of downloading, unzipping, moving, and cleaning up MMDB files.
    It takes in the LICENSE_KEY and MMDB_DIRECTORY as parameters.
    """
    download_mmdb_files(LICENSE_KEY, MMDB_DIRECTORY)
    unzip_mmdb_files(MMDB_DIRECTORY)
    move_mmdb_files(MMDB_DIRECTORY)
    clean_up_mmdb_files(MMDB_DIRECTORY)
    
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
    
def check_http_proxy(proxy, maxmind_reader):
    """
    Check HTTP proxy and return its details.
    
    Args:
        proxy (str): The HTTP proxy to be checked.
        maxmind_reader: The reader object for MaxMind database.
        
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
        
        match = maxmind_reader.get(proxy.split(':')[0])
        country = match['country']['iso_code'] if match and 'country' in match else "Unknown"

        return {
            "proxy": proxy, 
            "avg_ping": avg_ping, 
            "can_access_google": can_access_google, 
            "anonymity": anonymity, 
            "country": country,
            "status": "OK"
        }

    except requests.exceptions.RequestException as e:
        return {"proxy": proxy, "error": "Proxy not reachable: " + str(e), "status": "Error"}
    except Exception as e:
        return {"proxy": proxy, "error": "Error: " + str(e), "status": "Error"}

def check_http_proxies(FILE, READER):
    """
    Check HTTP proxies and update the input file with the valid proxies. 
    Args:
        FILE (str): The file path to read and update the proxies.
        READER: The reader object to use for checking the HTTP proxies.
    Returns:
        None
    """
    results = []
    
    with open(FILE, 'r' ) as f:
        proxies = f.readlines()
    proxies = [x.strip() for x in proxies]
    
    num_threads = 50
    
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(
            complete_style="green",
            pulse_style="dim",
        ),
        "[progress.completed][{task.completed}/{task.total}]",
        transient=True,
        console=console
    ) as progress:
        task_description = Fore.CYAN + "HTTP Checks: " + Style.RESET_ALL
        http_task = progress.add_task(task_description, total=len(proxies))
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_proxy = {executor.submit(check_http_proxy, proxy, READER): proxy for proxy in proxies}
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    print(Fore.RED + f"[-] Proxy {proxy} generated an exception: {exc}" + Style.RESET_ALL)
                progress.update(http_task, advance=1)

    print(Fore.CYAN + '[+] Completed HTTP proxy checks' + Fore.RESET)
    OUT = []
    OLD = []
    for result in results:
        if result['status'] == 'Error':
            old_ip = result['proxy']
            # print(Fore.RED + f'[-] Error: {old_ip}' + Fore.RESET)
            OLD.append(old_ip)
        else:
            data = f'{result["proxy"]},{result["avg_ping"]},{result["can_access_google"]},{result["anonymity"]},{result["country"]}'
            # print(Fore.GREEN + f'[+] OK: {data}' + Fore.RESET)
            OUT.append(data)
            
    checker('out/HTTP.txt', OUT, 'w')
    checker('old/HTTP.txt', OLD, 'a')       
    
    with open(FILE, 'w') as f:
        for proxy in OUT:
            out_ip = proxy.split(',')[0]
            f.write(out_ip + '\n')

def check_sock_proxy(proxy, version, maxmind_reader):
    """
    Check the given SOCK proxy by making a request to a geoip API and returning the proxy details.

    Args:
        proxy (str): The SOCK proxy to be checked.
        version (int): The SOCK protocol version (4 or 5).
        maxmind_reader (obj): The MaxMind GeoIP2 reader instance.

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
        
        match = maxmind_reader.get(proxy.split(':')[0])
        country = match['country']['iso_code'] if match and 'country' in match else "Unknown"
        
        return {
            "proxy": proxy, 
            "avg_ping": avg_ping, 
            "can_access_google": can_access_google, 
            "anonymity": anonymity, 
            "country": country,
            "status": "OK"
        }

    except requests.exceptions.RequestException as e:
        return {"proxy": proxy, "error": "Proxy not reachable: " + str(e), "status": "Error"}
    except Exception as e:
        return {"proxy": proxy, "error": "Error: " + str(e), "status": "Error"}
    finally:
        socks.set_default_proxy()
        socket.socket = original_socket
    
def check_socks_proxies(FILE, VERSION, READER):
    """
    Check SOCKS proxies in the given file and update the file with the valid proxies. 

    Args:
        FILE (str): The file containing the SOCKS proxies.
        VERSION (str): The version of SOCKS protocol to be checked.
        READER: The reader object to read the file.
    
    Returns:
        None
    """
    results = []

    with open(FILE, 'r') as f:
        proxies = f.readlines()
    proxies = [x.strip() for x in proxies]

    num_threads = 50

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(
            complete_style="green",
            pulse_style="dim",
        ),
        "[progress.completed][{task.completed}/{task.total}]",
        transient=True,
        console=console
    ) as progress:
        task_description = Fore.CYAN + f"SOCK{VERSION} Checks: " + Style.RESET_ALL
        sock_task = progress.add_task(task_description, total=len(proxies))

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_proxy = {executor.submit(check_sock_proxy, proxy, VERSION, READER): proxy for proxy in proxies}
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    data = future.result()
                    results.append(data)
                except Exception as exc:
                    print(Fore.RED + f"[-] Proxy {proxy} generated an exception: {exc}" + Style.RESET_ALL)
                progress.update(sock_task, advance=1)
        
    print(Fore.CYAN + f'[+] Completed SOCKS{VERSION} proxy checks' + Fore.RESET)
    OUT = []
    OLD = []
    for result in results:
        if result['status'] == 'Error':
            old_ip = result['proxy']
            # print(Fore.RED + f'[-] Error: {old_ip} - {result["error"]}' + Fore.RESET)
            OLD.append(old_ip)
        else:
            data = f'{result["proxy"]},{result["avg_ping"]},{result["can_access_google"]},{result["anonymity"]},{result["country"]}'
            # print(Fore.GREEN + f'[+] OK: {data}' + Fore.RESET)
            OUT.append(data)
            
            
    checker(f'out/SOCKS{VERSION}.txt', OUT, 'w')
    checker(f'old/SOCKS{VERSION}.txt', OLD, 'a')
    
    with open(FILE, 'w') as f:
        for proxy in OUT:
            out_ip = proxy.split(',')[0]
            f.write(out_ip + '\n')
    
def app():
    """
    A function to initialize the application, get environment variables, create directories if necessary,
    download GeoLite2-Country.mmdb if not found, load the database, and start the proxy check.
    """
    print(Fore.CYAN + '[+} Getting environment variables...' + Fore.RESET)
    LICENSE_KEY = os.getenv('LICENSE_KEY')
    MMDB_DIRECTORY = os.getenv('MMDB_DIRECTORY')
    
    print(Fore.CYAN + '[+] Checking if MMDB_DIRECTORY exists...' + Fore.RESET)
    if not os.path.exists(MMDB_DIRECTORY):
        os.mkdir(MMDB_DIRECTORY)

    print(Fore.CYAN + '[+] Checking if GeoLite2-Country.mmdb exists...' + Fore.RESET)
    if not os.path.exists(os.path.join(os.getcwd(), MMDB_DIRECTORY, 'GeoLite2-Country.mmdb')):
        print(Fore.RED + '[-] GeoLite2-Country.mmdb not found. Downloading...' + Fore.RESET)
        mmdb_controller(LICENSE_KEY, MMDB_DIRECTORY)
        print(Fore.GREEN + '[+] GeoLite2-Country.mmdb downloaded.' + Fore.RESET)
    else:
        print(Fore.CYAN + '[+] GeoLite2-Country.mmdb found.' + Fore.RESET)
        
    print(Fore.CYAN + '[+] Loading GeoLite2-Country.mmdb...' + Fore.RESET)
    reader = maxminddb.open_database(os.path.join(os.getcwd(), MMDB_DIRECTORY, 'GeoLite2-Country.mmdb'), mode=maxminddb.MODE_MEMORY)
    
    if not reader:
        print(Fore.RED + '[-] GeoLite2-Country.mmdb not loaded. Exiting...' + Fore.RESET)
        exit()
        
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Starting Proxy Check" + Style.RESET_ALL)
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
    
    check_http_proxies('data/HTTP.txt', reader)
    check_socks_proxies('data/SOCKS4.txt', 4, reader)
    check_socks_proxies('data/SOCKS5.txt', 5, reader)
    
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Proxy Check Complete" + Style.RESET_ALL)
    print(Fore.MAGENTA + "---------------------" + Style.RESET_ALL)
        

if __name__ == '__main__':
    app()