#!/bin/bash
# Resource State Management for Azure Coding Engine
# This file maintains the state of all deployed resources and provides easy start/stop commands

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

SUBSCRIPTION_ID="dab771f2-8670-4bf4-8067-ea813decb669"
RESOURCE_GROUP="ai-ta-2"
LOCATION="eastus2"

# Resource Names
ACR_NAME="aitaraacr1763805702"
ENV_NAME="ai-ta-RA-env"
SESSION_POOL_NAME="ai-ta-RA-session-pool"
BACKEND_APP_NAME="ai-ta-ra-coding-engine"
IDENTITY_NAME="ai-ta-RA-identity"

# ACR Details
ACR_LOGIN_SERVER="aitaraacr1763805702.azurecr.io"

# ============================================================================
# CURRENT STATE (as of Nov 24, 2025)
# ============================================================================

# ✅ Container Registry (ACR): RUNNING (always keep running - minimal cost)
# ✅ Container Apps Environment: RUNNING (always keep running - no cost)
# ✅ Managed Identity: EXISTS (no cost)
# ❌ Session Pool: DELETED (to save costs)
# ⏸️  Backend Container App: SCALED TO ZERO (to save costs)

# ============================================================================
# COST SUMMARY
# ============================================================================

# When STOPPED (current state):
#   - ACR: $0.17/day
#   - Environment: $0.10/day
#   - Total: ~$0.27/day ($8/month)

# When RUNNING (all resources active):
#   - ACR: $0.17/day
#   - Environment: $0.10/day
#   - Backend App (1 replica): $1.30/day
#   - Session Pool (ready-sessions: 0): $0/day (idle)
#   - Total: ~$1.57/day ($47/month)

# During Contest (2 hours, 200 users):
#   - Session Pool (ready-sessions: 5, max: 50): ~$10-15
#   - Backend App (10 replicas): ~$1
#   - Total: ~$11-16 per contest

# ============================================================================
# HELPER FUNCTIONS
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

get_acr_credentials() {
    ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query username -o tsv)
    ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query passwords[0].value -o tsv)
}

# ============================================================================
# RESOURCE STATUS COMMANDS
# ============================================================================

status() {
    echo "================================================"
    echo "📊 RESOURCE STATUS"
    echo "================================================"
    
    check_login
    
    echo ""
    echo "🗂️  Container Registry:"
    az acr show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" \
        --query '{name:name, loginServer:loginServer, sku:sku.name, status:provisioningState}' \
        --output table 2>/dev/null || echo "  ❌ Not found"
    
    echo ""
    echo "🌍 Container Apps Environment:"
    az containerapp env show --name "$ENV_NAME" --resource-group "$RESOURCE_GROUP" \
        --query '{name:name, location:location, status:properties.provisioningState}' \
        --output table 2>/dev/null || echo "  ❌ Not found"
    
    echo ""
    echo "🏊 Session Pool:"
    az containerapp sessionpool show --name "$SESSION_POOL_NAME" --resource-group "$RESOURCE_GROUP" \
        --query '{name:name, state:properties.provisioningState, maxSessions:properties.scaleConfiguration.maxConcurrentSessions, readySessions:properties.scaleConfiguration.readySessionInstances}' \
        --output table 2>/dev/null || echo "  ❌ Not found (DELETED to save costs)"
    
    echo ""
    echo "🔧 Backend Container App:"
    az containerapp show --name "$BACKEND_APP_NAME" --resource-group "$RESOURCE_GROUP" \
        --query '{name:name, url:properties.configuration.ingress.fqdn, minReplicas:properties.template.scale.minReplicas, maxReplicas:properties.template.scale.maxReplicas, runningReplicas:properties.runningStatus}' \
        --output table 2>/dev/null || echo "  ❌ Not found"
    
    echo ""
    echo "🆔 Managed Identity:"
    az identity show --name "$IDENTITY_NAME" --resource-group "$RESOURCE_GROUP" \
        --query '{name:name, clientId:clientId, principalId:principalId}' \
        --output table 2>/dev/null || echo "  ❌ Not found"
    
    echo ""
    echo "================================================"
}

# ============================================================================
# START COMMANDS (For Development/Testing)
# ============================================================================

start_backend() {
    echo "🚀 Starting Backend Container App..."
    check_login
    
    az containerapp update \
        --name "$BACKEND_APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --min-replicas 1 \
        --max-replicas 3
    
    echo "✅ Backend started (1-3 replicas)"
    echo "🌐 URL: https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io"
}

start_session_pool() {
    echo "🏊 Creating Session Pool (Cost-Optimized)..."
    check_login
    get_acr_credentials
    
    az containerapp sessionpool create \
        --name "$SESSION_POOL_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --environment "$ENV_NAME" \
        --container-type CustomContainer \
        --image "$ACR_LOGIN_SERVER/session-image:v1" \
        --target-port 2000 \
        --max-sessions 10 \
        --ready-sessions 0 \
        --cooldown-period 300 \
        --registry-server "$ACR_LOGIN_SERVER" \
        --registry-username "$ACR_USERNAME" \
        --registry-password "$ACR_PASSWORD" \
        --cpu 0.5 --memory 1.0Gi
    
    echo "✅ Session Pool created (ready-sessions: 0 = $0 when idle)"
}

start_all() {
    echo "🚀 Starting all resources..."
    start_session_pool
    start_backend
    echo ""
    echo "✅ All resources started!"
    echo "💰 Cost: ~$1.57/day when idle"
}

# ============================================================================
# STOP COMMANDS (To Save Costs)
# ============================================================================

stop_backend() {
    echo "⏸️  Stopping Backend Container App..."
    check_login
    
    az containerapp update \
        --name "$BACKEND_APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --min-replicas 0 \
        --max-replicas 0
    
    echo "✅ Backend stopped (scaled to 0)"
}

stop_session_pool() {
    echo "🗑️  Deleting Session Pool..."
    check_login
    
    az containerapp sessionpool delete \
        --name "$SESSION_POOL_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --yes
    
    echo "✅ Session Pool deleted"
}

stop_all() {
    echo "⏸️  Stopping all resources..."
    stop_backend
    stop_session_pool
    echo ""
    echo "✅ All resources stopped!"
    echo "💰 Cost: ~$0.27/day (only ACR + Environment)"
}

# ============================================================================
# CONTEST MODE (Scale up for high traffic)
# ============================================================================

contest_start() {
    echo "🏆 Starting CONTEST MODE..."
    echo "This will scale up for 200 concurrent users"
    check_login
    get_acr_credentials
    
    # Create session pool with higher capacity
    echo "🏊 Creating Session Pool (Contest Mode)..."
    az containerapp sessionpool create \
        --name "$SESSION_POOL_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --environment "$ENV_NAME" \
        --container-type CustomContainer \
        --image "$ACR_LOGIN_SERVER/session-image:v1" \
        --target-port 2000 \
        --max-sessions 50 \
        --ready-sessions 5 \
        --cooldown-period 300 \
        --registry-server "$ACR_LOGIN_SERVER" \
        --registry-username "$ACR_USERNAME" \
        --registry-password "$ACR_PASSWORD" \
        --cpu 0.5 --memory 1.0Gi
    
    # Scale up backend
    echo "🚀 Scaling up Backend..."
    az containerapp update \
        --name "$BACKEND_APP_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --min-replicas 2 \
        --max-replicas 10
    
    echo ""
    echo "✅ CONTEST MODE ACTIVE!"
    echo "📊 Capacity: 50 concurrent sessions, 1000 exec/min"
    echo "💰 Cost: ~$10-15 for 2-hour contest"
    echo "🌐 URL: https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io"
}

contest_stop() {
    echo "🏁 Stopping CONTEST MODE..."
    stop_all
    echo "✅ Contest mode stopped. Resources scaled down."
}

# ============================================================================
# TESTING COMMANDS
# ============================================================================

test_backend() {
    echo "🧪 Testing Backend Health..."
    curl -s https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/ | jq '.'
}

test_execution() {
    echo "🧪 Testing Code Execution..."
    curl -X POST https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute \
        -H "Content-Type: application/json" \
        -d '{
            "language": "python",
            "version": "3.10.0",
            "files": [
                {
                    "name": "main.py",
                    "content": "print(\"Hello from Azure!\")\nprint(\"2 + 2 =\", 2 + 2)"
                }
            ]
        }' | jq '.'
}

# ============================================================================
# COST MONITORING
# ============================================================================

cost_report() {
    echo "💰 Cost Report (Last 7 days)..."
    check_login
    
    az consumption usage list \
        --start-date $(date -v-7d +%Y-%m-%d) \
        --end-date $(date +%Y-%m-%d) \
        --query "[?contains(instanceName, 'ai-ta-ra') || contains(instanceName, 'aitaraacr')].{Resource:instanceName, Cost:pretaxCost, Currency:currency}" \
        --output table
}

# ============================================================================
# MAIN MENU
# ============================================================================

show_help() {
    cat << EOF
================================================
🎮 Azure Coding Engine - Resource Manager
================================================

USAGE: ./manage_resources.sh [command]

📊 STATUS COMMANDS:
  status              Show current state of all resources
  cost                Show cost report (last 7 days)

🚀 START COMMANDS:
  start-backend       Start backend only (for testing)
  start-session-pool  Create session pool (cost-optimized)
  start-all           Start all resources

⏸️  STOP COMMANDS:
  stop-backend        Stop backend (scale to 0)
  stop-session-pool   Delete session pool
  stop-all            Stop all resources (minimize costs)

🏆 CONTEST MODE:
  contest-start       Scale up for 200 users (50 sessions, 10 replicas)
  contest-stop        Scale down after contest

🧪 TESTING:
  test-backend        Test backend health endpoint
  test-execution      Test code execution (requires session pool)

💡 EXAMPLES:
  # Check current status
  ./manage_resources.sh status

  # Start for development
  ./manage_resources.sh start-all

  # Stop to save costs
  ./manage_resources.sh stop-all

  # Run a contest
  ./manage_resources.sh contest-start
  # ... run contest ...
  ./manage_resources.sh contest-stop

================================================
💰 COST SUMMARY:
  Stopped:  ~\$0.27/day  (\$8/month)
  Running:  ~\$1.57/day  (\$47/month)
  Contest:  ~\$10-15     (2 hours, 200 users)
================================================
EOF
}

# ============================================================================
# COMMAND ROUTER
# ============================================================================

case "${1:-help}" in
    status)
        status
        ;;
    cost)
        cost_report
        ;;
    start-backend)
        start_backend
        ;;
    start-session-pool)
        start_session_pool
        ;;
    start-all)
        start_all
        ;;
    stop-backend)
        stop_backend
        ;;
    stop-session-pool)
        stop_session_pool
        ;;
    stop-all)
        stop_all
        ;;
    contest-start)
        contest_start
        ;;
    contest-stop)
        contest_stop
        ;;
    test-backend)
        test_backend
        ;;
    test-execution)
        test_execution
        ;;
    help|*)
        show_help
        ;;
esac
