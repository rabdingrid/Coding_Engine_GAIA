#!/bin/bash

# Deployment script for Refactored Code Execution Service
# Builds Docker image and deploys to NEW Azure Container App for testing

set -e  # Exit on error

echo "=========================================="
echo "🚀 Deploying Refactored Code Executor"
echo "=========================================="
echo ""

# Configuration
ACR_NAME="ait2codingengineacr"
IMAGE_NAME="executor-service-refactored"
IMAGE_TAG="v4.0.0-refactored"
FULL_IMAGE="${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"
CONTAINER_APP_NAME="ai-ta-ra-code-executor2.1-testing"
RESOURCE_GROUP="ai-ta-2"
CONTAINER_APP_ENV="ai-ta-RA-env-testing"

echo "📋 Configuration:"
echo "   ACR: $ACR_NAME"
echo "   Image: $FULL_IMAGE"
echo "   Container App: $CONTAINER_APP_NAME"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Environment: $CONTAINER_APP_ENV"
echo ""

# Step 1: Login to Azure
echo "🔐 Step 1: Checking Azure login..."
az account show > /dev/null 2>&1 || {
    echo "❌ Not logged into Azure. Please run: az login"
    exit 1
}
echo "✅ Logged into Azure"
echo ""

# Step 2: Login to ACR
echo "🔐 Step 2: Logging into Azure Container Registry..."
az acr login --name $ACR_NAME || {
    echo "❌ Failed to login to ACR. Please ensure:"
    echo "   1. ACR name is correct: $ACR_NAME"
    echo "   2. You have permissions to ACR"
    echo "   3. ACR exists in your subscription"
    exit 1
}
echo "✅ Logged into ACR"
echo ""

# Step 3: Build Docker image
echo "🔨 Step 3: Building Docker image..."
echo "   Using: Dockerfile.fastapi"
echo "   Platform: linux/amd64 (for Azure)"
docker build --platform linux/amd64 -f Dockerfile.fastapi -t $FULL_IMAGE . || {
    echo "❌ Docker build failed"
    exit 1
}
echo "✅ Docker image built: $FULL_IMAGE"
echo ""

# Step 4: Push to ACR
echo "📤 Step 4: Pushing image to ACR..."
docker push $FULL_IMAGE || {
    echo "❌ Failed to push image to ACR"
    exit 1
}
echo "✅ Image pushed to ACR"
echo ""

# Step 5: Check if Container App exists
echo "🔍 Step 5: Checking if Container App exists..."
APP_EXISTS=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "name" -o tsv 2>/dev/null || echo "")

if [ -z "$APP_EXISTS" ]; then
    echo "📦 Container App doesn't exist. Creating new Container App..."
    
    # Step 5a: Check if Container App Environment exists, create if not
    echo "🔍 Checking Container App Environment..."
    ENV_EXISTS=$(az containerapp env show \
      --name $CONTAINER_APP_ENV \
      --resource-group $RESOURCE_GROUP \
      --query "name" -o tsv 2>/dev/null || echo "")
    
    if [ -z "$ENV_EXISTS" ]; then
        echo "🌍 Creating new Container App Environment: $CONTAINER_APP_ENV"
        az containerapp env create \
          --name $CONTAINER_APP_ENV \
          --resource-group $RESOURCE_GROUP \
          --location eastus2 || {
            echo "❌ Failed to create Container App Environment"
            exit 1
        }
        echo "✅ Container App Environment created"
        sleep 5
    else
        echo "✅ Container App Environment exists: $CONTAINER_APP_ENV"
    fi
    echo ""
    
    # Get ACR credentials
    ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
    ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)
    
    # Create Container App
    az containerapp create \
      --name $CONTAINER_APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --environment $CONTAINER_APP_ENV \
      --image $FULL_IMAGE \
      --target-port 8000 \
      --ingress external \
      --min-replicas 1 \
      --max-replicas 3 \
      --cpu 2.0 \
      --memory 4.0Gi \
      --registry-server "${ACR_NAME}.azurecr.io" \
      --registry-username $ACR_USERNAME \
      --registry-password $ACR_PASSWORD \
      --env-vars "PORT=8000" || {
        echo "❌ Failed to create container app"
        exit 1
    }
    echo "✅ Container App created: $CONTAINER_APP_NAME"
else
    echo "📦 Container App exists. Updating with new image..."
    az containerapp update \
      --name $CONTAINER_APP_NAME \
      --resource-group $RESOURCE_GROUP \
      --image $FULL_IMAGE || {
        echo "❌ Failed to update container app"
        exit 1
    }
    echo "✅ Container App updated"
fi
echo ""

# Step 6: Wait for deployment
echo "⏳ Step 6: Waiting for deployment to complete..."
sleep 15

# Step 7: Get service URL
echo "🌐 Step 7: Getting service URL..."
SERVICE_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.configuration.ingress.fqdn" -o tsv)

if [ -z "$SERVICE_URL" ]; then
    echo "⚠️  Could not get service URL"
else
    echo "   Service URL: https://$SERVICE_URL"
    echo ""
    
    # Step 8: Test health endpoint
    echo "🧪 Step 8: Testing health endpoint..."
    sleep 5
    HEALTH_RESPONSE=$(curl -s "https://$SERVICE_URL/health" || echo "failed")
    if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
        echo "✅ Service is healthy!"
        echo ""
        echo "📊 Health Response:"
        echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
    else
        echo "⚠️  Health check response: $HEALTH_RESPONSE"
        echo ""
        echo "💡 Check logs with:"
        echo "   az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
    fi
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "📊 Service Details:"
echo "   URL: https://$SERVICE_URL"
echo "   Name: $CONTAINER_APP_NAME"
echo "   Image: $FULL_IMAGE"
echo ""
echo "🧪 Test Endpoints:"
echo "   1. Health: curl https://$SERVICE_URL/health"
echo "   2. Run: curl -X POST https://$SERVICE_URL/run ..."
echo "   3. RunAll: curl -X POST https://$SERVICE_URL/runall ..."
echo ""
echo "📝 Useful Commands:"
echo "   View logs: az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo "   View status: az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.runningStatus"
echo "   Delete app: az containerapp delete --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --yes"
echo ""

