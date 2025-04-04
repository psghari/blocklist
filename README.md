# Mobile DNS Blocklist Automation (Hari's Setup)

> **WARNING – READ FIRST**
>
> 1. This repo includes a `dnsupdate.template` script – you **must copy it** and rename it to `dnsupdate` before use.
> 2. You MUST replace the dummy Discord webhook URL (`https://discord.com/api/webhooks/REPLACE_ME`) with your **own**. If you don't, your updates will fail or worse – go to someone else's Discord.
> 3. The actual working script (`dnsupdate`) is ignored via `.gitignore` for security. Keep your version local and private.

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

## GitHub Setup (Clone, Commit & Push)

1. Create a GitHub repo called `blocklist` (or any name you like)
2. Clone it into Termux:
   ```bash
   git clone https://github.com/YOUR_USERNAME/blocklist.git ~/blocklist
   ```
3. Set your Git identity:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
4. When ready to push:
   ```bash
   cd ~/blocklist
   git add .
   git commit -m "Your message"
   git push
   ```
5. Use a **Personal Access Token (PAT)** as your GitHub password when prompted

---

## Setting Up NextDNS for This Pipeline

1. Go to [https://my.nextdns.io](https://my.nextdns.io) and sign in or create an account
2. Create a new configuration
3. Enable logging:
   - Go to `Settings > Logs`
   - Set **Log Retention** (e.g. 1 or 2 weeks)
4. When you're ready to update:
   - Visit the **Logs** tab
   - Filter by **Status: Blocked**
   - Scroll down and **copy domain names**
   - Paste into a file called:
     ```
     /sdcard/Download/input_blocked_domains.txt
     ```
   - One domain per line, no formatting needed

---

## Discord Webhook Setup

> **IMPORTANT:** You must replace the webhook URL placeholder in `dnsupdate.template`:
> ```bash
> webhook_url="https://discord.com/api/webhooks/REPLACE_ME"
> ```
> Replace it with your own webhook from your Discord server settings.

1. Go to your Discord server → Settings → Integrations → Webhooks
2. Click **"New Webhook"** and copy the URL
3. Update the script (`dnsupdate`) after copying from the template

---

## Script Setup

1. Copy the template:
   ```bash
   cp dnsupdate.template dnsupdate
   ```
   Then edit:
   ```bash
   nano dnsupdate
   ```
   → Replace the webhook URL as mentioned above.

2. Move it to the Termux shortcuts folder:
   ```bash
   mv dnsupdate ~/.shortcuts/
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
| `dnsupdate.template` | Safe version of script with webhook placeholder |
| `adhell3_blocklist_from_nextdns.txt` | Your deduplicated master list |
| `input_blocked_domains.txt` | (Temporary) new domains copied from NextDNS logs |
| `.gitignore` | Prevents your real `dnsupdate` from being pushed by mistake |
| `README.md` | You’re reading it—don’t skip it again, meathead |

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

## Optional: Logging

Want to log every run to a file? Add this at the bottom of your script:
```bash
echo "$timestamp - Updated $count domains" >> ~/blocklist/update.log
```

---

## Credits

This setup was built and battle-tested by **Hari**, with automation, scripting, and profanity-ready optimization from **ChatGPT-4**.  
If you break it, you buy it.  
If you clone it, don't be an idiot—replace the webhook.

