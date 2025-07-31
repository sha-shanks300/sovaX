# modules/dnslookup.py

import dns.resolver

def resolve_with_resolver(domain, resolver_ip=None):
    record_types = ["A", "MX", "NS", "TXT", "CNAME"]
    resolved_data = {}

    resolver = dns.resolver.Resolver()
    if resolver_ip:
        resolver.nameservers = [resolver_ip]
        mode = f"Using custom resolver {resolver_ip} (PASSIVE)"
    else:
        mode = "Using system default resolver (POTENTIALLY ACTIVE)"

    print(f"\n[+] {mode}")
    print(f"[+] Resolving domain: {domain}\n")

    for record in record_types:
        try:
            answers = resolver.resolve(domain, record, lifetime=5)
            resolved_data[record] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            resolved_data[record] = []
        except dns.resolver.NXDOMAIN:
            resolved_data[record] = ["[!] Domain does not exist."]
            break
        except dns.resolver.Timeout:
            resolved_data[record] = ["[!] Query timed out."]
        except Exception as e:
            resolved_data[record] = [f"[!] Error: {e}"]

    return resolved_data

def print_results(title, results):
    print(f"\n=== {title} ===")
    for rtype, records in results.items():
        print(f"{rtype} Records:")
        if records:
            for rec in records:
                print(f"  - {rec}")
        else:
            print("  - No records found.")
        print()
