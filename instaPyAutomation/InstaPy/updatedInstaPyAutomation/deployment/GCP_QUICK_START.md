# GCP Quick Start - Instagram Bot Deployment

## 🚀 Deploy in 10 Minutes

### Step 1: Create GCP Account (3 min)
```
1. Go to: https://console.cloud.google.com/
2. Click "Try for free"
3. Sign in with Gmail
4. Add payment info (won't be charged)
5. Get $300 free credit ✅
```

### Step 2: Create VM (2 min)
```
1. Go to: Compute Engine → VM Instances
2. Click "CREATE INSTANCE"
3. Configure:
   - Name: instagram-bot
   - Region: us-central1 (Iowa)
   - Zone: us-central1-a
   - Machine: e2-micro (2 vCPU, 1GB RAM)
   - Boot disk: Ubuntu 22.04 LTS, 10GB
4. Click "CREATE"
5. Wait for green checkmark ✅
```

### Step 3: Install Google Cloud SDK on Windows (2 min)
```
1. Download: https://cloud.google.com/sdk/docs/install
2. Run installer
3. Open PowerShell and run:
   gcloud init
4. Login and select your project
```

### Step 4: Connect & Setup (5 min)
```powershell
# Connect to VM
gcloud compute ssh instagram-bot --zone=us-central1-a

# On the VM, create setup script
nano gcp_setup.sh
# Copy content from deployment/gcp_setup.sh
# Paste, save (Ctrl+O, Enter, Ctrl+X)

# Run setup
chmod +x gcp_setup.sh
./gcp_setup.sh
```

### Step 5: Upload Your Bot (1 min)
```powershell
# From Windows, in your project folder
cd C:\Users\siddh\OneDrive\Desktop\instaPyAutomation\InstaPy\updatedInstaPyAutomation

# Upload files
.\deployment\upload_to_gcp.ps1 -VMName instagram-bot -Zone us-central1-a
```

### Step 6: Setup Schedule (1 min)
```bash
# Back on VM
cd ~/instagram-bot/deployment
chmod +x gcp_setup_cron.sh
./gcp_setup_cron.sh

# Set your timezone
sudo timedatectl set-timezone America/Los_Angeles
```

## ✅ Done! 

Your bot now runs automatically at peak times:
- Mon-Wed: 11 AM
- Thu: 12 PM  
- Fri: 1 PM
- Sat-Sun: 10 AM

**Cost: $0** (using $300 free credit for 40+ months!)

---

## 📊 Quick Commands

**Connect to VM:**
```powershell
gcloud compute ssh instagram-bot --zone=us-central1-a
```

**View Logs:**
```bash
tail -f ~/instagram-bot/logs/monday.log
```

**Manual Test:**
```bash
cd ~/instagram-bot
source venv/bin/activate
python scheduled_automation.py
```

**Stop VM (save money):**
```powershell
gcloud compute instances stop instagram-bot --zone=us-central1-a
```

**Start VM:**
```powershell
gcloud compute instances start instagram-bot --zone=us-central1-a
```

---

## 💰 Cost After Free Credit

**Option 1: e2-micro** - $6-7/month (recommended)
**Option 2: f1-micro** - $0/month forever (Always Free tier)

To switch to f1-micro:
```bash
gcloud compute instances stop instagram-bot --zone=us-central1-a
gcloud compute instances set-machine-type instagram-bot --machine-type=f1-micro --zone=us-central1-a
gcloud compute instances start instagram-bot --zone=us-central1-a
```

---

## 🆘 Troubleshooting

**Can't connect?**
- Check VM is running in GCP Console
- Try web SSH: Compute Engine → VM Instances → SSH button

**Bot not running?**
```bash
# Check logs
cat ~/instagram-bot/logs/$(date +%A | tr '[:upper:]' '[:lower:]').log

# Check cron
crontab -l
```

**Need help?**
- Read full guide: `GCP_DEPLOYMENT_GUIDE.md`
- GCP docs: https://cloud.google.com/docs

---

## 🎓 Learning GCP

While your bot runs, explore:
- Cloud Console dashboard
- Billing reports (see your credit usage)
- VM metrics and monitoring
- Cloud Shell (built-in terminal)
- Free training: https://cloud.google.com/training

**Perfect for learning cloud while automating Instagram!** 🚀📚
