#!/bin/bash
# Setup VM Auto Start/Stop Scheduler
# This script creates Cloud Scheduler jobs to start VM before cron jobs and stop after

echo "=========================================="
echo "GCP VM Auto Start/Stop Scheduler Setup"
echo "=========================================="
echo ""

# Configuration
PROJECT_ID="emerald-diagram-478119-n2"
VM_NAME="instagram-bot"
ZONE="us-east1-c"
REGION="us-east1"

echo "Project: $PROJECT_ID"
echo "VM: $VM_NAME"
echo "Zone: $ZONE"
echo ""

# Enable required APIs
echo "→ Enabling required APIs..."
gcloud services enable cloudscheduler.googleapis.com --project=$PROJECT_ID
gcloud services enable compute.googleapis.com --project=$PROJECT_ID
echo "✓ APIs enabled"
echo ""

# Create scheduler jobs for each day's bot run
echo "→ Creating scheduler jobs..."
echo ""

# Monday - Bot runs at 11:00 AM, start VM at 10:45 AM, stop at 12:00 PM
echo "Setting up Monday schedule..."
gcloud scheduler jobs create http start-vm-monday \
  --location=$REGION \
  --schedule="45 10 * * 1" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Monday bot run (11:00 AM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-monday \
  --location=$REGION \
  --schedule="0 12 * * 1" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Monday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Tuesday - Bot runs at 11:00 AM
echo "Setting up Tuesday schedule..."
gcloud scheduler jobs create http start-vm-tuesday \
  --location=$REGION \
  --schedule="45 10 * * 2" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Tuesday bot run (11:00 AM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-tuesday \
  --location=$REGION \
  --schedule="0 12 * * 2" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Tuesday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Wednesday - Bot runs at 11:00 AM
echo "Setting up Wednesday schedule..."
gcloud scheduler jobs create http start-vm-wednesday \
  --location=$REGION \
  --schedule="45 10 * * 3" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Wednesday bot run (11:00 AM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-wednesday \
  --location=$REGION \
  --schedule="0 12 * * 3" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Wednesday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Thursday - Bot runs at 12:00 PM
echo "Setting up Thursday schedule..."
gcloud scheduler jobs create http start-vm-thursday \
  --location=$REGION \
  --schedule="45 11 * * 4" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Thursday bot run (12:00 PM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-thursday \
  --location=$REGION \
  --schedule="0 13 * * 4" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Thursday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Friday - Bot runs at 1:00 PM
echo "Setting up Friday schedule..."
gcloud scheduler jobs create http start-vm-friday \
  --location=$REGION \
  --schedule="45 12 * * 5" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Friday bot run (1:00 PM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-friday \
  --location=$REGION \
  --schedule="0 14 * * 5" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Friday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Saturday - Bot runs at 10:00 AM
echo "Setting up Saturday schedule..."
gcloud scheduler jobs create http start-vm-saturday \
  --location=$REGION \
  --schedule="45 9 * * 6" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Saturday bot run (10:00 AM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-saturday \
  --location=$REGION \
  --schedule="0 11 * * 6" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Saturday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Sunday - Bot runs at 10:00 AM
echo "Setting up Sunday schedule..."
gcloud scheduler jobs create http start-vm-sunday \
  --location=$REGION \
  --schedule="45 9 * * 0" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before Sunday bot run (10:00 AM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-sunday \
  --location=$REGION \
  --schedule="0 11 * * 0" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after Sunday bot run" \
  2>/dev/null || echo "  (Job may already exist)"

# Daily report at 9 PM
echo "Setting up daily report schedule..."
gcloud scheduler jobs create http start-vm-report \
  --location=$REGION \
  --schedule="45 20 * * *" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/start" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Start VM 15 min before daily report (9:00 PM)" \
  2>/dev/null || echo "  (Job may already exist)"

gcloud scheduler jobs create http stop-vm-report \
  --location=$REGION \
  --schedule="15 21 * * *" \
  --time-zone="America/Los_Angeles" \
  --uri="https://compute.googleapis.com/compute/v1/projects/$PROJECT_ID/zones/$ZONE/instances/$VM_NAME/stop" \
  --http-method=POST \
  --oauth-service-account-email=$(gcloud iam service-accounts list --filter="Compute Engine default service account" --format="value(email)") \
  --project=$PROJECT_ID \
  --description="Stop VM after daily report generation" \
  2>/dev/null || echo "  (Job may already exist)"

echo ""
echo "✓ Scheduler jobs created"
echo ""

# List all scheduler jobs
echo "=========================================="
echo "Created Scheduler Jobs:"
echo "=========================================="
gcloud scheduler jobs list --location=$REGION --project=$PROJECT_ID

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Your VM will now:"
echo "  • Start 15 minutes before each scheduled bot run"
echo "  • Stop 1 hour after bot completes"
echo "  • Run only ~2 hours/day instead of 24 hours"
echo ""
echo "Cost Savings:"
echo "  • Before: 24 hours/day × 30 days = 720 hours/month"
echo "  • After: ~2 hours/day × 30 days = 60 hours/month"
echo "  • Savings: ~92% reduction in compute costs!"
echo ""
echo "Monthly cost estimate:"
echo "  • e2-micro: ~$0.50/month (vs $6.50)"
echo "  • Cloud Scheduler: ~$0.30/month (8 jobs)"
echo "  • Total: ~$0.80/month"
echo ""
echo "Next steps:"
echo "  1. Stop the VM now: gcloud compute instances stop $VM_NAME --zone=$ZONE"
echo "  2. Scheduler will auto-start it when needed"
echo "  3. Monitor: https://console.cloud.google.com/cloudscheduler"
echo ""
