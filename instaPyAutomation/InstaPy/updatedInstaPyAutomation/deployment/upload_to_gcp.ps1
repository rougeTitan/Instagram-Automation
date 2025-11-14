# Upload Bot to Google Cloud VM
# Run this from your Windows PC after creating the VM

param(
    [Parameter(Mandatory=$true)]
    [string]$VMName,
    
    [Parameter(Mandatory=$false)]
    [string]$Zone = "us-central1-a",
    
    [Parameter(Mandatory=$false)]
    [string]$Project = ""
)

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Instagram Bot - Upload to Google Cloud VM" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud version --format="value(version)" 2>$null
    Write-Host "✓ Google Cloud SDK detected: $gcloudVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Google Cloud SDK not found!" -ForegroundColor Red
    Write-Host "Please install from: https://cloud.google.com/sdk/install" -ForegroundColor Yellow
    exit 1
}

Write-Host "VM Name: $VMName" -ForegroundColor Green
Write-Host "Zone: $Zone" -ForegroundColor Green
Write-Host ""

# Get project directory
$ProjectDir = Split-Path -Parent $PSScriptRoot

Write-Host "Uploading files from: $ProjectDir" -ForegroundColor Yellow
Write-Host ""

# Create remote directory
Write-Host "Creating remote directory..." -ForegroundColor Yellow
if ($Project) {
    gcloud compute ssh $VMName --zone=$Zone --project=$Project --command="mkdir -p ~/instagram-bot"
} else {
    gcloud compute ssh $VMName --zone=$Zone --command="mkdir -p ~/instagram-bot"
}

# Upload files
Write-Host "Uploading project files..." -ForegroundColor Cyan

$itemsToUpload = @(
    "core",
    "data", 
    "docs",
    "tests",
    "deployment",
    "scheduled_automation.py",
    "main.py",
    ".env",
    "requirements.txt"
)

foreach ($item in $itemsToUpload) {
    $sourcePath = Join-Path $ProjectDir $item
    
    if (Test-Path $sourcePath) {
        Write-Host "Uploading $item..." -ForegroundColor Cyan
        
        if ($Project) {
            gcloud compute scp --recurse $sourcePath ${VMName}:~/instagram-bot/ --zone=$Zone --project=$Project
        } else {
            gcloud compute scp --recurse $sourcePath ${VMName}:~/instagram-bot/ --zone=$Zone
        }
        
        Write-Host "  ✓ $item uploaded" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Skipping $item (not found)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "✅ Upload Complete!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan

if ($Project) {
    Write-Host "1. SSH into VM: gcloud compute ssh $VMName --zone=$Zone --project=$Project" -ForegroundColor White
} else {
    Write-Host "1. SSH into VM: gcloud compute ssh $VMName --zone=$Zone" -ForegroundColor White
}

Write-Host "2. Run setup: cd ~/instagram-bot/deployment && chmod +x gcp_setup_cron.sh && ./gcp_setup_cron.sh" -ForegroundColor White
Write-Host ""
