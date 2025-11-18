# Daily Reports Setup Guide

## 📊 Automated Daily Reports at 9 PM

Your Instagram automation bot now generates comprehensive performance reports every day at 9 PM, automatically saved on your GCP VM.

---

## 🎯 What's Included

### Reports Generated Daily:
1. **HTML Report** (`daily_report_YYYY-MM-DD.html`)
   - Beautiful, styled dashboard
   - Visual stats and charts
   - Easy to read in any browser

2. **JSON Report** (`daily_report_YYYY-MM-DD.json`)
   - Raw data for programmatic access
   - API-friendly format
   - Perfect for integrations

3. **Latest Reports** (always current)
   - `latest.html` - Most recent HTML report
   - `latest.json` - Most recent JSON data

---

## 📍 Report Locations

**On GCP VM:**
```
~/instagram-bot/reports/
├── daily_report_2025-11-18.html
├── daily_report_2025-11-18.json
├── daily_report_2025-11-19.html
├── daily_report_2025-11-19.json
├── latest.html  ← Always the newest
└── latest.json  ← Always the newest
```

**Logs:**
```
~/instagram-bot/logs/reports.log  ← Report generation logs
```

---

## 🚀 Setup Instructions

### Step 1: Upload Files to GCP

From your local Windows machine:

```powershell
# Navigate to your project folder
cd C:\Projects\instaPyAutomation\InstaPy\updatedInstaPyAutomation

# Upload the new files to GCP
gcloud compute scp generate_daily_report.py instagram-bot:~/instagram-bot/ --zone=us-east1-c --project=emerald-diagram-478119-n2

gcloud compute scp deployment/setup_daily_reports.sh instagram-bot:~/instagram-bot/deployment/ --zone=us-east1-c --project=emerald-diagram-478119-n2
```

### Step 2: Run Setup on GCP VM

Connect to your VM:

```powershell
gcloud compute ssh instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2
```

Then run the setup:

```bash
cd ~/instagram-bot/deployment
chmod +x setup_daily_reports.sh
./setup_daily_reports.sh
```

This will:
- ✅ Create reports directory
- ✅ Setup cron job for 9 PM daily
- ✅ Generate a test report
- ✅ Configure automatic report generation

### Step 3: Verify Setup

Check that the cron job is scheduled:

```bash
crontab -l | grep report
```

You should see:
```
0 21 * * * /home/YOUR_USER/instagram-bot/run_daily_report.sh >> /home/YOUR_USER/instagram-bot/logs/reports.log 2>&1
```

---

## 📥 How to View Reports

### Option 1: Download with PowerShell Script (Easiest)

From your local Windows machine:

```powershell
# Download and open HTML report in browser
.\view_latest_report.ps1 -OpenBrowser

# Download JSON data
.\view_latest_report.ps1 -JSON
```

### Option 2: Manual Download via gcloud

```powershell
# Download latest HTML report
gcloud compute scp instagram-bot:~/instagram-bot/reports/latest.html ./latest_report.html --zone=us-east1-c --project=emerald-diagram-478119-n2

# Open in browser
Start-Process .\latest_report.html
```

### Option 3: View Directly on VM

```bash
# SSH into VM
gcloud compute ssh instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2

# View JSON report in terminal
cat ~/instagram-bot/reports/latest.json | python -m json.tool

# List all reports
ls -lh ~/instagram-bot/reports/
```

### Option 4: Simple HTTP Server (Access from Browser)

On the VM:

```bash
cd ~/instagram-bot/reports
python3 -m http.server 8080
```

Then access via browser:
```
http://YOUR_VM_EXTERNAL_IP:8080/latest.html
```

**Note:** You'll need to configure firewall rules to allow port 8080.

---

## 📊 What's in the Report

### Quick Stats
- Total actions performed (last 7 days)
- Posts liked
- Comments posted
- Daily average activity

### Engagement Analysis
- Engagement rate with status indicator
- Performance comparison
- Recommendations

### Execution History
- Recent bot runs by day
- Posts processed
- Comments and likes given
- Success rates

### Optimal Timing
- **Best posting times** (top 5 hours)
- **Best posting days** (ranked by engagement)
- Recommended schedule

### Hashtag Performance
- Top performing hashtags
- Usage statistics
- Average engagement per hashtag

### Growth Metrics
- Follower growth (30-day trend)
- Growth rate percentage
- Historical data

### Recommendations
- Personalized action items
- Strategy suggestions
- Optimization tips

---

## 🕐 Schedule

Reports are automatically generated:
- **Time:** 9:00 PM (21:00) every day
- **Timezone:** Based on your VM's timezone setting
- **Logs:** Saved to `~/instagram-bot/logs/reports.log`

### To Check VM Timezone:

```bash
timedatectl
```

### To Change Timezone:

```bash
# Example: US Pacific Time
sudo timedatectl set-timezone America/Los_Angeles

# Example: US Eastern Time
sudo timedatectl set-timezone America/New_York

# Example: India
sudo timedatectl set-timezone Asia/Kolkata
```

---

## 🔧 Manual Report Generation

Generate a report anytime:

```bash
# SSH into VM
gcloud compute ssh instagram-bot --zone=us-east1-c --project=emerald-diagram-478119-n2

# Run report generation
cd ~/instagram-bot
./run_daily_report.sh
```

Or run directly:

```bash
cd ~/instagram-bot
source venv/bin/activate
python generate_daily_report.py
```

---

## 📋 Report File Details

### HTML Report Features:
- 📱 Responsive design (mobile-friendly)
- 🎨 Beautiful gradient styling
- 📊 Data tables and stats cards
- 💡 Color-coded recommendations
- 🔥 Engagement status indicators

### JSON Report Structure:
```json
{
  "generated_at": "2025-11-18T21:00:00",
  "report_date": "2025-11-18",
  "engagement_rate": 4.5,
  "activity_last_7_days": {
    "total_actions": 70,
    "likes": 35,
    "comments": 35,
    "avg_actions_per_day": 10
  },
  "best_posting_times": [...],
  "best_posting_days": [...],
  "top_hashtags": [...],
  "recent_executions": [...]
}
```

---

## 🔍 Monitoring & Logs

### Check Report Generation Logs:

```bash
# View recent logs
tail -50 ~/instagram-bot/logs/reports.log

# Watch logs in real-time
tail -f ~/instagram-bot/logs/reports.log

# Check for errors
grep -i error ~/instagram-bot/logs/reports.log
```

### Verify Cron Execution:

```bash
# Check system cron logs
grep "run_daily_report" /var/log/syslog | tail -20
```

---

## 🎯 Quick Command Reference

### From Windows (Local Machine):

```powershell
# Download and view latest HTML report
.\view_latest_report.ps1 -OpenBrowser

# Download JSON data
.\view_latest_report.ps1 -JSON

# Upload updated report generator
gcloud compute scp generate_daily_report.py instagram-bot:~/instagram-bot/ --zone=us-east1-c
```

### On GCP VM:

```bash
# Generate report manually
cd ~/instagram-bot && ./run_daily_report.sh

# View latest report (JSON)
cat ~/instagram-bot/reports/latest.json | python -m json.tool

# List all reports
ls -lh ~/instagram-bot/reports/

# Check report logs
tail -f ~/instagram-bot/logs/reports.log

# View cron schedule
crontab -l
```

---

## 🐛 Troubleshooting

### Report Not Generating at 9 PM

**Check cron job:**
```bash
crontab -l | grep report
```

**Check cron service:**
```bash
sudo service cron status
```

**View cron logs:**
```bash
grep CRON /var/log/syslog | tail -20
```

### Reports Directory Missing

```bash
mkdir -p ~/instagram-bot/reports
```

### Permission Issues

```bash
chmod +x ~/instagram-bot/run_daily_report.sh
chmod +x ~/instagram-bot/deployment/setup_daily_reports.sh
```

### No Data in Reports

The bot needs to run a few times to collect data. Reports show:
- "Not enough data yet" - for new deployments
- Data populates after bot runs multiple times
- Give it a few days to build analytics

### Download Failed from Windows

Make sure gcloud is configured:
```powershell
gcloud config list
gcloud auth list
```

---

## 💡 Pro Tips

### 1. **Set Up Budget Alerts**
- Reports are lightweight (few KB each)
- Minimal cost impact
- Monitor in GCP Console → Billing

### 2. **Automate Report Downloads**
Schedule a Windows Task to download reports daily:
```powershell
# Create scheduled task to run daily at 9:30 PM
schtasks /create /tn "Download Instagram Report" /tr "powershell -File C:\Path\To\view_latest_report.ps1 -OpenBrowser" /sc daily /st 21:30
```

### 3. **Email Reports (Advanced)**
Modify `generate_daily_report.py` to send email:
- Use Gmail SMTP
- Send HTML report as email body
- Attach JSON for records

### 4. **Share Reports**
- Upload HTML to cloud storage
- Share link with team/clients
- Password protect with HTTP auth

### 5. **Archive Old Reports**
```bash
# Keep last 30 days only
find ~/instagram-bot/reports/ -name "daily_report_*.html" -mtime +30 -delete
find ~/instagram-bot/reports/ -name "daily_report_*.json" -mtime +30 -delete
```

---

## 🎓 Next Steps

1. ✅ Run setup script on GCP VM
2. ✅ Wait for first report at 9 PM tonight
3. ✅ Download and review using `view_latest_report.ps1`
4. ✅ Check reports daily to track performance
5. ✅ Adjust bot strategy based on insights

---

## 📚 Related Files

- `generate_daily_report.py` - Report generator script
- `view_latest_report.ps1` - Windows download script
- `deployment/setup_daily_reports.sh` - GCP setup script
- `core/analytics.py` - Analytics engine
- `logs/reports.log` - Report generation logs

---

## 🆘 Need Help?

**Common Issues:**
- Reports not showing data → Wait for bot to run a few times
- Can't download → Check gcloud authentication
- Timezone wrong → Use `timedatectl set-timezone`
- Cron not running → Check `sudo service cron status`

**Check System Status:**
```bash
# Full system check
cd ~/instagram-bot
echo "=== Cron Jobs ===" && crontab -l
echo "=== Reports ===" && ls -lh reports/
echo "=== Logs ===" && tail -20 logs/reports.log
```

---

**Happy Monitoring! 📊🚀**

Your Instagram bot now provides daily insights to optimize your growth strategy!
