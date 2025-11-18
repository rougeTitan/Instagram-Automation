# PowerShell Script to Download and View Latest Report from GCP
# Run this from your local Windows machine

param(
    [string]$VMName = "instagram-bot",
    [string]$Zone = "us-east1-c",
    [string]$Project = "emerald-diagram-478119-n2",
    [switch]$JSON,
    [switch]$OpenBrowser
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instagram Bot - Report Viewer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create local reports directory
$LocalReportsDir = ".\reports"
if (-not (Test-Path $LocalReportsDir)) {
    New-Item -ItemType Directory -Path $LocalReportsDir | Out-Null
    Write-Host "✓ Created local reports directory" -ForegroundColor Green
}

# Generate filename with timestamp
$Timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"

if ($JSON) {
    # Download JSON report
    $LocalFile = "$LocalReportsDir\report_$Timestamp.json"
    Write-Host "→ Downloading JSON report from GCP..." -ForegroundColor Yellow
    
    gcloud compute scp "${VMName}:~/instagram-bot/reports/latest.json" $LocalFile `
        --zone=$Zone `
        --project=$Project
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Report downloaded: $LocalFile" -ForegroundColor Green
        Write-Host ""
        
        # Display JSON content
        Write-Host "Report Contents:" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Get-Content $LocalFile | ConvertFrom-Json | ConvertTo-Json -Depth 10
        Write-Host "----------------------------------------" -ForegroundColor Cyan
    } else {
        Write-Host "✗ Failed to download report" -ForegroundColor Red
        exit 1
    }
} else {
    # Download HTML report
    $LocalFile = "$LocalReportsDir\report_$Timestamp.html"
    Write-Host "→ Downloading HTML report from GCP..." -ForegroundColor Yellow
    
    gcloud compute scp "${VMName}:~/instagram-bot/reports/latest.html" $LocalFile `
        --zone=$Zone `
        --project=$Project
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Report downloaded: $LocalFile" -ForegroundColor Green
        Write-Host ""
        
        if ($OpenBrowser) {
            Write-Host "→ Opening report in browser..." -ForegroundColor Yellow
            Start-Process $LocalFile
            Write-Host "✓ Report opened in default browser" -ForegroundColor Green
        } else {
            Write-Host "💡 To open the report, run:" -ForegroundColor Yellow
            Write-Host "   .\view_latest_report.ps1 -OpenBrowser" -ForegroundColor White
            Write-Host ""
            Write-Host "   Or open manually:" -ForegroundColor Yellow
            Write-Host "   $LocalFile" -ForegroundColor White
        }
    } else {
        Write-Host "✗ Failed to download report" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Available Commands:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "View HTML report:" -ForegroundColor Yellow
Write-Host "  .\view_latest_report.ps1 -OpenBrowser" -ForegroundColor White
Write-Host ""
Write-Host "View JSON data:" -ForegroundColor Yellow
Write-Host "  .\view_latest_report.ps1 -JSON" -ForegroundColor White
Write-Host ""
Write-Host "All reports saved in: .\reports\" -ForegroundColor Yellow
Write-Host ""
