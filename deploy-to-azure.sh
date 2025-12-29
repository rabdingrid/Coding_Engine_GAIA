#!/bin/bash

# Deployment script for C++ batch optimization
# Builds Docker image and deploys to Azure Container Apps

set -e  # Exit on error

echo "=========================================="
echo "🚀 Deploying C++ Batch Optimization"
echo "=========================================="
echo ""

# Configuration
ACR_NAME="aitaraacr1763805702"
IMAGE_NAME="executor-fastapi"
IMAGE_TAG="optimized-cpp-batch-v1"
FULL_IMAGE="${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"
CONTAINER_APP_NAME="ai-ta-ra-code-executor2"
RESOURCE_GROUP="ai-ta-2"

echo "📋 Configuration:"
echo "   ACR: $ACR_NAME"
echo "   Image: $FULL_IMAGE"
echo "   Container App: $CONTAINER_APP_NAME"
echo "   Resource Group: $RESOURCE_GROUP"
echo ""

# Step 1: Login to ACR
echo "🔐 Step 1: Logging into Azure Container Registry..."
az acr login --name $ACR_NAME || {
    echo "❌ Failed to login to ACR. Please ensure:"
    echo "   1. Azure CLI is installed"
    echo "   2. You're logged in: az login"
    echo "   3. You have permissions to ACR"
    exit 1
}
echo "✅ Logged into ACR"
echo ""

# Step 2: Build Docker image
echo "🔨 Step 2: Building Docker image..."
docker build -f Dockerfile.fastapi -t $FULL_IMAGE . || {
    echo "❌ Docker build failed"
    exit 1
}
echo "✅ Docker image built: $FULL_IMAGE"
echo ""

# Step 3: Push to ACR
echo "📤 Step 3: Pushing image to ACR..."
docker push $FULL_IMAGE || {
    echo "❌ Failed to push image to ACR"
    exit 1
}
echo "✅ Image pushed to ACR"
echo ""

# Step 4: Update Container App
echo "☁️  Step 4: Updating Azure Container App..."
az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $FULL_IMAGE || {
    echo "❌ Failed to update container app"
    echo ""
    echo "💡 Manual update command:"
    echo "   az containerapp update \\"
    echo "     --name $CONTAINER_APP_NAME \\"
    echo "     --resource-group $RESOURCE_GROUP \\"
    echo "     --image $FULL_IMAGE"
    exit 1
}
echo "✅ Container app updated"
echo ""

# Step 5: Wait for deployment
echo "⏳ Step 5: Waiting for deployment to complete..."
sleep 10

# Step 6: Verify deployment
echo "✅ Step 6: Verifying deployment..."
SERVICE_URL=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "properties.configuration.ingress.fqdn" -o tsv)

if [ -z "$SERVICE_URL" ]; then
    echo "⚠️  Could not get service URL"
else
    echo "   Service URL: https://$SERVICE_URL"
    echo ""
    echo "🧪 Testing health endpoint..."
    HEALTH_RESPONSE=$(curl -s "https://$SERVICE_URL/health" || echo "failed")
    if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
        echo "✅ Service is healthy!"
    else
        echo "⚠️  Health check response: $HEALTH_RESPONSE"
    fi
fi

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "📊 Next Steps:"
echo "   1. Test the optimized endpoint:"
echo "      curl -X POST https://$SERVICE_URL/runall ..."
echo ""
echo "   2. Monitor logs:"
echo "      az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow"
echo ""
echo "   3. If issues occur, see REVERT_PLAN.md"
echo ""
echo "🎯 Expected Performance:"
echo "   Before: 24s for 17 C++ test cases"
echo "   After:  ~5s for 17 C++ test cases"
echo ""


