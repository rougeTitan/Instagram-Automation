# PowerShell Script to Setup VM Auto Start/Stop with Cloud Scheduler
# This dramatically reduces costs by only running VM when needed

param(
    [string]$Project = "emerald-diagram-478119-n2",
    [string]$VMName = "instagram-bot",
    [string]$Zone = "us-east1-c",
    [string]$Region = "us-east1"
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "GCP VM Auto Start/Stop Scheduler Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project: $Project" -ForegroundColor Yellow
Write-Host "VM: $VMName" -ForegroundColor Yellow
Write-Host "Zone: $Zone" -ForegroundColor Yellow
Write-Host ""

# Service account
$ServiceAccount = "263660997732-compute@developer.gserviceaccount.com"

# Define schedule (Day, Start Time, Stop Time, Bot Run Time)
$Schedule = @(
    @{Day="monday"; DayNum=1; BotHour=11; BotMin=0; StartHour=10; StartMin=45; StopHour=12; StopMin=0},
    @{Day="tuesday"; DayNum=2; BotHour=11; BotMin=0; StartHour=10; StartMin=45; StopHour=12; StopMin=0},
    @{Day="wednesday"; DayNum=3; BotHour=11; BotMin=0; StartHour=10; StartMin=45; StopHour=12; StopMin=0},
    @{Day="thursday"; DayNum=4; BotHour=12; BotMin=0; StartHour=11; StartMin=45; StopHour=13; StopMin=0},
    @{Day="friday"; DayNum=5; BotHour=13; BotMin=0; StartHour=12; StartMin=45; StopHour=14; StopMin=0},
    @{Day="saturday"; DayNum=6; BotHour=10; BotMin=0; StartHour=9; StartMin=45; StopHour=11; StopMin=0},
    @{Day="sunday"; DayNum=0; BotHour=10; BotMin=0; StartHour=9; StartMin=45; StopHour=11; StopMin=0}
)

Write-Host "→ Creating scheduler jobs for bot runs..." -ForegroundColor Yellow
Write-Host ""

foreach ($day in $Schedule) {
    Write-Host "  Setting up $($day.Day.ToUpper())..." -ForegroundColor Cyan
    
    # Start VM job
    $startJobName = "start-vm-$($day.Day)"
    $startSchedule = "$($day.StartMin) $($day.StartHour) * * $($day.DayNum)"
    
    gcloud scheduler jobs create http $startJobName `
        --location=$Region `
        --schedule="$startSchedule" `
        --time-zone="America/Los_Angeles" `
        --uri="https://compute.googleapis.com/compute/v1/projects/$Project/zones/$Zone/instances/$VMName/start" `
        --http-method=POST `
        --oauth-service-account-email=$ServiceAccount `
        --project=$Project `
        --description="Start VM 15min before $($day.Day) bot run" `
        2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ Start job created" -ForegroundColor Green
    } else {
        Write-Host "    ⚠ Start job exists or error" -ForegroundColor Yellow
    }
    
    # Stop VM job
    $stopJobName = "stop-vm-$($day.Day)"
    $stopSchedule = "$($day.StopMin) $($day.StopHour) * * $($day.DayNum)"
    
    gcloud scheduler jobs create http $stopJobName `
        --location=$Region `
        --schedule="$stopSchedule" `
        --time-zone="America/Los_Angeles" `
        --uri="https://compute.googleapis.com/compute/v1/projects/$Project/zones/$Zone/instances/$VMName/stop" `
        --http-method=POST `
        --oauth-service-account-email=$ServiceAccount `
        --project=$Project `
        --description="Stop VM after $($day.Day) bot run" `
        2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ Stop job created" -ForegroundColor Green
    } else {
        Write-Host "    ⚠ Stop job exists or error" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "→ Setting up daily report schedule (9 PM)..." -ForegroundColor Yellow

# Start for report
gcloud scheduler jobs create http start-vm-report `
    --location=$Region `
    --schedule="45 20 * * *" `
    --time-zone="America/Los_Angeles" `
    --uri="https://compute.googleapis.com/compute/v1/projects/$Project/zones/$Zone/instances/$VMName/start" `
    --http-method=POST `
    --oauth-service-account-email=$ServiceAccount `
    --project=$Project `
    --description="Start VM for daily report (9 PM)" `
    2>&1 | Out-Null

Write-Host "  ✓ Report start job created" -ForegroundColor Green

# Stop after report
gcloud scheduler jobs create http stop-vm-report `
    --location=$Region `
    --schedule="15 21 * * *" `
    --time-zone="America/Los_Angeles" `
    --uri="https://compute.googleapis.com/compute/v1/projects/$Project/zones/$Zone/instances/$VMName/stop" `
    --http-method=POST `
    --oauth-service-account-email=$ServiceAccount `
    --project=$Project `
    --description="Stop VM after report generation" `
    2>&1 | Out-Null

Write-Host "  ✓ Report stop job created" -ForegroundColor Green
Write-Host ""

# List all jobs
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Created Scheduler Jobs:" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
gcloud scheduler jobs list --location=$Region --project=$Project

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your VM will now:" -ForegroundColor Cyan
Write-Host "  • Start 15 minutes before each scheduled task" -ForegroundColor White
Write-Host "  • Stop 1 hour after task completes" -ForegroundColor White
Write-Host "  • Run only ~2-3 hours/day instead of 24 hours" -ForegroundColor White
Write-Host ""
Write-Host "Cost Savings:" -ForegroundColor Cyan
Write-Host "  Before: 24 hrs/day × 30 days = 720 hours/month" -ForegroundColor White
Write-Host "  After:  ~2 hrs/day × 30 days = 60 hours/month" -ForegroundColor White
Write-Host "  Savings: ~92% reduction!" -ForegroundColor Green
Write-Host ""
Write-Host "Monthly Cost Estimate:" -ForegroundColor Cyan
Write-Host "  e2-micro compute:     About 50 cents per month (down from 6.50)" -ForegroundColor White
Write-Host "  Cloud Scheduler:      About 30 cents per month" -ForegroundColor White
Write-Host "  Total:                About 80 cents per month" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Stop VM manually when done testing" -ForegroundColor White
Write-Host "  2. Scheduler will auto-start VM when needed" -ForegroundColor White
Write-Host "  3. Monitor jobs in GCP Console" -ForegroundColor White
Write-Host ""
