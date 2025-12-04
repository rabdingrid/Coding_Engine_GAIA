#!/bin/bash
# Script to add a contributor to Azure PostgreSQL database

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}👥 Add Contributor to Azure PostgreSQL${NC}"
echo "=========================================="
echo ""

# Get contributor details
read -p "Contributor username (e.g., contributor_john): " USERNAME
read -p "Contributor password (min 8 chars): " -s PASSWORD
echo ""
read -p "Contributor IP address (e.g., 123.456.789.0): " CONTRIBUTOR_IP

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$CONTRIBUTOR_IP" ]; then
    echo -e "${RED}❌ All fields are required${NC}"
    exit 1
fi

# Get Azure connection string
AZURE_DB=$(cat .postgres-connection.txt 2>/dev/null || echo "")
if [ -z "$AZURE_DB" ]; then
    echo -e "${RED}❌ Could not find connection string${NC}"
    echo "Please set AZURE_DB environment variable"
    exit 1
fi

export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"

echo ""
echo -e "${YELLOW}📝 Step 1: Creating database user...${NC}"

# Create user SQL
CREATE_USER_SQL="
CREATE USER $USERNAME WITH PASSWORD '$PASSWORD';
GRANT CONNECT ON DATABASE railway TO $USERNAME;
GRANT USAGE ON SCHEMA public TO $USERNAME;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $USERNAME;
GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public TO $USERNAME;
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $USERNAME;
"

psql "$AZURE_DB" -c "$CREATE_USER_SQL" 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ User created successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  User might already exist, continuing...${NC}"
fi

echo ""
echo -e "${YELLOW}🔒 Step 2: Adding firewall rule...${NC}"

az postgres flexible-server firewall-rule create \
    --resource-group ai-ta-2 \
    --name ai-ta-ra-postgre \
    --rule-name "Allow$USERNAME" \
    --start-ip-address "$CONTRIBUTOR_IP" \
    --end-ip-address "$CONTRIBUTOR_IP" \
    --yes 2>&1 | head -5

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Firewall rule added!${NC}"
else
    echo -e "${YELLOW}⚠️  Firewall rule might already exist${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Contributor added successfully!${NC}"
echo ""
echo "=========================================="
echo -e "${GREEN}📋 Share these details with $USERNAME:${NC}"
echo "=========================================="
echo ""
echo "Server: ai-ta-ra-postgre.postgres.database.azure.com"
echo "Port: 5432"
echo "Database: railway"
echo "Username: $USERNAME"
echo "Password: $PASSWORD"
echo "SSL: Required"
echo ""
echo "Connection String:"
echo "postgresql://$USERNAME:$PASSWORD@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require"
echo ""
echo "=========================================="
echo ""
echo -e "${YELLOW}💡 Visualization Tools:${NC}"
echo "  - Azure Data Studio: https://aka.ms/azuredatastudio"
echo "  - pgAdmin: https://www.pgadmin.org/"
echo "  - Azure Portal Query Editor: (see SHARE_DATABASE_ACCESS.md)"
echo ""

