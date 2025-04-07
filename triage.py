from pathlib import Path

NEXTDNS_LOG = "nextdns_log.txt"
ALLOWLIST_FILE = "allowlist.txt"
OUTPUT_BLOCKLIST = "auto_block.txt"

def load_allowlist():
    if not Path(ALLOWLIST_FILE).exists():
        return set()
    return set(line.strip().lower() for line in open(ALLOWLIST_FILE) if line.strip())

def parse_log():
    raw = Path(NEXTDNS_LOG).read_text().lower()
    domains = set(line.strip() for line in raw.splitlines() if line.strip())
    return domains

def main():
    if not Path(NEXTDNS_LOG).exists():
        print("No log file found.")
        return

    allowlist = load_allowlist()
    all_domains = parse_log()
    blocked = sorted(d for d in all_domains if d not in allowlist)

    with open(OUTPUT_BLOCKLIST, "w") as f:
        for d in blocked:
            f.write(f"0.0.0.0 {d}\n")

    print(f"🔥 Blocked {len(blocked)} domains (everything except allowlist).")
    print(f"✅ Output written to {OUTPUT_BLOCKLIST}")

if __name__ == "__main__":
    main()
