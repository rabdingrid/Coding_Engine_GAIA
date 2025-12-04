#!/bin/bash
# Script to create Azure PostgreSQL database
# This will create a cost-optimized PostgreSQL Flexible Server in Azure

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Creating Azure PostgreSQL Database${NC}"
echo "=========================================="
echo ""

# Check if Azure CLI is logged in
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Azure. Please run: az login${NC}"
    exit 1
fi

# Check if resource group exists
RESOURCE_GROUP="ai-ta-2"
if ! az group show --name "$RESOURCE_GROUP" &> /dev/null; then
    echo -e "${RED}❌ Resource group '$RESOURCE_GROUP' not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Resource group found: $RESOURCE_GROUP${NC}"

# Generate a secure password if not provided
if [ -z "$POSTGRES_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️  Generating secure password...${NC}"
    POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    echo -e "${GREEN}✅ Password generated (saved for later use)${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: Save this password!${NC}"
    echo -e "${YELLOW}   Password: $POSTGRES_PASSWORD${NC}"
    echo ""
    read -p "Press Enter to continue..."
fi

# Set Terraform variable
export TF_VAR_postgres_password="$POSTGRES_PASSWORD"

# Navigate to terraform directory
cd terraform

echo -e "${YELLOW}📦 Step 1: Initializing Terraform...${NC}"
terraform init

echo ""
echo -e "${YELLOW}📋 Step 2: Planning PostgreSQL deployment...${NC}"
terraform plan -out=tfplan

echo ""
echo -e "${YELLOW}🚀 Step 3: Creating PostgreSQL database...${NC}"
echo -e "${YELLOW}   This may take 5-10 minutes...${NC}"
terraform apply tfplan

echo ""
echo -e "${GREEN}✅ PostgreSQL database created!${NC}"
echo ""

# Get connection string
echo -e "${YELLOW}📊 Database Information:${NC}"
echo "=========================================="
terraform output -json | jq -r '
  "Server Name: " + .postgresql_server_name.value,
  "FQDN: " + .postgresql_fqdn.value,
  "Admin Login: " + .postgresql_admin_login.value,
  "",
  "Connection String:",
  .postgresql_connection_string.value
'

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Run migration script: ./migrate-database.sh"
echo "2. Update connection strings in your codebase"
echo "3. Test the application"

