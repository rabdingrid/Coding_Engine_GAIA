#!/bin/bash
# Deploy C# Support to Azure Container Apps

set -e

echo "🚀 Deploying C# Support to Azure Container Apps"
echo ""

# Configuration
ACR_NAME="aitaraacr1763805702"
IMAGE_NAME="executor-secure"
VERSION="v17-csharp"
FULL_IMAGE="${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${VERSION}"

echo "📦 Building Docker image with C# support..."
cd "$(dirname "$0")"

# Build the image
echo "🔨 Building ${FULL_IMAGE}..."
docker build -t ${IMAGE_NAME}:${VERSION} .

# Tag for ACR
echo "🏷️  Tagging image..."
docker tag ${IMAGE_NAME}:${VERSION} ${FULL_IMAGE}

# Login to ACR (if not already logged in)
echo "🔐 Logging into Azure Container Registry..."
az acr login --name ${ACR_NAME} || {
    echo "❌ Failed to login to ACR. Please run: az login"
    exit 1
}

# Push to ACR
echo "📤 Pushing image to ACR..."
docker push ${FULL_IMAGE}

echo ""
echo "✅ Image pushed successfully: ${FULL_IMAGE}"
echo ""
echo "📝 Next steps:"
echo "1. Update terraform/variables.tf:"
echo "   executor_image = \"${FULL_IMAGE}\""
echo ""
echo "2. Apply terraform:"
echo "   cd terraform"
echo "   terraform apply"
echo ""
echo "3. Verify C# support:"
echo "   curl https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/health"
echo ""

