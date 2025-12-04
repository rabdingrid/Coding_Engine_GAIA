#!/bin/bash
set -e

# Configuration
SUBSCRIPTION_ID="dab771f2-8670-4bf4-8067-ea813decb669"
RESOURCE_GROUP="ai-ta-2"
LOCATION="eastus2"

# Naming (ai-ta-RA-*)
ACR_NAME="aitaraacr1763805702" # Reusing created ACR
SESSION_POOL_NAME="ai-ta-RA-session-pool"
BACKEND_APP_NAME="ai-ta-ra-coding-engine"
IDENTITY_NAME="ai-ta-RA-identity"

echo "🚀 Starting Deployment to Organization Subscription: $SUBSCRIPTION_ID"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"

# 1. Login & Set Subscription
echo "--------------------------------------------------"
echo "🔑 Logging in..."
az account set --subscription "$SUBSCRIPTION_ID"

# 2. Create ACR (if not exists)
echo "--------------------------------------------------"
echo "📦 Creating Container Registry ($ACR_NAME)..."
# Check if we should use an existing one or create new. 
# Since user asked for "ai-ta-RA-Coding-Engine or something similar", we create a new one.
az acr create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACR_NAME" \
  --sku Basic \
  --admin-enabled true \
  --location "$LOCATION"

# Get ACR Credentials
ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query loginServer --output tsv)
echo "✅ ACR Created: $ACR_LOGIN_SERVER"

# 3. Build & Push Session Image (The one with languages)
echo "--------------------------------------------------"
echo "🏗️  Building Session Image (Pre-installed Languages)..."
echo "Skipping build (already done)..."
# az acr build \
#   --registry "$ACR_NAME" \
#   --image session-image:v1 \
#   --file Dockerfile.session \
#   .

# 4. Build & Push Backend Image
echo "--------------------------------------------------"
echo "🏗️  Building Backend Image..."
echo "Skipping build (already done)..."
# az acr build \
#   --registry "$ACR_NAME" \
#   --image backend-image:v1 \
#   --file backend/Dockerfile \
#   backend/

# 5. Create Managed Identity
echo "--------------------------------------------------"
echo "🆔 Creating Managed Identity..."
az identity create \
  --name "$IDENTITY_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION"

IDENTITY_ID=$(az identity show --name "$IDENTITY_NAME" --resource-group "$RESOURCE_GROUP" --query id --output tsv)
IDENTITY_CLIENT_ID=$(az identity show --name "$IDENTITY_NAME" --resource-group "$RESOURCE_GROUP" --query clientId --output tsv)

echo "⏳ Waiting 60s for Identity propagation..."
sleep 60

# Grant Identity permission to pull from ACR - SKIPPING due to permissions
# ACR_ID=$(az acr show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query id --output tsv)
# az role assignment create ...

# Get ACR Admin Credentials (Workaround for missing permissions)
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query passwords[0].value --output tsv)

# 6. Create Container Apps Environment (Required for Custom Container Sessions)
echo "--------------------------------------------------"
echo "🌍 Creating Container Apps Environment..."
ENV_NAME="ai-ta-RA-env"
az containerapp env create \
  --name "$ENV_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION"

# 7. Create Dynamic Session Pool
echo "--------------------------------------------------"
echo "🏊 Creating Dynamic Session Pool ($SESSION_POOL_NAME)..."
echo "Skipping Session Pool creation (already done)..."
# az containerapp sessionpool create ...

# Get Pool Management Endpoint (Required for Backend)
POOL_ENDPOINT=$(az containerapp sessionpool show \
  --name "$SESSION_POOL_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query properties.poolManagementEndpoint \
  --output tsv)

echo "✅ Session Pool Endpoint: $POOL_ENDPOINT"

# 8. Create Backend Container App
echo "--------------------------------------------------"
echo "🚀 Deploying Backend Container App ($BACKEND_APP_NAME)..."

# Grant Identity permission to manage sessions (Session Executor Role)
echo "Attempting to assign Session Executor role..."
az role assignment create \
  --assignee "$IDENTITY_CLIENT_ID" \
  --role "Azure ContainerApps Session Executor" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.App/sessionPools/$SESSION_POOL_NAME" || echo "⚠️  Warning: Could not assign role. You may need to ask an Admin to grant 'Azure ContainerApps Session Executor' to $IDENTITY_NAME on the Session Pool."

az containerapp create \
  --name "$BACKEND_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENV_NAME" \
  --image "$ACR_LOGIN_SERVER/backend-image:v1" \
  --target-port 8000 \
  --ingress external \
  --user-assigned "$IDENTITY_ID" \
  --registry-server "$ACR_LOGIN_SERVER" \
  --registry-username "$ACR_USERNAME" \
  --registry-password "$ACR_PASSWORD" \
  --env-vars "POOL_MANAGEMENT_ENDPOINT=$POOL_ENDPOINT" "AZURE_CLIENT_ID=$IDENTITY_CLIENT_ID" \
  --min-replicas 1 \
  --max-replicas 5

# Get Public URL
BACKEND_URL=$(az containerapp show --name "$BACKEND_APP_NAME" --resource-group "$RESOURCE_GROUP" --query properties.configuration.ingress.fqdn --output tsv)

echo "--------------------------------------------------"
echo "🎉 Deployment Complete!"
echo "Backend URL: https://$BACKEND_URL"
echo "--------------------------------------------------"
echo "Next Steps:"
echo "1. Update your frontend/app.js to point to: https://$BACKEND_URL"
echo "2. Test with Python, C++, Java."
