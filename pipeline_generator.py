# pipeline_generator.py
# Hari's personal DNS -> Adhell3 blocklist updater
# Run weekly to update your GitHub-hosted blocklist

blocked_domains = ['mobile.pipe.aria.microsoft.com', 'contile.services.mozilla.com', 'mobile.events.data.microsoft.com', 'eu-teams.events.data.microsoft.com', 'o1069899.ingest.sentry.io', 'in.appcenter.ms', 'o33249.ingest.sentry.io']

# Deduplicate & format
formatted = sorted(set(f"0.0.0.0 {d}" for d in blocked_domains))

# Save to blocklist file
with open("hari_adhell_blocklist.txt", "w") as f:
    f.write("\n".join(formatted))

print("Updated Adhell3 blocklist written to hari_adhell_blocklist.txt")

# Optionally, git push this to your GitHub repo using CLI:
# git add hari_adhell_blocklist.txt
# git commit -m "Update blocklist"
# git push
