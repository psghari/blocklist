import requests
import urllib3
from pathlib import Path

FJ_URL = "https://gitlab.com/fusionjack/adhell3-hosts/-/raw/master/hosts"
ALLOWLIST_FILE = "allowlist.txt"
SEED_OUTPUT = "fj_seed.txt"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_allowlist():
    if not Path(ALLOWLIST_FILE).exists():
        return set()
    with open(ALLOWLIST_FILE) as f:
        return set(line.strip().lower().lstrip("*.") for line in f if line.strip())

def fetch_fj():
    print("Fetching Fusionjack list...")
    r = requests.get(FJ_URL, timeout=15, verify=False)
    r.raise_for_status()
    lines = r.text.splitlines()
    domains = set()
    for line in lines:
        line = line.strip().lower()
        if not line or line.startswith("#"):
            continue
        if "*" in line or "." in line:
            domains.add(line)
    return domains

def save(domains):
    with open(SEED_OUTPUT, "w") as f:
        for d in sorted(domains):
            f.write(d + "\n")
    print(f"Saved {len(domains)} to {SEED_OUTPUT}")

def main():
    allowlist = load_allowlist()
    raw = fetch_fj()
    filtered = {d for d in raw if d.lstrip("*.") not in allowlist}
    save(filtered)

if __name__ == "__main__":
    main()
