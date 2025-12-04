#!/bin/bash
# Database Migration Script: Railway PostgreSQL -> Azure PostgreSQL
# This script migrates all data from Railway to Azure PostgreSQL

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Database Migration: Railway -> Azure PostgreSQL${NC}"
echo "=========================================="
echo ""

# Source and destination connection strings
RAILWAY_DB="postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway"

# Get Azure PostgreSQL connection string
if [ -z "$AZURE_DB" ]; then
    echo -e "${YELLOW}⚠️  Azure database connection string not set${NC}"
    echo "Trying to get from Terraform output..."
    if [ -d "terraform" ]; then
        cd terraform
        AZURE_DB=$(terraform output -raw postgresql_connection_string 2>/dev/null || echo "")
        cd ..
    fi
    
    # If Terraform output failed, try Azure CLI
    if [ -z "$AZURE_DB" ]; then
        echo "Trying to get from Azure CLI..."
        FQDN=$(az postgres flexible-server show --resource-group ai-ta-2 --name ai-ta-ra-postgre --query "fullyQualifiedDomainName" -o tsv 2>/dev/null || echo "")
        if [ -n "$FQDN" ]; then
            echo -e "${YELLOW}⚠️  Please provide PostgreSQL password:${NC}"
            read -s POSTGRES_PASSWORD
            echo ""
            AZURE_DB="postgresql://postgresadmin:$POSTGRES_PASSWORD@$FQDN:5432/railway?sslmode=require"
        fi
    fi
    
    if [ -z "$AZURE_DB" ]; then
        echo -e "${RED}❌ Could not get Azure database connection string${NC}"
        echo "Please set AZURE_DB environment variable or run:"
        echo "  ./create-postgresql.sh (Terraform)"
        echo "  ./create-postgresql-azcli.sh (Azure CLI)"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Source: Railway PostgreSQL${NC}"
echo -e "${GREEN}✅ Destination: Azure PostgreSQL${NC}"
echo ""

# Check if pg_dump and psql are available
if ! command -v pg_dump &> /dev/null; then
    echo -e "${RED}❌ pg_dump not found. Please install PostgreSQL client tools.${NC}"
    echo "   macOS: brew install postgresql"
    echo "   Ubuntu: sudo apt-get install postgresql-client"
    exit 1
fi

if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ psql not found. Please install PostgreSQL client tools.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Step 1: Dumping database schema and data...${NC}"
DUMP_FILE="/tmp/railway_db_dump.sql"
pg_dump "$RAILWAY_DB" --no-owner --no-acl --clean --if-exists > "$DUMP_FILE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to dump Railway database${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Database dump created: $DUMP_FILE${NC}"
echo ""

echo -e "${YELLOW}📤 Step 2: Restoring to Azure PostgreSQL...${NC}"
psql "$AZURE_DB" < "$DUMP_FILE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to restore to Azure database${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Migration completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📊 Verifying migration...${NC}"

# Verify by counting tables
TABLE_COUNT=$(psql "$AZURE_DB" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')

echo -e "${GREEN}✅ Found $TABLE_COUNT tables in Azure database${NC}"

# List tables
echo ""
echo -e "${YELLOW}📋 Tables in Azure database:${NC}"
psql "$AZURE_DB" -c "\dt"

echo ""
echo -e "${GREEN}🎉 Migration complete!${NC}"
echo ""
echo -e "${YELLOW}⚠️  Next steps:${NC}"
echo "1. Update connection strings in your codebase"
echo "2. Test the application with Azure database"
echo "3. Once verified, you can decommission Railway database"

