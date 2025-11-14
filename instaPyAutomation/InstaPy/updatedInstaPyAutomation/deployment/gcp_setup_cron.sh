#!/bin/bash
# Setup Cron Jobs for Instagram Automation on GCP
# Run this after uploading your bot files

set -e

echo "========================================================================"
echo "Setting up Cron Jobs for Peak Engagement Times"
echo "========================================================================"
echo ""

# Project directory
PROJECT_DIR="$HOME/instagram-bot"
PYTHON_PATH="$PROJECT_DIR/venv/bin/python"
SCRIPT_PATH="$PROJECT_DIR/scheduled_automation.py"

# Create wrapper script for xvfb
echo "📝 Creating Xvfb wrapper script..."
cat > $PROJECT_DIR/run_with_display.sh << 'EOF'
#!/bin/bash
# Wrapper to run automation with virtual display

export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
XVFB_PID=$!

# Wait for Xvfb to start
sleep 2

# Run the automation
cd ~/instagram-bot
source venv/bin/activate
python scheduled_automation.py

# Kill Xvfb
kill $XVFB_PID
EOF

chmod +x $PROJECT_DIR/run_with_display.sh

echo "⏰ Setting up cron jobs..."

# Backup existing crontab
crontab -l > /tmp/crontab_backup 2>/dev/null || true

# Create new crontab
cat > /tmp/instagram_cron << EOF
# Instagram Automation - Peak Engagement Times
# Format: minute hour day month weekday command

# Monday - 11:00 AM (Late morning break)
0 11 * * 1 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/monday.log 2>&1

# Tuesday - 11:00 AM (Mid-morning peak)
0 11 * * 2 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/tuesday.log 2>&1

# Wednesday - 11:00 AM (Best day - morning peak)
0 11 * * 3 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/wednesday.log 2>&1

# Thursday - 12:00 PM (Lunch hour)
0 12 * * 4 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/thursday.log 2>&1

# Friday - 1:00 PM (Lunch hour)
0 13 * * 5 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/friday.log 2>&1

# Saturday - 10:00 AM (Weekend morning)
0 10 * * 6 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/saturday.log 2>&1

# Sunday - 10:00 AM (Sunday morning browsing)
0 10 * * 0 $PROJECT_DIR/run_with_display.sh >> $PROJECT_DIR/logs/sunday.log 2>&1

EOF

# Install crontab
crontab /tmp/instagram_cron

# Create logs directory
mkdir -p $PROJECT_DIR/logs

echo ""
echo "========================================================================"
echo "✅ Cron Jobs Installed Successfully!"
echo "========================================================================"
echo ""
echo "📅 Scheduled Times:"
echo "  Monday:    11:00 AM"
echo "  Tuesday:   11:00 AM"
echo "  Wednesday: 11:00 AM (Best day!)"
echo "  Thursday:  12:00 PM"
echo "  Friday:    1:00 PM"
echo "  Saturday:  10:00 AM"
echo "  Sunday:    10:00 AM"
echo ""
echo "📊 View cron jobs:  crontab -l"
echo "📝 View logs:       tail -f ~/instagram-bot/logs/monday.log"
echo "🗑️  Remove cron:     crontab -r"
echo ""
echo "⏱️  Times are in server timezone. Check with: timedatectl"
echo ""
