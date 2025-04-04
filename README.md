# Mobile DNS Blocklist Automation (Hari's Setup)

A complete Termux-powered, GitHub-synced, Discord-notifying DNS blocklist automation pipeline that runs directly from an Android device—no root, no PC needed.

---

## Features

- Maintain a deduplicated Adhell3/NextDNS-style blocklist
- Add new blocked domains via a simple text file
- Push updates to GitHub
- Get instant Discord alerts with domain count and status
- Trigger via Termux Widget or manually with one command
- Works 100% offline once setup is complete

---

## Requirements

1. **Install Termux**  
   Download **Termux** from [F-Droid](https://f-droid.org/packages/com.termux/)

2. **Install Termux Plugins**
   - [Termux:API](https://f-droid.org/packages/com.termux.api/)
   - [Termux:Widget](https://f-droid.org/packages/com.termux.widget/)

3. **Grant storage permission**
   ```bash
   termux-setup-storage
   ```

4. **Install required packages**
   ```bash
   pkg update && pkg upgrade
   pkg install git python curl nano termux-api cronie
   ```

---

## GitHub Setup

1. Create a new repo (e.g. `blocklist`)
2. Clone it in Termux:
   ```bash
   git clone https://github.com/YOUR_USERNAME/blocklist.git ~/blocklist
   ```

---

## Discord Webhook Setup

1. Go to your Discord server → Settings → Integrations → Webhooks
2. Click **"New Webhook"** and copy the URL
3. In your script (`dnsupdate`), update the webhook line:
   ```bash
   curl -H "Content-Type: application/json" -X POST -d '{ "content": ... }' https://discord.com/api/webhooks/XXXX/YYY
   ```

---

## Script Setup

1. Save the script as `dnsupdate` in:
   ```
   ~/.shortcuts/
   ```
   or create it with:
   ```bash
   nano ~/.shortcuts/dnsupdate
   ```

2. Make it executable:
   ```bash
   chmod +x ~/.shortcuts/dnsupdate
   ```

3. Add a bash alias (optional):
   ```bash
   echo "alias dnsupdate='~/.shortcuts/dnsupdate'" >> ~/.bashrc
   source ~/.bashrc
   ```

---

## Usage

### **Step 1: Scrape & Save Blocked Domains**
- From NextDNS logs (filtered by “Blocked”), copy the domains
- Save them in a file named:
  ```
  /sdcard/Download/input_blocked_domains.txt
  ```
  - One domain per line, no formatting

### **Step 2: Trigger Update**

#### Option A: Manually via Termux
```bash
dnsupdate
```

#### Option B: From Home Screen (Termux Widget)
- Add the **Termux Widget** to your home screen
- Tap the `dnsupdate` shortcut to run the whole flow

---

## Files in This Repo

| File | Purpose |
|------|---------|
| `dnsupdate` | Main script that moves, dedupes, updates, and reports |
| `adhell3_blocklist_from_nextdns.txt` | Your deduplicated master list |
| `input_blocked_domains.txt` | (Temporary) new domains copied from NextDNS logs |

---

## Script Flow Summary

1. Checks if `input_blocked_domains.txt` exists in Downloads
2. Moves it to Termux (`~/blocklist`)
3. Deduplicates and appends to `adhell3_blocklist_from_nextdns.txt`
4. Pushes the file to GitHub
5. Sends a success/failure Discord message
6. Shows a toast on your phone

---

## Maintenance Notes

- Clean `input_blocked_domains.txt` gets cleared after every run
- No duplicates are added to your master list
- Script is safe to run multiple times
- Git/Discord integration will fail silently if credentials/webhook are invalid

---

## Optional: Logging (Future Add-On)

Want to log every run to a file? Add this at the bottom of your script:
```bash
echo "$timestamp - Updated $count domains" >> ~/blocklist/update.log
```

---

## Credits

Custom pipeline built by Hari with ChatGPT-4 assistance. Precision-engineered on Android.
