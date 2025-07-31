import requests
import re

def fetch_wayback_urls(domain):
    print(f"\n[+] Fetching Wayback Machine data for: {domain}")
    base_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"{domain}/*",
        "output": "json",
        "fl": "original",
        "collapse": "urlkey"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        urls = [entry[0] for entry in data[1:]]  # skip header
        return urls
    except Exception as e:
        print(f"[!] Error fetching Wayback data: {e}")
        return []

def filter_interesting_urls(urls):
    patterns = [
        r"admin", r"login", r"signin", r"signup",
        r"\.php", r"\.js", r"\.json", r"\.sql", r"\.bak",
        r"\.zip", r"\.tar", r"\.gz",
        r"\.env", r"\.git", r"\.svn",
        r"\?",  # URLs with parameters
    ]
    return list(set(url for url in urls if any(re.search(p, url, re.IGNORECASE) for p in patterns)))
