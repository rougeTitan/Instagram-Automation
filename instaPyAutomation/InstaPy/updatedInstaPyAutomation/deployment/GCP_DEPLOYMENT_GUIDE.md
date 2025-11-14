# Google Cloud Platform Deployment Guide
# Complete guide to deploy Instagram automation on GCP

## 🎯 Why Google Cloud Platform?

- ✅ **$300 FREE credit** (valid for 90 days)
- ✅ **Easy to use** - Best for learning cloud
- ✅ **e2-micro**: $6-7/month after credit (or FREE tier available)
- ✅ **Excellent documentation** and learning resources
- ✅ **Integration** with other Google services
- ✅ **Automatic scaling** options

---

## 💰 Cost Breakdown

### Free Trial:
- **$300 credit** for 90 days (new accounts)
- Can run e2-medium (~$20/month) for free during trial
- No charges until you upgrade to paid account

### After Free Trial:
**Option 1: e2-micro (Recommended)**
- Cost: ~$6-7/month
- 2 vCPU, 1GB RAM
- Sufficient for Instagram bot

**Option 2: Always Free Tier**
- f1-micro: FREE forever
- 0.6GB RAM (may be tight, but workable)
- Only in specific regions (us-west1, us-central1, us-east1)

**Our recommendation:** Use e2-micro during free trial, then switch to f1-micro if you want $0 cost.

---

## 📋 Prerequisites

1. Google account (Gmail)
2. Credit/debit card (for verification, won't be charged during free trial)
3. Google Cloud SDK installed on Windows
4. Your Instagram credentials
5. Gemini API key

---

## 🚀 Step 1: Create GCP Account

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Activate Free Trial**
   - Click "Try for free" or "Activate" button
   - Fill in:
     - Country
     - Terms of service (agree)
     - Account type: Individual
     - Name and address
     - Payment method (won't be charged)
   - Click "Start my free trial"

3. **Verify $300 Credit**
   - Go to: Billing → Overview
   - Should see "$300 credit remaining"

---

## ☁️ Step 2: Create VM Instance

1. **Navigate to Compute Engine**
   - Go to: Navigation Menu (☰) → Compute Engine → VM Instances
   - Click "Enable API" if prompted (takes 1-2 minutes)

2. **Create Instance**
   - Click "CREATE INSTANCE"

3. **Configure Instance**
   
   **Name:** `instagram-bot`
   
   **Region & Zone:**
   - Region: `us-central1` (Iowa) - Cheapest
   - Zone: `us-central1-a`
   
   **Machine Configuration:**
   - Series: `E2`
   - Machine type: `e2-micro` (2 vCPU, 1GB RAM)
     - Cost: ~$6.50/month (FREE during trial)
   
   **Boot Disk:**
   - Click "CHANGE"
   - Operating System: `Ubuntu`
   - Version: `Ubuntu 22.04 LTS`
   - Boot disk type: `Standard persistent disk`
   - Size: `10 GB` (minimum)
   - Click "SELECT"
   
   **Firewall:**
   - ✓ Allow HTTP traffic
   - ✓ Allow HTTPS traffic
   
4. **Click "CREATE"**
   - Wait 30-60 seconds for VM to start
   - Status will show green checkmark when ready

5. **Note the External IP**
   - Copy the External IP address (e.g., 34.123.x.x)

---

## 🔧 Step 3: Install Google Cloud SDK (Windows)

1. **Download Cloud SDK**
   - Go to: https://cloud.google.com/sdk/docs/install
   - Download Windows installer (x86_64)

2. **Install**
   - Run `GoogleCloudSDKInstaller.exe`
   - Accept defaults
   - ✓ Check "Run gcloud init"
   - Click "Finish"

3. **Initialize gcloud**
   ```powershell
   # This should open automatically, if not run:
   gcloud init
   
   # Follow prompts:
   # 1. Log in to Google account (browser will open)
   # 2. Select your project
   # 3. Set default region: us-central1-a
   ```

4. **Verify Installation**
   ```powershell
   gcloud --version
   # Should show: Google Cloud SDK [version]
   ```

---

## 🔑 Step 4: Connect to Your VM

### Method 1: Web SSH (Easiest)
1. Go to: Compute Engine → VM Instances
2. Click "SSH" button next to your VM
3. Browser window opens with terminal

### Method 2: gcloud CLI (Recommended)
```powershell
# From PowerShell
gcloud compute ssh instagram-bot --zone=us-central1-a
```

**First time:** Type "yes" to add host to known hosts

---

## 📦 Step 5: Run Setup Script

Once connected via SSH:

```bash
# Create setup script
nano gcp_setup.sh

# Copy content from deployment/gcp_setup.sh file
# Paste it (Right-click in terminal)
# Save: Ctrl+O, Enter, Ctrl+X

# Make executable
chmod +x gcp_setup.sh

# Run setup (takes 5-10 minutes)
./gcp_setup.sh
```

**What this installs:**
- Python 3.11
- Google Chrome
- ChromeDriver
- Xvfb (virtual display)
- All dependencies
- Virtual environment

---

## 📁 Step 6: Upload Your Bot Files

### Option A: Using gcloud (Recommended)

```powershell
# From Windows PowerShell, in your project folder
cd C:\Users\siddh\OneDrive\Desktop\instaPyAutomation\InstaPy\updatedInstaPyAutomation

# Run upload script
.\deployment\upload_to_gcp.ps1 -VMName instagram-bot -Zone us-central1-a
```

### Option B: Manual Upload

```powershell
# Upload specific folders
gcloud compute scp --recurse core instagram-bot:~/instagram-bot/ --zone=us-central1-a
gcloud compute scp --recurse data instagram-bot:~/instagram-bot/ --zone=us-central1-a
gcloud compute scp --recurse deployment instagram-bot:~/instagram-bot/ --zone=us-central1-a
gcloud compute scp scheduled_automation.py instagram-bot:~/instagram-bot/ --zone=us-central1-a
gcloud compute scp main.py instagram-bot:~/instagram-bot/ --zone=us-central1-a
gcloud compute scp .env instagram-bot:~/instagram-bot/ --zone=us-central1-a
```

### Option C: Create .env on VM

```bash
# On the VM
nano ~/instagram-bot/.env
```

Paste:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
GEMINI_API_KEY=your_api_key
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## ⏰ Step 7: Setup Cron Jobs

```bash
# On the VM
cd ~/instagram-bot/deployment

# Make executable
chmod +x gcp_setup_cron.sh

# Run setup
./gcp_setup_cron.sh
```

**This creates scheduled jobs for:**
- Monday:    11:00 AM
- Tuesday:   11:00 AM
- Wednesday: 11:00 AM (Best day!)
- Thursday:  12:00 PM
- Friday:    1:00 PM
- Saturday:  10:00 AM
- Sunday:    10:00 AM

---

## ⚠️ Step 8: Set Timezone

GCP VMs default to UTC. Set to your timezone:

```bash
# View current timezone
timedatectl

# Set timezone (examples)
# US Pacific:
sudo timedatectl set-timezone America/Los_Angeles

# US Eastern:
sudo timedatectl set-timezone America/New_York

# India:
sudo timedatectl set-timezone Asia/Kolkata

# List all timezones:
timedatectl list-timezones | grep -i YOUR_CITY

# Verify
timedatectl
```

---

## 🧪 Step 9: Test Manual Run

```bash
cd ~/instagram-bot
source venv/bin/activate
python scheduled_automation.py
```

**Expected output:**
- Chrome starts in headless mode
- Logs in to Instagram
- Selects 2 random categories
- Processes 5 posts each
- Comments with AI
- Likes posts
- Closes browser

---

## 📊 Step 10: Monitor Your Bot

### View Cron Jobs
```bash
crontab -l
```

### View Logs
```bash
# Today's log
tail -f ~/instagram-bot/logs/$(date +%A | tr '[:upper:]' '[:lower:]').log

# Specific day
cat ~/instagram-bot/logs/monday.log

# All logs
ls -lh ~/instagram-bot/logs/
```

### Check Running Processes
```bash
ps aux | grep python
```

### View Analytics
```bash
cat ~/instagram-bot/data/statistics.json
```

---

## 🔧 GCP-Specific Management

### Stop VM (Save Money)
```powershell
# From Windows
gcloud compute instances stop instagram-bot --zone=us-central1-a

# Note: Cron jobs won't run when stopped
```

### Start VM
```powershell
gcloud compute instances start instagram-bot --zone=us-central1-a
```

### View VM Status
```powershell
gcloud compute instances list
```

### Check Costs
1. Go to: Billing → Reports
2. View daily spending
3. Set budget alerts

### Set Budget Alert
1. Go to: Billing → Budgets & alerts
2. Click "CREATE BUDGET"
3. Set amount: $10/month
4. Set alert at: 50%, 90%, 100%
5. Enter email for notifications

---

## 💡 Cost Optimization Tips

### During Free Trial ($300 credit):
- Use e2-micro or e2-small freely
- Credit lasts ~12-15 months for e2-micro
- No need to stop VM

### After Free Trial:

**Option 1: Switch to f1-micro (FREE forever)**
```bash
# Stop current VM
gcloud compute instances stop instagram-bot --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type instagram-bot \
  --machine-type=f1-micro \
  --zone=us-central1-a

# Start VM
gcloud compute instances start instagram-bot --zone=us-central1-a
```

**Option 2: Keep e2-micro ($6-7/month)**
- Better performance
- More reliable
- Worth the cost

**Option 3: Schedule VM Auto-Start/Stop**
```bash
# Stop VM at night (11 PM)
0 23 * * * gcloud compute instances stop instagram-bot --zone=us-central1-a

# Start VM in morning (9 AM)
0 9 * * * gcloud compute instances start instagram-bot --zone=us-central1-a
```

---

## 🔐 Security Best Practices

### Firewall Rules (Already set up, but good to know)
```bash
# Check firewall
gcloud compute firewall-rules list

# Only allow SSH from your IP (optional)
gcloud compute firewall-rules create allow-ssh-from-home \
  --allow=tcp:22 \
  --source-ranges=YOUR_HOME_IP/32
```

### Regular Updates
```bash
# Update system monthly
sudo apt update && sudo apt upgrade -y
```

---

## 🐛 Troubleshooting

### Chrome won't start
```bash
google-chrome --version
chromedriver --version

# Test with display
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
```

### Can't connect via SSH
```bash
# Reset SSH key
gcloud compute config-ssh

# Or use web SSH
# Go to Compute Engine → VM Instances → Click SSH button
```

### Out of memory
```bash
# Check memory
free -h

# If f1-micro is too small, upgrade to e2-micro
gcloud compute instances set-machine-type instagram-bot \
  --machine-type=e2-micro \
  --zone=us-central1-a
```

### Cron not running
```bash
# Check cron service
sudo service cron status

# View system logs
grep CRON /var/log/syslog
```

---

## 📚 Learning Resources

**GCP Basics:**
- Documentation: https://cloud.google.com/docs
- Free training: https://cloud.google.com/training
- Quickstart labs: https://www.cloudskillsboost.google/

**VM Management:**
- Compute Engine docs: https://cloud.google.com/compute/docs
- Cost calculator: https://cloud.google.com/products/calculator

**Billing:**
- Understanding billing: https://cloud.google.com/billing/docs
- Free tier: https://cloud.google.com/free

---

## 🎯 Next Steps

1. **Monitor first week**
   - Check logs daily
   - Verify bot runs at scheduled times
   - Review Instagram activity

2. **Set up billing alerts**
   - Alert at $5, $10, $15
   - Monitor credit usage

3. **Optimize performance**
   - Review analytics
   - Adjust categories
   - Tune engagement settings

4. **Learn GCP features**
   - Try Cloud Functions
   - Explore Cloud Scheduler
   - Use Cloud Monitoring

---

## 💰 Final Cost Summary

**During Free Trial (90 days):**
- Cost: $0 (using $300 credit)
- e2-micro usage: ~$6.50/month
- Total credit used: ~$20
- **Remaining credit: $280** (can last 40+ months!)

**After Trial:**
- e2-micro: $6-7/month
- f1-micro: $0/month (Always Free)
- Storage: $0.40/month (10GB)
- Network: $0 (within free tier)

**Recommendation:** Use trial fully, then switch to f1-micro for $0 forever!

---

## ✅ You're All Set!

Your Instagram bot is running 24/7 on Google Cloud Platform!

- ✅ $300 free credit (90 days)
- ✅ Professional cloud infrastructure
- ✅ Learning real cloud technology
- ✅ Automatic peak-time engagement
- ✅ AI-powered comments
- ✅ 10 posts/day = 70/week

**Enjoy your automated Instagram growth while learning GCP!** 🚀📚
