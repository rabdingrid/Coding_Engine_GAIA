#!/bin/bash
# Azure Monitoring & Alerting Setup Script
# This script sets up comprehensive monitoring with Email and Slack notifications

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

RESOURCE_GROUP="ai-ta-2"
SUBSCRIPTION_ID="dab771f2-8670-4bf4-8067-ea813decb669"
LOCATION="eastus2"

# Notification Settings
ADMIN_EMAIL="rabdin@griddynamics.com"
SLACK_WEBHOOK_URL=""  # Add your Slack webhook URL here

# Resource IDs
BACKEND_APP_ID="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/containerApps/ai-ta-ra-coding-engine"
SESSION_POOL_ID="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/sessionPools/ai-ta-RA-session-pool"

# ============================================================================
# FUNCTIONS
# ============================================================================

check_login() {
    echo "🔐 Checking Azure login..."
    az account show &>/dev/null || {
        echo "❌ Not logged in. Please run: az login"
        exit 1
    }
    az account set --subscription "$SUBSCRIPTION_ID"
    echo "✅ Logged in to subscription: $SUBSCRIPTION_ID"
}

# ============================================================================
# STEP 1: CREATE ACTION GROUP
# ============================================================================

create_action_group() {
    echo "================================================"
    echo "📧 Creating Action Group with Email..."
    echo "================================================"
    
    # Create action group with email
    az monitor action-group create \
        --name "CodingEngineAlerts" \
        --resource-group "$RESOURCE_GROUP" \
        --short-name "CodeAlert" \
        --email-receiver \
            name="AdminEmail" \
            email-address="$ADMIN_EMAIL" \
            use-common-alert-schema=true
    
    echo "✅ Action group created with email: $ADMIN_EMAIL"
    
    # Add Slack webhook if provided
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        echo "💬 Adding Slack webhook..."
        az monitor action-group update \
            --name "CodingEngineAlerts" \
            --resource-group "$RESOURCE_GROUP" \
            --add-action \
                webhook \
                name="SlackWebhook" \
                service-uri="$SLACK_WEBHOOK_URL" \
                use-common-alert-schema=true
        echo "✅ Slack webhook added"
    else
        echo "⚠️  Slack webhook URL not provided. Skipping Slack integration."
        echo "   To add later, update SLACK_WEBHOOK_URL in this script and re-run."
    fi
}

# ============================================================================
# STEP 2: CREATE BUDGET ALERT
# ============================================================================

create_budget_alert() {
    echo "================================================"
    echo "💰 Creating Cost Budget Alert..."
    echo "================================================"
    
    az consumption budget create \
        --budget-name "CodingEngineDailyBudget" \
        --category Cost \
        --amount 10 \
        --time-grain Monthly \
        --time-period start-date=$(date +%Y-%m-01) \
        --resource-group "$RESOURCE_GROUP" \
        --notifications \
            threshold=80 \
            operator=GreaterThan \
            contact-emails="$ADMIN_EMAIL" \
            contact-roles="Owner"
    
    echo "✅ Budget alert created: $10/day threshold"
}

# ============================================================================
# STEP 3: CREATE METRIC ALERTS
# ============================================================================

create_metric_alerts() {
    echo "================================================"
    echo "🚨 Creating Metric Alerts..."
    echo "================================================"
    
    # Alert 1: High Error Rate
    echo "Creating alert: High Error Rate..."
    az monitor metrics alert create \
        --name "HighErrorRate" \
        --resource-group "$RESOURCE_GROUP" \
        --scopes "$BACKEND_APP_ID" \
        --condition "avg Percentage HTTP Server Error > 5" \
        --window-size 5m \
        --evaluation-frequency 1m \
        --severity 1 \
        --description "More than 5% of requests are failing" \
        --action CodingEngineAlerts \
        --auto-mitigate true
    
    # Alert 2: Session Pool Near Capacity
    echo "Creating alert: Session Pool Near Capacity..."
    az monitor metrics alert create \
        --name "SessionPoolNearCapacity" \
        --resource-group "$RESOURCE_GROUP" \
        --scopes "$SESSION_POOL_ID" \
        --condition "avg ActiveSessions > 45" \
        --window-size 5m \
        --evaluation-frequency 1m \
        --severity 2 \
        --description "Session pool is at 90% capacity (45/50 sessions)" \
        --action CodingEngineAlerts \
        --auto-mitigate true
    
    # Alert 3: Long Queue
    echo "Creating alert: Long Queue..."
    az monitor metrics alert create \
        --name "LongQueue" \
        --resource-group "$RESOURCE_GROUP" \
        --scopes "$SESSION_POOL_ID" \
        --condition "avg QueueLength > 10" \
        --window-size 2m \
        --evaluation-frequency 1m \
        --severity 1 \
        --description "More than 10 users waiting for sessions" \
        --action CodingEngineAlerts \
        --auto-mitigate true
    
    # Alert 4: Unusual Traffic Spike
    echo "Creating alert: Unusual Traffic Spike..."
    az monitor metrics alert create \
        --name "UnusualTrafficSpike" \
        --resource-group "$RESOURCE_GROUP" \
        --scopes "$BACKEND_APP_ID" \
        --condition "avg Requests > 1000" \
        --window-size 5m \
        --evaluation-frequency 1m \
        --severity 2 \
        --description "Receiving more than 1000 requests/min" \
        --action CodingEngineAlerts \
        --auto-mitigate true
    
    # Alert 5: Slow Response Time
    echo "Creating alert: Slow Response Time..."
    az monitor metrics alert create \
        --name "SlowResponseTime" \
        --resource-group "$RESOURCE_GROUP" \
        --scopes "$BACKEND_APP_ID" \
        --condition "avg Request Duration > 10000" \
        --window-size 5m \
        --evaluation-frequency 1m \
        --severity 2 \
        --description "Average response time > 10 seconds" \
        --action CodingEngineAlerts \
        --auto-mitigate true
    
    # Alert 6: Container Restarts
    echo "Creating alert: Container Restarts..."
    az monitor metrics alert create \
        --name "ContainerRestarting" \
        --resource-group "$RESOURCE_GROUP" \
        --scopes "$BACKEND_APP_ID" \
        --condition "total Restarts > 0" \
        --window-size 5m \
        --evaluation-frequency 1m \
        --severity 1 \
        --description "Backend container is restarting (possible crash)" \
        --action CodingEngineAlerts \
        --auto-mitigate true
    
    echo "✅ All metric alerts created"
}

# ============================================================================
# STEP 4: VERIFY SETUP
# ============================================================================

verify_setup() {
    echo "================================================"
    echo "✅ Verifying Setup..."
    echo "================================================"
    
    echo ""
    echo "Action Groups:"
    az monitor action-group list \
        --resource-group "$RESOURCE_GROUP" \
        --query "[].{Name:name, Email:emailReceivers[0].emailAddress}" \
        --output table
    
    echo ""
    echo "Metric Alerts:"
    az monitor metrics alert list \
        --resource-group "$RESOURCE_GROUP" \
        --query "[].{Name:name, Severity:severity, Enabled:enabled}" \
        --output table
    
    echo ""
    echo "Budgets:"
    az consumption budget list \
        --resource-group "$RESOURCE_GROUP" \
        --query "[].{Name:name, Amount:amount, TimeGrain:timeGrain}" \
        --output table
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    echo "================================================"
    echo "🚀 Azure Monitoring Setup"
    echo "================================================"
    echo ""
    echo "This script will set up:"
    echo "  - Email notifications to: $ADMIN_EMAIL"
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        echo "  - Slack notifications"
    fi
    echo "  - 6 metric alerts"
    echo "  - 1 budget alert"
    echo ""
    
    check_login
    
    # Create monitoring components
    create_action_group
    create_budget_alert
    create_metric_alerts
    
    # Verify
    verify_setup
    
    echo ""
    echo "================================================"
    echo "🎉 Monitoring Setup Complete!"
    echo "================================================"
    echo ""
    echo "You will receive alerts via:"
    echo "  ✅ Email: $ADMIN_EMAIL"
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        echo "  ✅ Slack: Configured"
    else
        echo "  ⚠️  Slack: Not configured (add webhook URL and re-run)"
    fi
    echo ""
    echo "Next steps:"
    echo "  1. Check your email for a verification message"
    echo "  2. Test alerts by triggering a condition"
    echo "  3. View alerts in Azure Portal → Monitor → Alerts"
    echo ""
}

# Run main function
main
