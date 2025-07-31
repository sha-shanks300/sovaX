import whois
import requests

def fetch_rdap_fallback(domain):
    """
    Fallback using rdap.org if whois.whois() fails.
    No API key required. Free and reliable.
    """
    try:
        url = f"https://rdap.org/domain/{domain}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "Domain Name": data.get("ldhName", "Unavailable"),
            "Registrar": data.get("registrar", {}).get("name", "Unavailable"),
            "Creation Date": next((e.get("eventDate") for e in data.get("events", []) if e["eventAction"] == "registration"), "Unavailable"),
            "Expiration Date": next((e.get("eventDate") for e in data.get("events", []) if e["eventAction"] == "expiration"), "Unavailable"),
            "Updated Date": next((e.get("eventDate") for e in data.get("events", []) if e["eventAction"] == "last changed"), "Unavailable"),
            "Name Servers": [ns.get("ldhName") for ns in data.get("nameservers", [])] or "Unavailable",
            "Status": data.get("status", "Unavailable"),
            "Registrant Country": extract_country(data)
        }

    except Exception as e:
        print(f"[!] RDAP lookup failed: {e}")
        return None

def extract_country(data):
    """
    Attempts to extract registrant country from RDAP data.
    """
    for entity in data.get("entities", []):
        if "registrant" in entity.get("roles", []):
            vcard_array = entity.get("vcardArray", [])
            if len(vcard_array) > 1:
                for item in vcard_array[1]:
                    if item[0] == "adr" and len(item) >= 4:
                        return item[3][-1] if isinstance(item[3], list) else item[3]
    return "Unavailable"

def fetch_whois_info(domain):
    """
    Primary WHOIS lookup using python-whois.
    Falls back to RDAP if WHOIS fails or returns incomplete data.
    """
    try:
        w = whois.whois(domain)

        result = {
            "Domain Name": w.domain_name or "Unavailable",
            "Registrar": w.registrar or "Unavailable",
            "Creation Date": str(w.creation_date) if w.creation_date else "Unavailable",
            "Expiration Date": str(w.expiration_date) if w.expiration_date else "Unavailable",
            "Updated Date": str(w.updated_date) if w.updated_date else "Unavailable",
            "Name Servers": w.name_servers or "Unavailable",
            "Status": w.status or "Unavailable",
            "Registrant Country": w.country or "Unavailable"
        }

        # If data is too sparse, fallback to RDAP
        if result["Domain Name"] in [None, "Unavailable"] or result["Registrar"] == "Unavailable":
            print("[*] WHOIS info incomplete, falling back to RDAP...")
            rdap_data = fetch_rdap_fallback(domain)
            return rdap_data or result

        return result

    except Exception as e:
        print(f"[!] WHOIS lookup failed: {e}")
        print("[*] Falling back to RDAP...")
        return fetch_rdap_fallback(domain)

# Example usage for testing directly
if __name__ == "__main__":
    domain = input("Enter domain (e.g. example.com): ").strip()
    data = fetch_whois_info(domain)

    if data:
        print("\n[+] WHOIS/RDAP Information:\n")
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("[!] No WHOIS info retrieved.")
