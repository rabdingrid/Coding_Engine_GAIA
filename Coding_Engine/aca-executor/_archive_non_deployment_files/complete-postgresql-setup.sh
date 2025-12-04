#!/bin/bash
# Complete PostgreSQL setup: Wait for server, create database, migrate data

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

RESOURCE_GROUP="ai-ta-2"
SERVER_NAME="ai-ta-ra-postgre"
DATABASE_NAME="railway"
ADMIN_USER="postgresadmin"

echo -e "${GREEN}🚀 Completing PostgreSQL Setup${NC}"
echo "=========================================="
echo ""

# Step 1: Wait for server to be ready
echo -e "${YELLOW}⏳ Step 1: Waiting for server to be ready...${NC}"
MAX_WAIT=600  # 10 minutes
ELAPSED=0
CHECK_INTERVAL=30

while [ $ELAPSED -lt $MAX_WAIT ]; do
    STATE=$(az postgres flexible-server show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$SERVER_NAME" \
        --query "state" -o tsv 2>/dev/null || echo "Unknown")
    
    if [ "$STATE" = "Ready" ]; then
        echo -e "${GREEN}✅ Server is ready!${NC}"
        break
    elif [ "$STATE" = "Provisioning" ]; then
        echo -e "${YELLOW}   Still provisioning... (${ELAPSED}s elapsed)${NC}"
    else
        echo -e "${YELLOW}   Status: $STATE (${ELAPSED}s elapsed)${NC}"
    fi
    
    if [ $ELAPSED -ge $MAX_WAIT ]; then
        echo -e "${RED}❌ Timeout waiting for server${NC}"
        exit 1
    fi
    
    sleep $CHECK_INTERVAL
    ELAPSED=$((ELAPSED + CHECK_INTERVAL))
done

# Get server FQDN
FQDN=$(az postgres flexible-server show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$SERVER_NAME" \
    --query "fullyQualifiedDomainName" -o tsv)

echo -e "${GREEN}✅ Server FQDN: $FQDN${NC}"
echo ""

# Step 2: Get or prompt for password
if [ -z "$POSTGRES_PASSWORD" ]; then
    echo -e "${YELLOW}⚠️  PostgreSQL password needed${NC}"
    echo "Please enter the password you set when creating the server:"
    read -s POSTGRES_PASSWORD
    echo ""
fi

# Step 3: Create database
echo -e "${YELLOW}📦 Step 2: Creating database '$DATABASE_NAME'...${NC}"
az postgres flexible-server db create \
    --resource-group "$RESOURCE_GROUP" \
    --server-name "$SERVER_NAME" \
    --database-name "$DATABASE_NAME" \
    --yes

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database created!${NC}"
else
    echo -e "${YELLOW}⚠️  Database might already exist, continuing...${NC}"
fi

echo ""

# Step 4: Set up firewall rule for Azure services (if not exists)
echo -e "${YELLOW}🔒 Step 3: Setting up firewall rules...${NC}"
az postgres flexible-server firewall-rule create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$SERVER_NAME" \
    --rule-name "AllowAzureServices" \
    --start-ip-address "0.0.0.0" \
    --end-ip-address "0.0.0.0" \
    --yes 2>/dev/null || echo -e "${YELLOW}   Firewall rule might already exist${NC}"

echo -e "${GREEN}✅ Firewall configured${NC}"
echo ""

# Step 5: Display connection information
CONNECTION_STRING="postgresql://$ADMIN_USER:$POSTGRES_PASSWORD@$FQDN:5432/$DATABASE_NAME?sslmode=require"

echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo "=========================================="
echo -e "${GREEN}📊 Database Information${NC}"
echo "=========================================="
echo "Server Name: $SERVER_NAME"
echo "FQDN: $FQDN"
echo "Admin User: $ADMIN_USER"
echo "Database: $DATABASE_NAME"
echo ""
echo "Connection String:"
echo "$CONNECTION_STRING"
echo ""
echo "=========================================="
echo ""

# Step 6: Check if migration tools are available
if command -v pg_dump &> /dev/null && command -v psql &> /dev/null; then
    echo -e "${YELLOW}📦 Step 4: Ready to migrate data...${NC}"
    echo "Run: ./migrate-database.sh"
    echo ""
    echo "Or set environment variable and run:"
    echo "export AZURE_DB=\"$CONNECTION_STRING\""
    echo "./migrate-database.sh"
else
    echo -e "${YELLOW}⚠️  PostgreSQL client tools not found${NC}"
    echo "Install them to migrate data:"
    echo "  macOS: brew install postgresql"
    echo "  Ubuntu: sudo apt-get install postgresql-client"
    echo ""
    echo "Then run: ./migrate-database.sh"
fi

echo ""
echo -e "${GREEN}✅ PostgreSQL setup complete!${NC}"

