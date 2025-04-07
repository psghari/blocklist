#!/data/data/com.termux/files/usr/bin/bash

cd ~/blocklist || exit 1

echo "[+] Updating Fusionjack seed..."
python update_seed_from_fusionjack.py

echo "[+] Running domain triage..."
python triage_blocklist.py

echo "[+] Committing and pushing to GitHub..."
git add *.py *.txt personal_blocklist.txt
git commit -m "Auto-update blocklist: $(date '+%Y-%m-%d %H:%M')"
git push

echo "[✓] Done. Everything synced."