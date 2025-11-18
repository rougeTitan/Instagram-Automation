#!/bin/bash
# Setup Daily Report Generation on GCP VM
# This script configures automatic report generation at 9 PM every day

echo "=========================================="
echo "Daily Report Setup for Instagram Bot"
echo "=========================================="
echo ""

# Get the bot directory
BOT_DIR="$HOME/instagram-bot"

if [ ! -d "$BOT_DIR" ]; then
    echo "Error: Bot directory not found at $BOT_DIR"
    exit 1
fi

echo "Bot directory: $BOT_DIR"
echo ""

# Create reports directory
echo "→ Creating reports directory..."
mkdir -p "$BOT_DIR/reports"
echo "✓ Reports directory created"
echo ""

# Create wrapper script for report generation
echo "→ Creating report wrapper script..."
cat > "$BOT_DIR/run_daily_report.sh" << 'EOF'
#!/bin/bash
# Wrapper script to run daily report generation

export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
XVFB_PID=$!

cd ~/instagram-bot
source venv/bin/activate

echo "=========================================="
echo "Generating Daily Report"
echo "Date: $(date)"
echo "=========================================="
echo ""

python generate_daily_report.py

echo ""
echo "✓ Report generation completed"
echo ""

kill $XVFB_PID 2>/dev/null

EOF

chmod +x "$BOT_DIR/run_daily_report.sh"
echo "✓ Report wrapper script created"
echo ""

# Setup cron job for 9 PM daily
echo "→ Setting up cron job for daily reports (9 PM)..."

# Create temporary crontab file
TEMP_CRON=$(mktemp)

# Get existing crontab (if any)
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Remove any existing daily report cron jobs
sed -i '/run_daily_report.sh/d' "$TEMP_CRON"

# Add new cron job for 9 PM every day
echo "# Generate daily Instagram bot report at 9 PM" >> "$TEMP_CRON"
echo "0 21 * * * $BOT_DIR/run_daily_report.sh >> $BOT_DIR/logs/reports.log 2>&1" >> "$TEMP_CRON"
echo "" >> "$TEMP_CRON"

# Install new crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "✓ Cron job configured"
echo ""

# Display current crontab
echo "Current scheduled jobs:"
echo "----------------------------------------"
crontab -l
echo "----------------------------------------"
echo ""

# Test report generation
echo "→ Testing report generation..."
echo ""
cd "$BOT_DIR"
source venv/bin/activate
python generate_daily_report.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Daily reports will be generated at 9 PM every day"
    echo "Reports location: $BOT_DIR/reports/"
    echo ""
    echo "Available files:"
    echo "  • daily_report_YYYY-MM-DD.html (dated reports)"
    echo "  • daily_report_YYYY-MM-DD.json (dated JSON data)"
    echo "  • latest.html (always the most recent)"
    echo "  • latest.json (always the most recent)"
    echo ""
    echo "To view reports:"
    echo "  1. Download: gcloud compute scp instagram-bot:~/instagram-bot/reports/latest.html . --zone=us-east1-c"
    echo "  2. Or view on VM: cat ~/instagram-bot/reports/latest.json | python -m json.tool"
    echo ""
    echo "To manually generate a report:"
    echo "  cd ~/instagram-bot && ./run_daily_report.sh"
    echo ""
    echo "Logs location: $BOT_DIR/logs/reports.log"
    echo ""
else
    echo ""
    echo "⚠ Test failed. Please check the error messages above."
    exit 1
fi
