#!/bin/bash
# Script to set up connection string and prepare for migration

FQDN=$(az postgres flexible-server show --resource-group ai-ta-2 --name ai-ta-ra-postgre --query "fullyQualifiedDomainName" -o tsv)

echo "🔐 PostgreSQL Connection Setup"
echo "================================"
echo ""
echo "Server FQDN: $FQDN"
echo "Database: railway"
echo "Admin User: postgresadmin"
echo ""
echo "Please enter the PostgreSQL password:"
read -s PASSWORD
echo ""

CONNECTION_STRING="postgresql://postgresadmin:$PASSWORD@$FQDN:5432/railway?sslmode=require"

echo "✅ Connection string created!"
echo ""
echo "To use for migration, run:"
echo "export AZURE_DB=\"$CONNECTION_STRING\""
echo "./migrate-database.sh"
echo ""
echo "Or save to .env file:"
echo "echo 'DATABASE_URL=$CONNECTION_STRING' >> .env"
