import sqlite3
from pathlib import Path
from datetime import datetime
import re

LOG_FILE = "nextdns_log.txt"
ALLOWLIST_FILE = "allowlist.txt"
DB_FILE = "domain_db.sqlite"
OUTPUT_FILE = "auto_block.txt"
SCORE_THRESHOLD = 5
MAX_EXPORT = 50000

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS domains (
        domain TEXT PRIMARY KEY,
        first_seen TEXT,
        last_seen TEXT,
        hits INTEGER,
        score INTEGER
    )
""")
conn.commit()

def load_allowlist():
    if not Path(ALLOWLIST_FILE).exists():
        return set()
    with open(ALLOWLIST_FILE) as f:
        return set(line.strip().lower().lstrip("*.") for line in f if line.strip())

def parse_log():
    if not Path(LOG_FILE).exists():
        return set()
    text = Path(LOG_FILE).read_text().lower()
    return set(re.findall(r"\b(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b", text))

def update_scores(domains, allowlist):
    now = datetime.now().isoformat()
    for d in domains:
        if d in allowlist:
            continue
        score = 1
        if any(x in d for x in ["ads", "track", "metric", "analytics", "firebase", "moengage", "appsflyer"]):
            score += 2
        c.execute("SELECT hits, score FROM domains WHERE domain = ?", (d,))
        row = c.fetchone()
        if row:
            hits, prev = row
            c.execute("UPDATE domains SET hits = ?, score = ?, last_seen = ? WHERE domain = ?",
                      (hits + 1, prev + score, now, d))
        else:
            c.execute("INSERT INTO domains (domain, first_seen, last_seen, hits, score) VALUES (?, ?, ?, ?, ?)",
                      (d, now, now, 1, score))
    conn.commit()

def export_blocklist():
    c.execute("SELECT domain FROM domains WHERE score >= ? ORDER BY score DESC LIMIT ?", (SCORE_THRESHOLD, MAX_EXPORT))
    rows = c.fetchall()
    Path(OUTPUT_FILE).write_text("\n".join(f"0.0.0.0 {r[0]}" for r in rows))
    print(f"Exported {len(rows)} to {OUTPUT_FILE}")

def main():
    allow = load_allowlist()
    hits = parse_log()
    update_scores(hits, allow)
    export_blocklist()

if __name__ == "__main__":
    main()
