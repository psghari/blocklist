#!/data/data/com.termux/files/usr/bin/bash
# dnsupdate - Automates blocklist update from input file, deduplicates, commits to GitHub, sends Discord alerts, and shows toast

cd ~/blocklist || exit 1

# Move input file from Downloads if it exists
if [ -f /sdcard/Download/input_blocked_domains.txt ]; then
  mv /sdcard/Download/input_blocked_domains.txt ~/blocklist/
fi

input_file="input_blocked_domains.txt"
master_file="adhell3_blocklist_from_nextdns.txt"

# Check if input file exists and is not empty
if [ ! -s "$input_file" ]; then
  termux-toast -g bottom -s "⚠️ No domains to update."
  echo "No new domains to process."
  exit 0
fi

# Deduplicate and append new domains
while read -r domain; do
  domain=$(echo "$domain" | xargs)  # trim
  if ! grep -Fxq "0.0.0.0 $domain" "$master_file"; then
    echo "0.0.0.0 $domain" >> "$master_file"
  fi
done < "$input_file"

# Clear input file after processing
> "$input_file"

# --- Clean malformed lines and deduplicate master file ---
temp_cleaned=$(mktemp)
awk '$1 == "0.0.0.0" && NF == 2 && $2 !~ /^0\.0\.0\.0$/ { gsub(/^0\.0\.0\.0 /, "", $2); print "0.0.0.0 " $2 }' "$master_file" | sort -u > "$temp_cleaned"
mv "$temp_cleaned" "$master_file"

# Count and timestamp
count=$(grep -c "^0.0.0.0" "$master_file")
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

# Git commit and push
git add "$master_file"
git commit -m "Delta update at $timestamp with $count total domains"
git push

# Discord webhook status message
webhook_url="https://discord.com/api/webhooks/1357810542970015784/Cz-cPSsb82vHu189zEtuElbEiitdlzLCqyibhSobs5uptjZ8P3K1zd70Y7rxLcgQJ6vW"
if [ $? -eq 0 ]; then
  curl -H "Content-Type: application/json" -X POST -d '{ "content": "✅ Delta update complete at **'"$timestamp"'** with **'"$count"'** total domains in blocklist." }' "$webhook_url"
  termux-toast -g bottom -s "✅ DNS update complete and pushed!"
else
  curl -H "Content-Type: application/json" -X POST -d '{ "content": "❌ Delta update failed at **'"$timestamp"'**. Check Termux logs." }' "$webhook_url"
  termux-toast -g bottom -s "❌ DNS update failed. Check logs."
fi
