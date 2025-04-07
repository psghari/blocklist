import requests
from pathlib import Path

FUSIONJACK_URL = "https://gitlab.com/fusionjack/adhell3-hosts/-/raw/master/hosts"
ALLOWLIST_FILE = "nextdns_allowlist.txt"
SEED_OUTPUT_FILE = "my_blocklist_seed.txt"

def load_allowlist():
    if not Path(ALLOWLIST_FILE).exists():
        return set()
    with open(ALLOWLIST_FILE) as f:
        return set(line.strip().lower().lstrip("*.") for line in f if line.strip())

def fetch_fusionjack_hosts():
    print("Fetching Fusionjack host list...")
    r = requests.get(FUSIONJACK_URL, timeout=15)
    r.raise_for_status()
    lines = r.text.splitlines()
    domains = set()
    for line in lines:
        line = line.strip().lower()
        if not line or line.startswith("#"):
            continue
        if "*" in line:
            domains.add(line)
        elif "." in line:
            domains.add(line)
    return domains

def save_filtered_seed(domains):
    with open(SEED_OUTPUT_FILE, "w") as f:
        for domain in sorted(domains):
            f.write(domain + "\n")
    print(f"Saved {len(domains)} domains to {SEED_OUTPUT_FILE}")

def main():
    allowlist = load_allowlist()
    fusionjack_domains = fetch_fusionjack_hosts()
    filtered = {d for d in fusionjack_domains if d.lstrip("*.") not in allowlist}
    print(f"Fetched: {len(fusionjack_domains)} | After allowlist filter: {len(filtered)}")
    save_filtered_seed(filtered)

if __name__ == "__main__":
    main()