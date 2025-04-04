# pipeline_generator.py
# Updates your GitHub-hosted Adhell3 blocklist for NextDNS

# STEP 1: Add your domains here (update from logs weekly)
blocked_domains = [
    "mobile.pipe.aria.microsoft.com",
    "contile.services.mozilla.com",
    "mobile.events.data.microsoft.com",
    "eu-teams.events.data.microsoft.com",
    "o1069899.ingest.sentry.io",
    "in.appcenter.ms",
    "o33249.ingest.sentry.io"
]

# STEP 2: Format to Adhell3 blacklist style
formatted = sorted(set(f"0.0.0.0 {d}" for d in blocked_domains))

# STEP 3: Write to correct file for GitHub sync
with open("adhell3_blocklist_from_nextdns.txt", "w") as f:
    f.write("\n".join(formatted))

print("Updated adhell3_blocklist_from_nextdns.txt")

# STEP 4: Git push (run manually or automate via Termux cron)
# git add adhell3_blocklist_from_nextdns.txt
# git commit -m "Auto update from mobile"
# git push
