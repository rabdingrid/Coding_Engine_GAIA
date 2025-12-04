#!/bin/bash
# Alternative: Create Azure PostgreSQL using Azure CLI directly
# This is simpler and doesn't require Terraform

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Creating Azure PostgreSQL Database (Azure CLI)${NC}"
echo "=========================================="
echo ""

# Configuration
RESOURCE_GROUP="ai-ta-2"
SERVER_NAME="ai-ta-ra-postgre"
ADMIN_USER="postgresadmin"
LOCATION="eastus2"
DATABASE_NAME="railway"
SKU="Standard_B1ms"  # Burstable, 1 vCore, 2GB RAM - ~$12/month

# Check if Azure CLI is logged in
if ! az account show &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Azure. Please run: az login${NC}"
    exit 1
fi

# Check if resource group exists
if ! az group show --name "$RESOURCE_GROUP" &> /dev/null; then
    echo -e "${RED}❌ Resource group '$RESOURCE_GROUP' not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Resource group found: $RESOURCE_GROUP${NC}"

# Check if server already exists
if az postgres flexible-server show --resource-group "$RESOURCE_GROUP" --name "$SERVER_NAME" &> /dev/null; then
    echo -e "${YELLOW}⚠️  PostgreSQL server '$SERVER_NAME' already exists${NC}"
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Generate password if not provided
if [ -z "$POSTGRES_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️  Generating secure password...${NC}"
    POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    echo -e "${GREEN}✅ Password generated${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: Save this password!${NC}"
    echo -e "${YELLOW}   Password: $POSTGRES_PASSWORD${NC}"
    echo ""
    read -p "Press Enter to continue..."
fi

echo -e "${YELLOW}📦 Creating PostgreSQL Flexible Server...${NC}"
echo -e "${YELLOW}   This may take 5-10 minutes...${NC}"
echo ""

# Create PostgreSQL Flexible Server
az postgres flexible-server create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$SERVER_NAME" \
    --location "$LOCATION" \
    --admin-user "$ADMIN_USER" \
    --admin-password "$POSTGRES_PASSWORD" \
    --sku-name "$SKU" \
    --tier Burstable \
    --version 14 \
    --storage-size 32 \
    --public-access 0.0.0.0 \
    --yes

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create PostgreSQL server${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ PostgreSQL server created!${NC}"

# Create database
echo ""
echo -e "${YELLOW}📦 Creating database '$DATABASE_NAME'...${NC}"
az postgres flexible-server db create \
    --resource-group "$RESOURCE_GROUP" \
    --server-name "$SERVER_NAME" \
    --database-name "$DATABASE_NAME"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create database${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Database created!${NC}"

# Get server FQDN
FQDN=$(az postgres flexible-server show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$SERVER_NAME" \
    --query "fullyQualifiedDomainName" -o tsv)

# Display connection information
echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "=========================================="
echo -e "${GREEN}📊 Database Information${NC}"
echo "=========================================="
echo "Server Name: $SERVER_NAME"
echo "FQDN: $FQDN"
echo "Admin User: $ADMIN_USER"
echo "Database: $DATABASE_NAME"
echo "Password: $POSTGRES_PASSWORD"
echo ""
echo "Connection String:"
echo "postgresql://$ADMIN_USER:$POSTGRES_PASSWORD@$FQDN:5432/$DATABASE_NAME?sslmode=require"
echo ""
echo "=========================================="
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Run migration script: ./migrate-database.sh"
echo "2. Update connection strings in your codebase"
echo "3. Test the application"

