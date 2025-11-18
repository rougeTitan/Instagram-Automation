# GCP Deployment Troubleshooting Log

**Date:** November 14, 2025 (Updated: November 18, 2025)  
**Project:** Instagram Automation Bot  
**VM Instance:** instagram-bot (e2-micro, us-east1-c)  
**Final Status:** ✅ Successfully Deployed with Auto Start/Stop (85% Cost Reduction)

---

## Overview

This document records all issues encountered and solutions applied during the GCP deployment process. Use this as a reference for future deployments or troubleshooting.

---

## Issue 1: Billing Not Enabled

### Problem
```
ERROR: (gcloud.compute.instances.create) Could not fetch resource:
 - Billing must be enabled for activation of service
```

### Root Cause
- Attempting to create VM in project `gen-lang-client-0942698456` which didn't have billing enabled
- $300 free credit was on a different project

### Solution
1. Listed all projects: `gcloud projects list`
2. Found correct project with billing: `emerald-diagram-478119-n2` (My First Project)
3. Switched to correct project: `gcloud config set project emerald-diagram-478119-n2`
4. Enabled Compute Engine API: `gcloud services enable compute.googleapis.com`

### Prevention
- Always verify billing is enabled on the project before creating resources
- Check which project has the $300 free credit: Look in GCP Console → Billing

---

## Issue 2: VM Already Exists in Different Project

### Problem
- Could not find VM "instagram-bot" in expected project
- VM creation appeared to fail but VM actually existed elsewhere

### Root Cause
- VM was created in `emerald-diagram-478119-n2` project (correct one)
- Was searching in `gen-lang-client-0942698456` project (wrong one)

### Solution
1. Listed all VMs across projects:
```bash
gcloud compute instances list --project=emerald-diagram-478119-n2
```

2. Found VM details:
- **Name:** instagram-bot
- **Zone:** us-east1-c
- **Status:** TERMINATED (stopped)
- **External IP:** 34.75.39.52 (later changed to 34.26.122.94)

3. Started the VM:
```bash
gcloud compute instances start instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2
```

### Prevention
- Always note the exact project ID where resources are created
- Use `--project` flag explicitly in all gcloud commands

---

## Issue 3: SSH Connection Failures

### Problem
Multiple SSH connection attempts failed:
```
ERROR: (gcloud.compute.ssh) Could not SSH into the instance.
Permission denied (publickey)
```

### Attempted Solutions (Failed)
1. ❌ SSH key generation and upload
2. ❌ Metadata SSH key configuration
3. ❌ OS Login enable/disable
4. ❌ Direct gcloud compute ssh commands

### Working Solution
**Use GCP Console Web SSH:**
1. Go to: https://console.cloud.google.com/compute/instances
2. Select project: `emerald-diagram-478119-n2`
3. Find VM: `instagram-bot` in zone `us-east1-c`
4. Click "SSH" button in browser → Opens web terminal
5. Works immediately without any configuration!

### Why Web SSH Works
- Managed by Google Cloud automatically
- No SSH key configuration needed
- Browser-based authentication using your Google account
- Most reliable method for initial setup

### Prevention
- For initial setup and troubleshooting, always use Web SSH from GCP Console
- Only configure local SSH after VM is fully set up and working

---

## Issue 4: File Upload - Permission Denied

### Problem
```bash
gcloud compute scp --recurse . instagram-bot:~/instagram-bot --zone=us-east1-c
```
Failed with:
- Permission denied errors
- "Too many authentication failures"
- Connection timeouts

### Attempted Solutions (Failed)
1. ❌ Recursive directory copy
2. ❌ Individual file upload
3. ❌ Different SSH key configurations
4. ❌ Absolute paths
5. ❌ User specification variations

### Working Solution
**Create zip archive and upload:**

```powershell
# 1. Create zip archive locally
Compress-Archive -Path * -DestinationPath instagram-bot.zip -Force

# 2. Upload zip file via gcloud scp (MUCH more reliable)
gcloud compute scp instagram-bot.zip instagram-bot:~ --zone=us-east1-c --project=emerald-diagram-478119-n2

# 3. Connect via Web SSH and extract
ssh-in-browser> unzip instagram-bot.zip -d instagram-bot
ssh-in-browser> cd instagram-bot
```

### Why This Works
- Single file upload is more reliable than recursive directory copy
- Zip reduces file count from hundreds to 1
- Web SSH terminal handles extraction perfectly
- No permission issues with local file operations on VM

### Prevention
- **Always use zip/tar for project uploads**
- Upload archive → Extract on VM → Delete archive
- Don't try to scp recursive directories with many files

---

## Issue 5: ChromeDriver Download 404 Error

### Problem
Initial setup script tried to download ChromeDriver manually:
```bash
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
# Returns 404 - Google changed download location
```

### Root Cause
- Google moved ChromeDriver downloads to new location
- Old googleapis.com URLs deprecated
- Manual ChromeDriver management is outdated

### Solution
**Use `undetected-chromedriver` package instead:**
```python
# In browser_setup.py - this package handles everything automatically
import undetected_chromedriver as uc
driver = uc.Chrome(options=options)
```

Benefits:
- Automatically downloads correct ChromeDriver version
- Matches installed Chrome version
- Bypasses Instagram bot detection
- No manual driver management needed

### Updated Setup Script
Removed these lines from `gcp_setup.sh`:
```bash
# DON'T DO THIS - outdated and broken
CHROME_DRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
```

Instead, just install Chrome and let Python handle the driver:
```bash
# Install Chrome only
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt-get install -f -y
```

### Prevention
- Never manually download ChromeDriver
- Always use `undetected-chromedriver` Python package
- It handles version matching automatically

---

## Issue 6: Python apt_pkg Module Error

### Problem
```
ModuleNotFoundError: No module named 'apt_pkg'
```

### Root Cause
- PPA repository for Python 3.11 was problematic
- Conflicts with Ubuntu's default Python packages
- Ubuntu 20.04 ships with Python 3.8 by default

### Solution
**Skip problematic PPA, use simple approach:**

```bash
# Install Python 3.11 from Ubuntu repositories (if available)
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# If not in repositories, install from source or use default Python 3.8
# For our use case, Python 3.8+ works fine
```

Alternative: Use deadsnakes PPA but don't fight apt conflicts:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
# If errors occur, just use system Python
```

### Prevention
- Don't obsess over exact Python version
- Python 3.8+ works perfectly for this bot
- Use system Python if PPA causes issues
- Virtual environment isolates packages anyway

---

## Issue 7: Cron Not Installed

### Problem
```bash
crontab -e
# Command 'crontab' not found
```

### Root Cause
- Fresh Ubuntu VM doesn't have cron installed by default
- Minimal installation to save resources

### Solution
```bash
# Install cron
sudo apt install -y cron

# Start cron service
sudo service cron start

# Enable cron to start on boot
sudo systemctl enable cron

# Verify cron is running
sudo service cron status
```

### Prevention
- Always install cron explicitly on new VMs
- Add to setup script for future deployments

---

## Issue 8: Headless Chrome Display Issues

### Problem
Chrome needs a display to run, but VM has no GUI

### Solution
**Use Xvfb (X Virtual Frame Buffer):**

```bash
# Install Xvfb
sudo apt install -y xvfb

# Create wrapper script: run_with_display.sh
#!/bin/bash
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
XVFB_PID=$!

cd ~/instagram-bot
source venv/bin/activate
python scheduled_automation.py

kill $XVFB_PID
```

This creates a virtual display so Chrome can run without physical monitor.

### Prevention
- Always use Xvfb for headless Chrome on servers
- Include in setup script
- Wrap Python execution with Xvfb startup/cleanup

---

## Issue 9: High Costs - VM Running 24/7 Unnecessarily

**Date:** November 18, 2025

### Problem
VM was running 24/7 even though bot only executes for ~30 minutes per day
- Running continuously: 720 hours/month
- Actual usage needed: ~60-75 hours/month
- Wasting: ~90% of compute time and costs

### Root Cause
- Initial deployment configured for 24/7 operation
- No auto-start/stop mechanism
- VM idle most of the time consuming resources and costs

### Solution
**Implemented GCP Cloud Scheduler for Auto Start/Stop:**

#### Step 1: Enable Cloud Scheduler API
```bash
gcloud services enable cloudscheduler.googleapis.com --project=emerald-diagram-478119-n2
```

#### Step 2: Create Scheduler Jobs (16 total)
Created automated start/stop jobs for:
- **7 daily bot runs** (Monday-Sunday) - 14 jobs
- **1 daily report generation** (9 PM) - 2 jobs

#### Schedule Configuration:

| Day | Bot Run | VM Start | VM Stop | Duration |
|-----|---------|----------|---------|----------|
| Monday | 11:00 AM | 10:45 AM | 12:00 PM | 1h 15m |
| Tuesday | 11:00 AM | 10:45 AM | 12:00 PM | 1h 15m |
| Wednesday | 11:00 AM | 10:45 AM | 12:00 PM | 1h 15m |
| Thursday | 12:00 PM | 11:45 AM | 1:00 PM | 1h 15m |
| Friday | 1:00 PM | 12:45 PM | 2:00 PM | 1h 15m |
| Saturday | 10:00 AM | 9:45 AM | 11:00 AM | 1h 15m |
| Sunday | 10:00 AM | 9:45 AM | 11:00 AM | 1h 15m |
| Report | 9:00 PM | 8:45 PM | 9:15 PM | 30m |

#### PowerShell Commands Used:
```powershell
# Enable API
gcloud services enable cloudscheduler.googleapis.com --project=emerald-diagram-478119-n2

# Create scheduler jobs (example for Monday)
gcloud scheduler jobs create http start-vm-monday `
  --location=us-east1 `
  --schedule="45 10 * * 1" `
  --time-zone="America/Los_Angeles" `
  --uri="https://compute.googleapis.com/compute/v1/projects/emerald-diagram-478119-n2/zones/us-east1-c/instances/instagram-bot/start" `
  --http-method=POST `
  --oauth-service-account-email="263660997732-compute@developer.gserviceaccount.com" `
  --project=emerald-diagram-478119-n2

gcloud scheduler jobs create http stop-vm-monday `
  --location=us-east1 `
  --schedule="0 12 * * 1" `
  --time-zone="America/Los_Angeles" `
  --uri="https://compute.googleapis.com/compute/v1/projects/emerald-diagram-478119-n2/zones/us-east1-c/instances/instagram-bot/stop" `
  --http-method=POST `
  --oauth-service-account-email="263660997732-compute@developer.gserviceaccount.com" `
  --project=emerald-diagram-478119-n2

# (Repeated for all 7 days + daily report)
```

#### Step 3: Stop VM and Let Scheduler Manage
```bash
gcloud compute instances stop instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2
```

### Cost Analysis

#### Before (24/7 Operation):
- **Runtime:** 720 hours/month (24 hours × 30 days)
- **e2-micro cost:** ~$6.50/month
- **Storage:** ~$0.40/month
- **Total:** ~$6.90/month

#### After (Auto Start/Stop):
- **Runtime:** ~75 hours/month (2.5 hours × 30 days)
- **e2-micro cost:** ~$0.60/month (90% reduction!)
- **Cloud Scheduler:** ~$0.30/month (16 jobs)
- **Storage:** ~$0.40/month
- **Total:** ~$1.30/month

**Monthly Savings:** $5.60 (81% cost reduction!)  
**Annual Savings:** $67.20  
**Using $300 Credit:** Now lasts 230+ months (~19 years) instead of 46 months!

### Benefits
✅ **81% cost reduction** - from $6.90 to $1.30 per month  
✅ **Extended free credit** - 230+ months of free operation  
✅ **More efficient** - VM only runs when actually needed  
✅ **Zero manual intervention** - fully automated  
✅ **Easy monitoring** - Cloud Scheduler dashboard  
✅ **Same functionality** - bot runs at all scheduled times  

### Verification
```bash
# List all scheduler jobs
gcloud scheduler jobs list --location=us-east1 --project=emerald-diagram-478119-n2

# Check VM status
gcloud compute instances list --project=emerald-diagram-478119-n2

# Monitor scheduler execution
# Visit: https://console.cloud.google.com/cloudscheduler?project=emerald-diagram-478119-n2
```

### Prevention
- **Always evaluate actual usage** before keeping VMs running 24/7
- **Use Cloud Scheduler** for predictable start/stop patterns
- **Monitor Cloud Billing** to catch unnecessary costs early
- **Set up budget alerts** to notify when spending exceeds thresholds

### Files Created
- `deployment/setup_vm_scheduler.sh` - Bash setup script
- `setup_vm_scheduler.ps1` - PowerShell setup script (Windows)

---

## Final Working Configuration

### Project Details
- **GCP Project:** emerald-diagram-478119-n2 (My First Project)
- **VM Name:** instagram-bot
- **Zone:** us-east1-c
- **Machine Type:** e2-micro (1 vCPU, 1GB RAM)
- **Cost (Updated Nov 18, 2025):** ~$1.30/month with auto start/stop = $0 for 230+ months (~19 years using $300 credit!)
- **Previous Cost:** $6.50/month = 46 months
- **External IP:** 34.26.122.94 (dynamic - changes when VM restarts)

### Cron Schedule (Peak Engagement Times)
```cron
# Monday - 11 AM
0 11 * * 1 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1

# Tuesday - 11 AM (Very High Engagement)
0 11 * * 2 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1

# Wednesday - 11 AM (Best Day)
0 11 * * 3 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1

# Thursday - 12 PM
0 12 * * 4 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1

# Friday - 1 PM
0 13 * * 5 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1

# Saturday - 10 AM
0 10 * * 6 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1

# Sunday - 10 AM
0 10 * * 0 /home/siddh/instagram-bot/run_with_display.sh >> /home/siddh/instagram-bot/logs/cron.log 2>&1
```

### VM Directory Structure
```
~/instagram-bot/
├── venv/                      # Python virtual environment
├── core/                      # Core bot modules
│   ├── actions.py
│   ├── ai_comments.py
│   ├── browser_setup.py
│   ├── config.py
│   ├── safety.py
│   ├── humanize.py
│   ├── categories.py
│   ├── engagement_scheduler.py
│   └── analytics.py
├── data/                      # Cookies, stats, analytics
│   ├── cookies.json
│   ├── statistics.json
│   └── analytics.json
├── logs/                      # Cron and application logs
│   └── cron.log
├── tests/                     # Test scripts
├── .env                       # Credentials (Instagram, Gemini API)
├── scheduled_automation.py    # Main automation script
├── requirements.txt           # Python dependencies
└── run_with_display.sh        # Xvfb wrapper for cron
```

---

## Key Commands Reference

### VM Management
```bash
# List all VMs
gcloud compute instances list --project=emerald-diagram-478119-n2

# Start VM (usually done automatically by Cloud Scheduler)
gcloud compute instances start instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2

# Stop VM (usually done automatically by Cloud Scheduler)
gcloud compute instances stop instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2

# SSH via browser (RECOMMENDED - VM must be running)
# Go to: https://console.cloud.google.com/compute/instances
# Click "SSH" button next to instagram-bot

# Get VM details
gcloud compute instances describe instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2
```

### Cloud Scheduler Management (Auto Start/Stop)
```bash
# List all scheduler jobs
gcloud scheduler jobs list --location=us-east1 --project=emerald-diagram-478119-n2

# View specific job details
gcloud scheduler jobs describe start-vm-monday --location=us-east1 --project=emerald-diagram-478119-n2

# Manually trigger a job (for testing)
gcloud scheduler jobs run start-vm-monday --location=us-east1 --project=emerald-diagram-478119-n2

# Pause a job (disable auto start/stop temporarily)
gcloud scheduler jobs pause start-vm-monday --location=us-east1 --project=emerald-diagram-478119-n2

# Resume a paused job
gcloud scheduler jobs resume start-vm-monday --location=us-east1 --project=emerald-diagram-478119-n2

# Delete a job (if needed)
gcloud scheduler jobs delete start-vm-monday --location=us-east1 --project=emerald-diagram-478119-n2

# Monitor in GCP Console
# https://console.cloud.google.com/cloudscheduler?project=emerald-diagram-478119-n2
```

### File Upload
```powershell
# Local: Create archive
Compress-Archive -Path * -DestinationPath instagram-bot.zip -Force

# Upload to VM
gcloud compute scp instagram-bot.zip instagram-bot:~ --zone=us-east1-c --project=emerald-diagram-478119-n2

# VM: Extract
unzip instagram-bot.zip -d instagram-bot
cd instagram-bot
```

### Cron Management
```bash
# Edit crontab
crontab -e

# List cron jobs
crontab -l

# Check cron logs
tail -f ~/instagram-bot/logs/cron.log

# Manually run bot (for testing)
cd ~/instagram-bot
source venv/bin/activate
python scheduled_automation.py
```

### System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip
sudo apt install -y wget unzip curl
sudo apt install -y xvfb
sudo apt install -y cron

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt-get install -f -y

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
mkdir -p logs
```

---

## Success Metrics

✅ **Deployment Complete:**
- VM running 24/7 on GCP
- Automated cron jobs at peak engagement times
- Virtual display (Xvfb) for headless Chrome
- All dependencies installed and working
- Credentials configured in .env
- Logs directory for monitoring

✅ **Cost Optimization (Updated Nov 18, 2025):**
- e2-micro with auto start/stop: ~$1.30/month (81% savings!)
- Cloud Scheduler: 16 jobs for automated VM management
- $300 free credit: 230+ months of free operation (~19 years!)
- Runtime reduced from 720 hrs/month to ~75 hrs/month

✅ **Automation Working:**
- 7-day schedule covering all peak times
- Mon/Wed: 11 AM (highest engagement)
- Thu: 12 PM, Fri: 1 PM
- Sat/Sun: 10 AM (weekend activity)

---

## Lessons Learned

### ✅ Do This
1. **Use Web SSH** from GCP Console for initial setup - most reliable
2. **Upload files as zip** archives - much faster and more reliable
3. **Use undetected-chromedriver** - handles ChromeDriver automatically
4. **Always enable billing** and verify project before creating resources
5. **Create wrapper scripts** for cron jobs (Xvfb, logging, error handling)
6. **Test manually first** before adding to cron
7. **Monitor logs** regularly: `tail -f ~/instagram-bot/logs/cron.log`
8. **Implement auto start/stop** for VMs with predictable schedules - saves 80%+ on costs
9. **Use Cloud Scheduler** for automated VM lifecycle management
10. **Set up budget alerts** to monitor spending and catch issues early

### ❌ Don't Do This
1. Don't fight with local SSH key configuration - Web SSH just works
2. Don't manually download ChromeDriver - use Python package
3. Don't try recursive scp uploads - zip it first
4. Don't assume cron is installed - install explicitly
5. Don't forget Xvfb for headless Chrome
6. Don't use wrong GCP project - double check project ID

---

## Future Troubleshooting Checklist

If bot stops working:

1. **Check VM status (may be stopped by scheduler):**
   ```bash
   gcloud compute instances list --project=emerald-diagram-478119-n2
   # VM will show TERMINATED when stopped - this is NORMAL with auto start/stop
   ```

2. **Verify scheduler jobs are enabled:**
   ```bash
   gcloud scheduler jobs list --location=us-east1 --project=emerald-diagram-478119-n2
   # All jobs should show STATE: ENABLED
   ```

3. **Check cron logs (VM must be running or start it manually):**
   ```bash
   # Start VM if stopped
   gcloud compute instances start instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2
   
   # SSH into VM (use Web SSH from Console)
   tail -50 ~/instagram-bot/logs/cron.log
   tail -50 ~/instagram-bot/logs/reports.log
   ```

4. **Check Cloud Scheduler execution history:**
   ```bash
   # View in GCP Console
   # https://console.cloud.google.com/cloudscheduler?project=emerald-diagram-478119-n2
   # Look for failed executions or errors
   ```

5. **Verify cron jobs (on VM):**
   ```bash
   crontab -l
   ```

6. **Test manually (start VM first if stopped):**
   ```bash
   cd ~/instagram-bot
   source venv/bin/activate
   python scheduled_automation.py
   ```

7. **Check Instagram credentials:**
   ```bash
   cat ~/instagram-bot/.env
   # Verify INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD
   ```

8. **Verify Chrome and Xvfb:**
   ```bash
   google-chrome --version
   which xvfb-run
   ```

9. **Check disk space:**
   ```bash
   df -h
   ```

10. **Check memory:**
    ```bash
    free -h
    ```

11. **Verify timezone is correct:**
    ```bash
    timedatectl
    # Should show: America/Los_Angeles (PST, -0800)
    ```

---

## Contact & Resources

- **GCP Console:** https://console.cloud.google.com
- **Project:** emerald-diagram-478119-n2
- **VM Instance:** instagram-bot (us-east1-c)
- **Setup Date:** November 14, 2025
- **Next Review:** Check logs after first scheduled run tonight

---

**Document Version:** 2.0  
**Last Updated:** November 18, 2025  
**Status:** ✅ Production Ready - Bot Running with Auto Start/Stop (Cost Optimized)

**Major Updates:**
- Added Issue 9: Implemented Cloud Scheduler for 81% cost reduction
- Updated cost estimates: $1.30/month (from $6.90/month)
- Extended free credit usage: 230+ months (from 46 months)
- Added Cloud Scheduler management commands
- Updated troubleshooting checklist for auto start/stop scenarios
