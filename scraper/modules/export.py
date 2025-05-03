import os
import json
import csv
import logging
from .db import ProxyDB

logger = logging.getLogger(__name__)

def export_proxies():
    """Export active proxies to txt, csv and json files"""
    db = ProxyDB()
    output_dir = os.path.join(os.getcwd(), 'proxies')
    os.makedirs(output_dir, exist_ok=True)
    
    # Define protocols and their export settings
    protocols = {
        'http': {},
        'socks4': {}, 
        'socks5': {}
    }
    
    # Get all active proxies in one query per protocol
    for protocol in protocols:
        protocols[protocol]['proxies'] = db.get_active_proxies_by_protocol(protocol)
    
    # Export each protocol's proxies in all formats
    for protocol, data in protocols.items():
        proxies = data['proxies']
        if not proxies:
            continue
            
        base_path = os.path.join(output_dir, f"{protocol}_proxies")
        
        # TXT export (formatted proxy details)
        with open(f"{base_path}.txt", 'w') as f:
            for p in proxies:
                f.write(f"{p['proxy']},{p.get('response_time',0)},{p.get('google_pass',False)},"
                        f"{p.get('anonymity','Unknown')},{p.get('country','Unknown')}\n")
        
        # CSV export (selected details)
        with open(f"{base_path}.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['proxy', 'response_time', 'google_pass', 'anonymity', 'country', 'city', 'isp'])
            writer.writerows(
                [p['proxy'], p.get('response_time',0), p.get('google_pass',False),
                 p.get('anonymity','Unknown'), p.get('country','Unknown'),
                 p.get('city','Unknown'), p.get('isp','Unknown')]
                for p in proxies
            )
        
        # JSON export (filtered objects)
        with open(f"{base_path}.json", 'w') as f:
            filtered_proxies = [{
                'proxy': p['proxy'],
                'response_time': p.get('response_time',0),
                'google_pass': p.get('google_pass',False),
                'anonymity': p.get('anonymity','Unknown'),
                'country': p.get('country','Unknown'),
                'city': p.get('city','Unknown'),
                'isp': p.get('isp','Unknown')
            } for p in proxies]
            json.dump(filtered_proxies, f, indent=2)
    
    logger.info(f"Exported proxies to {output_dir}")

def app():
    """Main export function"""
    logger.info("Starting proxy export")
    export_proxies()
    logger.info("Proxy export completed")
