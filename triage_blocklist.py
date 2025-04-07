import sqlite3
from pathlib import Path
from datetime import datetime
import re

# Configs
NEXTDNS_LOG = "nextdns_log.txt"
ALLOWLIST_FILE = "nextdns_allowlist.txt"
SEED_LIST_FILE = "my_blocklist_seed.txt"
FIREBASE_DOMAINS = [,
    "firebaselogging-pa.googleapis.com",
    "firebase-settings.crashlytics.com",
    "crashlyticsreports-pa.googleapis.com",
    "firebase.analytics.com",
    "in.appmessaging.googleapis.com",
    "firebaseinappmessaging.googleapis.com",
    "firestore.googleapis.com",
]
DB_FILE = "domain_score.db"
PROMOTION_SCORE = 5
MAX_EXPORT = 10000

# Setup database
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS domains (
        domain TEXT PRIMARY KEY,
        first_seen TEXT,
        last_seen TEXT,
        hit_count INTEGER,
        score INTEGER,
        status TEXT
    )
''')
conn.commit()

def load_allowlist():
    if not Path(ALLOWLIST_FILE).exists():
        return set()
    with open(ALLOWLIST_FILE) as f:
        return set(line.strip().lower() for line in f if line.strip())

def load_seed_list():
    if not Path(SEED_LIST_FILE).exists():
        return set()
    with open(SEED_LIST_FILE) as f:
        return set(line.strip().lower() for line in f if line.strip())

def parse_domains_from_log():
    text = Path(NEXTDNS_LOG).read_text().lower()
    domains = re.findall(r"\b(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b", text)
    return set(domains)

def update_scores(domains, allowlist):
    now = datetime.now().isoformat()
    promoted = []

    for domain in domains:
        if domain in allowlist:
            continue

        score_delta = 1
        if any(bad in domain for bad in ["analytics", "ads", "track", "metrics"]):
            score_delta += 2
        if domain.endswith((".xyz", ".click", ".top", ".cf", ".ml")):
            score_delta += 1
        if domain in FIREBASE_DOMAINS:
            score_delta += 999

        c.execute("SELECT hit_count, score, status FROM domains WHERE domain = ?", (domain,))
        row = c.fetchone()
        if row:
            hit_count, score, status = row
            new_score = score + score_delta
            c.execute("UPDATE domains SET hit_count = ?, last_seen = ?, score = ? WHERE domain = ?",
                      (hit_count + 1, now, new_score, domain))
        else:
            c.execute("INSERT INTO domains (domain, first_seen, last_seen, hit_count, score, status) VALUES (?, ?, ?, ?, ?, ?)",
                      (domain, now, now, 1, score_delta, "pending"))

        if domain in FIREBASE_DOMAINS or score_delta >= PROMOTION_SCORE:
            promoted.append(domain)

    conn.commit()
    return promoted

def ingest_seed_list(seed_list, allowlist):
    now = datetime.now().isoformat()
    for domain in seed_list:
        if domain in allowlist:
            continue
        c.execute("SELECT domain FROM domains WHERE domain = ?", (domain,))
        if not c.fetchone():
            c.execute("INSERT INTO domains (domain, first_seen, last_seen, hit_count, score, status) VALUES (?, ?, ?, ?, ?, ?)",
                      (domain, now, now, 1, 999, "seeded"))
    conn.commit()

def export_blocklist():
    c.execute("SELECT domain FROM domains WHERE score >= ? AND status != 'allowlisted' ORDER BY score DESC LIMIT ?", (PROMOTION_SCORE, MAX_EXPORT))
    entries = [f"0.0.0.0 {row[0]}" for row in c.fetchall()]
    Path("personal_blocklist.txt").write_text("\n".join(entries))
    print(f"Exported {len(entries)} domains to personal_blocklist.txt")

def export_logs():
    c.execute("SELECT domain FROM domains WHERE score < ? AND status = 'pending'", (PROMOTION_SCORE,))
    pending = sorted(row[0] for row in c.fetchall())
    Path("pending_classification.txt").write_text("\n".join(pending))

    c.execute("SELECT domain FROM domains WHERE score >= ? AND status != 'allowlisted'", (PROMOTION_SCORE,))
    promoted = sorted(row[0] for row in c.fetchall())
    Path("promoted_today.txt").write_text("\n".join(promoted))

    print("Logs updated: pending_classification.txt, promoted_today.txt")

def main():
    if not Path(NEXTDNS_LOG).exists():
        print("No nextdns_log.txt found. Drop it in the folder and re-run.")
        return

    allowlist = load_allowlist()
    seed_list = load_seed_list()
    ingest_seed_list(seed_list, allowlist)
    domains = parse_domains_from_log()
    promoted = update_scores(domains, allowlist)
    export_blocklist()
    export_logs()

if __name__ == "__main__":
    main()