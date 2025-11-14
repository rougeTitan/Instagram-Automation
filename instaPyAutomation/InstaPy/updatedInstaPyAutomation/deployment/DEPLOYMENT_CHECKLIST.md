# Oracle Cloud Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] Oracle Cloud account created
- [ ] Credit card added (for verification only)
- [ ] Email verified
- [ ] Instagram credentials ready
- [ ] Gemini API key obtained
- [ ] SSH client installed (Windows Terminal, WSL, or PuTTY)

---

## 🖥️ VM Creation Checklist

- [ ] Logged into Oracle Cloud Console (cloud.oracle.com)
- [ ] Clicked "Create a VM Instance"
- [ ] Named instance: "instagram-bot"
- [ ] Selected Ubuntu 22.04 image
- [ ] Selected VM.Standard.A1.Flex shape
- [ ] Configured: 1 OCPU, 6GB RAM
- [ ] Generated SSH key pair
- [ ] Downloaded private key (oracle_key.pem)
- [ ] Noted public IP address: ___________________
- [ ] VM status shows "Running" (green)

---

## 🔐 Connection Checklist

- [ ] SSH key file saved to: C:\Users\siddh\Downloads\oracle_key.pem
- [ ] Successfully connected via SSH
- [ ] Command used: `ssh -i oracle_key.pem ubuntu@YOUR_IP`
- [ ] Accepted host fingerprint (typed "yes")
- [ ] Seeing ubuntu@instagram-bot prompt

---

## 📦 Setup Checklist

- [ ] Uploaded oracle_setup.sh to VM
- [ ] Made script executable: `chmod +x oracle_setup.sh`
- [ ] Ran setup script: `./oracle_setup.sh`
- [ ] Python 3.11 installed successfully
- [ ] Chrome installed successfully
- [ ] ChromeDriver installed successfully
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] No errors in setup output

---

## 📁 File Upload Checklist

**Option A: PowerShell Upload Script**
- [ ] Ran: `.\deployment\upload_to_oracle.ps1 -PublicIP YOUR_IP`
- [ ] All files uploaded successfully

**Option B: Manual SCP**
- [ ] Uploaded core/ folder
- [ ] Uploaded data/ folder
- [ ] Uploaded docs/ folder
- [ ] Uploaded tests/ folder
- [ ] Uploaded deployment/ folder
- [ ] Uploaded scheduled_automation.py
- [ ] Uploaded main.py
- [ ] Uploaded .env file with credentials
- [ ] Uploaded requirements.txt

**Verify on VM:**
- [ ] Ran: `ls ~/instagram-bot/`
- [ ] See all folders and files listed

---

## ⚙️ Configuration Checklist

**Environment Variables:**
- [ ] Created .env file: `nano ~/instagram-bot/.env`
- [ ] Added INSTAGRAM_USERNAME
- [ ] Added INSTAGRAM_PASSWORD
- [ ] Added GEMINI_API_KEY
- [ ] Saved file (Ctrl+O, Enter, Ctrl+X)
- [ ] Verified: `cat ~/instagram-bot/.env`

**Dependencies:**
- [ ] Activated venv: `source ~/instagram-bot/venv/bin/activate`
- [ ] Installed packages: `pip install -r requirements.txt`
- [ ] No installation errors

---

## ⏰ Cron Setup Checklist

- [ ] Navigated to: `cd ~/instagram-bot/deployment`
- [ ] Made executable: `chmod +x setup_cron.sh`
- [ ] Ran script: `./setup_cron.sh`
- [ ] Saw success messages for all 7 days
- [ ] Verified jobs: `crontab -l`
- [ ] See 7 cron entries (Monday-Sunday)

**Timezone Configuration:**
- [ ] Checked timezone: `timedatectl`
- [ ] Set correct timezone: `sudo timedatectl set-timezone YOUR/TIMEZONE`
- [ ] Verified timezone is correct

---

## 🧪 Testing Checklist

**Manual Test Run:**
- [ ] Activated venv: `source ~/instagram-bot/venv/bin/activate`
- [ ] Ran test: `python scheduled_automation.py`
- [ ] Saw "Setting up Chrome browser..."
- [ ] Login successful
- [ ] Categories selected (2 random)
- [ ] Posts found
- [ ] Comments posted with AI
- [ ] Posts liked
- [ ] Browser closed
- [ ] No critical errors

**Log Files:**
- [ ] Logs directory created: `ls ~/instagram-bot/logs/`
- [ ] Can view logs: `cat ~/instagram-bot/logs/monday.log`

---

## 📊 Monitoring Setup Checklist

**Verify Automation:**
- [ ] Check cron status: `sudo service cron status`
- [ ] Cron service is "active (running)"
- [ ] Can view logs for each day
- [ ] Analytics file exists: `~/instagram-bot/data/analytics.json`
- [ ] Statistics file exists: `~/instagram-bot/data/statistics.json`

---

## 🎯 Post-Deployment Checklist

**First 24 Hours:**
- [ ] Check if bot ran at scheduled time
- [ ] Review log file for that day
- [ ] Verify posts were liked and commented
- [ ] Check Instagram account for new activity
- [ ] No error messages in logs

**First Week:**
- [ ] Bot runs daily at scheduled times
- [ ] Different categories selected each day
- [ ] Comments are varied and contextual
- [ ] No Instagram warnings/blocks
- [ ] Analytics data accumulating

**Optimization:**
- [ ] Review analytics: `cat ~/instagram-bot/data/analytics.json`
- [ ] Adjust schedule if needed
- [ ] Modify categories if desired
- [ ] Update custom message if needed

---

## 🆘 Troubleshooting Reference

**If bot doesn't run:**
```bash
# Check cron logs
grep CRON /var/log/syslog

# Check bot logs
tail -100 ~/instagram-bot/logs/$(date +%A | tr '[:upper:]' '[:lower:]').log

# Run manually to see errors
cd ~/instagram-bot
source venv/bin/activate
python scheduled_automation.py
```

**If Chrome fails:**
```bash
# Test Chrome
google-chrome --version
chromedriver --version

# Check display
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
```

**If login fails:**
```bash
# Verify credentials
cat ~/instagram-bot/.env

# Check Instagram for security notifications
# May need to verify account from email
```

---

## ✨ Final Verification

- [ ] VM is running (check Oracle Cloud Console)
- [ ] Cron jobs are active: `crontab -l`
- [ ] Can SSH to VM anytime
- [ ] Bot runs at scheduled times automatically
- [ ] Logs are being created
- [ ] Instagram activity is visible
- [ ] No cost charges (Always Free tier)

---

## 🎊 Deployment Complete!

**Your Instagram bot is now:**
- ✅ Running 24/7 on Oracle Cloud
- ✅ Completely FREE (Always Free tier)
- ✅ Automated at peak engagement times
- ✅ Using AI for contextual comments
- ✅ Processing 10 posts per day (70/week)
- ✅ Independent of your PC

**Total Setup Time:** ~30-60 minutes
**Monthly Cost:** $0.00 forever 🎉

---

## 📝 Important Notes

**Save These Details:**
- Public IP: ___________________
- SSH Key Location: ___________________
- Oracle Account Email: ___________________
- VM OCID (for reference): ___________________

**Bookmark:**
- Oracle Cloud Console: https://cloud.oracle.com/
- This checklist for future reference

**Next Steps:**
- Monitor for first week
- Check logs daily
- Review analytics weekly
- Optimize based on results
