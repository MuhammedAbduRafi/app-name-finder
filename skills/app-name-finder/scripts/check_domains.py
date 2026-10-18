#!/usr/bin/env python3
"""Check domain availability via RDAP (the modern, free replacement for WHOIS).

Usage:
    python check_domains.py nimbly.com nimbly.app getnimbly.com
    python check_domains.py --names nimbly,taskfox --tlds com,app,io
    python check_domains.py --json ...        # machine-readable output

How it decides:
    RDAP HTTP 200  -> TAKEN      (the registry has a record)
    RDAP HTTP 404  -> AVAILABLE  (no record; still confirm at a registrar,
                                  some names are reserved or "premium" priced)
    anything else  -> UNKNOWN    (registry unreachable / rate-limited / no RDAP)
    If RDAP is unreachable, a DNS lookup is tried: if the name resolves it is
    TAKEN; if it doesn't, the result stays UNKNOWN (unresolving != unregistered).

Network: sends only the domain names being checked, to IANA (to download the
public list of registry RDAP servers) and to each TLD's official registry.
No API keys, no tracking, nothing stored. Standard library only.

Exit code 2 means no network at all (every lookup was UNKNOWN) so the caller
can switch to another checking method.
"""
import argparse
import json
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"

# Used only if the IANA bootstrap list can't be downloaded.
FALLBACK = {
    "com": "https://rdap.verisign.com/com/v1/",
    "net": "https://rdap.verisign.com/net/v1/",
    "app": "https://pubapi.registry.google/rdap/",
    "dev": "https://pubapi.registry.google/rdap/",
    "page": "https://pubapi.registry.google/rdap/",
    "io": "https://rdap.identitydigital.services/rdap/",
}

UA = {"User-Agent": "app-name-finder/1.0 (domain availability check)",
      "Accept": "application/rdap+json, application/json"}


def load_bootstrap(timeout=8):
    try:
        req = urllib.request.Request(BOOTSTRAP_URL, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
        table = {}
        for tlds, urls in data.get("services", []):
            https = [u for u in urls if u.startswith("https")] or urls
            for t in tlds:
                table[t.lower()] = https[0].rstrip("/") + "/"
        return table
    except Exception:
        return {}


def dns_resolves(domain):
    try:
        socket.getaddrinfo(domain, None)
        return True
    except Exception:
        return False


def check(domain, servers, timeout=10):
    domain = domain.strip().lower().rstrip(".")
    tld = domain.rsplit(".", 1)[-1]
    base = servers.get(tld) or FALLBACK.get(tld)
    result = {"domain": domain, "status": "UNKNOWN", "detail": ""}
    if base:
        try:
            req = urllib.request.Request(f"{base}domain/{domain}", headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status == 200:
                    result.update(status="TAKEN", detail="registry record exists")
                    return result
        except urllib.error.HTTPError as e:
            if e.code == 404:
                result.update(status="AVAILABLE", detail="no registry record (404)")
                return result
            result["detail"] = f"RDAP HTTP {e.code}"
        except Exception as e:
            result["detail"] = f"RDAP unreachable ({type(e).__name__})"
    else:
        result["detail"] = f"no RDAP server known for .{tld}"
    if dns_resolves(domain):
        result.update(status="TAKEN", detail=result["detail"] + "; resolves in DNS")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("domains", nargs="*")
    ap.add_argument("--names", help="comma-separated base names (no TLD)")
    ap.add_argument("--tlds", default="com", help="comma-separated TLDs for --names")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    domains = list(a.domains)
    if a.names:
        for n in a.names.split(","):
            for t in a.tlds.split(","):
                if n.strip() and t.strip():
                    domains.append(f"{n.strip()}.{t.strip().lstrip('.')}")
    if not domains:
        ap.error("give domains or --names")

    servers = load_bootstrap()
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda d: check(d, servers), domains))

    if a.json:
        print(json.dumps(results, indent=2))
    else:
        w = max(len(r["domain"]) for r in results)
        for r in results:
            print(f"{r['domain']:<{w}}  {r['status']:<9}  {r['detail']}")

    sys.exit(2 if all(r["status"] == "UNKNOWN" for r in results) else 0)


if __name__ == "__main__":
    main()
