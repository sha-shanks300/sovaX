#!/usr/bin/env python3
# sovax.py

import pyfiglet
import argparse
from modules.crt_enum2 import enumerate_subdomains
from modules.whois_dns import fetch_whois_info
from modules.dnslookup import resolve_with_resolver, print_results
from modules.wayback_fetcher import fetch_wayback_urls, filter_interesting_urls


def print_banner():
    banner = pyfiglet.figlet_format("sovaX", font="graffiti")
    print(banner)


def passive_recon(domain):
    print(f"\n[*] Starting Passive Recon for: {domain}")

    # Subdomain enumeration
    print("\n[+] Enumerating Subdomains...\n")
    subdomains = enumerate_subdomains(domain)
    if subdomains:
        for sub in subdomains:
            print(f"  - {sub}")
    else:
        print("  [!] No subdomains found.")

    # WHOIS Lookup
    print("\n[+] Fetching WHOIS Info...\n")
    whois_data = fetch_whois_info(domain)
    if whois_data:
        for key, value in whois_data.items():
            print(f"{key}: {value}")
    else:
        print("  [!] WHOIS lookup failed.")

    # DNS Lookup
    print("\n[+] Performing DNS Resolution (Passive)...\n")
    dns_results = resolve_with_resolver(domain, resolver_ip="8.8.8.8")
    print_results("DNS Records via Public Resolver (8.8.8.8)", dns_results)

    # Wayback Machine URLs
    print("\n[+] Extracting URLs from Wayback Machine...\n")
    wayback_urls = fetch_wayback_urls(domain)
    if wayback_urls:
        filtered = filter_interesting_urls(wayback_urls)
        if filtered:
            print(f"[+] Found {len(filtered)} potentially interesting URLs:\n")
            for url in filtered:
                print(f"  - {url}")
        else:
            print("[!] No interesting URLs found.")
    else:
        print("[!] No Wayback data found.")


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="sovaX - Passive Recon Toolkit")
    parser.add_argument("-p", "--passive", help="Run passive recon on target domain", metavar="DOMAIN")
    args = parser.parse_args()

    if args.passive:
        passive_recon(args.passive.strip())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
