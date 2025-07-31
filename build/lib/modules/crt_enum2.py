import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------------------------
# Helper to fetch from crt.sh JSON API
# --------------------------
def fetch_crtsh_json(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        subdomains = set()
        for entry in data:
            name_value = entry.get("name_value", "")
            subdomains.update(name_value.split("\n"))

        print("[+] crt.sh JSON successful.")
        return subdomains

    except Exception as e:
        print(f"[!] crt.sh JSON failed: {e}")
        return set()

# --------------------------
# Fallback: HTML scraping if JSON fails
# --------------------------
def fetch_crtsh_html(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        subdomains = set()

        for td in soup.find_all("td"):
            if domain in td.text:
                subdomains.update(td.text.strip().split())

        print("[+] crt.sh HTML fallback successful.")
        return subdomains

    except Exception as e:
        print(f"[!] crt.sh HTML failed: {e}")
        return set()

# --------------------------
# ThreatCrowd API
# --------------------------
def fetch_threatcrowd(domain):
    try:
        url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
        response = requests.get(url, timeout=10)
        data = response.json()
        subs = set(data.get("subdomains", []))
        print("[+] ThreatCrowd successful.")
        return subs

    except Exception as e:
        print(f"[!] ThreatCrowd failed: {e}")
        return set()

# --------------------------
# BufferOver API
# --------------------------
def fetch_bufferover(domain):
    try:
        url = f"https://dns.bufferover.run/dns?q=.{domain}"
        response = requests.get(url, timeout=10)
        data = response.json()
        subs = set()

        for entry in data.get("FDNS_A", []):
            parts = entry.split(",")
            if len(parts) > 1 and domain in parts[1]:
                subs.add(parts[1].strip())

        print("[+] BufferOver successful.")
        return subs

    except Exception as e:
        print(f"[!] BufferOver failed: {e}")
        return set()

# --------------------------
# AlienVault API
# --------------------------
def fetch_alienvault(domain):
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        response = requests.get(url, timeout=10)
        data = response.json()
        subs = {r["hostname"] for r in data.get("passive_dns", []) if domain in r["hostname"]}
        print("[+] AlienVault successful.")
        return subs

    except Exception as e:
        print(f"[!] AlienVault failed: {e}")
        return set()

# --------------------------
# Wrapper for concurrent execution
# --------------------------
def enumerate_subdomains(domain):
    all_subdomains = set()

    # List of sources
    sources = [
        fetch_crtsh_json,
        fetch_threatcrowd,
        fetch_bufferover,
        fetch_alienvault
    ]

    # First run concurrent methods
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_func = {executor.submit(func, domain): func.__name__ for func in sources}

        for future in as_completed(future_to_func):
            result = future.result()
            all_subdomains.update(result)

    # If crt.sh JSON failed, try HTML as fallback
    if not any("crt.sh JSON" in k for k in future_to_func.values()) or not any("crt.sh" in sub for sub in all_subdomains):
        all_subdomains.update(fetch_crtsh_html(domain))

    return sorted(all_subdomains)


# --------------------------
# Main execution
# --------------------------
if __name__ == "__main__":
    domain = input("Enter domain (e.g. example.com): ").strip()
    print("[*] Enumerating subdomains...\n")

    results = enumerate_subdomains(domain)

    if results:
        print(f"\n[+] Found {len(results)} unique subdomains:")
        for sub in results:
            print(sub)
    else:
        print("[!] No subdomains found.")
