# PostgreSQL Migration Guide: Railway → Azure

## 🎯 Overview

This guide will help you migrate your PostgreSQL database from Railway to Azure PostgreSQL Flexible Server.

## 📋 Prerequisites

1. **Azure CLI** installed and logged in
   ```bash
   az login
   ```

2. **PostgreSQL client tools** installed
   - macOS: `brew install postgresql`
   - Ubuntu: `sudo apt-get install postgresql-client`

3. **Terraform** installed (for infrastructure)

4. **Resource Group**: `ai-ta-2` must exist in Azure

## 🚀 Step 1: Create Azure PostgreSQL Database

### Option A: Using the Automated Script (Recommended)

```bash
cd Coding_Engine/aca-executor
./create-postgresql.sh
```

This script will:
- Generate a secure password
- Create PostgreSQL Flexible Server using Terraform
- Display connection information

### Option B: Manual Terraform Deployment

```bash
cd Coding_Engine/aca-executor/terraform

# Generate a secure password
export TF_VAR_postgres_password=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

# Initialize and apply
terraform init
terraform plan
terraform apply
```

**Note**: Save the password! You'll need it for migration and connection strings.

## 📊 Database Configuration

The Terraform configuration creates:
- **Server Name**: `ai-ta-ra-postgre`
- **SKU**: `B_Standard_B1ms` (Burstable, 1 vCore, 2GB RAM)
- **Cost**: ~$12/month (much cheaper than Railway)
- **Storage**: 32GB
- **Backup**: 7 days retention
- **Location**: Same as resource group (`eastus2`)

## 🔄 Step 2: Migrate Data

### Using the Migration Script

```bash
cd Coding_Engine/aca-executor
./migrate-database.sh
```

This script will:
1. Dump all data from Railway PostgreSQL
2. Restore to Azure PostgreSQL
3. Verify the migration

### Manual Migration

```bash
# 1. Dump Railway database
pg_dump "postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway" \
  --no-owner --no-acl --clean --if-exists > railway_dump.sql

# 2. Get Azure connection string
cd terraform
AZURE_DB=$(terraform output -raw postgresql_connection_string)
cd ..

# 3. Restore to Azure
psql "$AZURE_DB" < railway_dump.sql
```

## 🔧 Step 3: Update Connection Strings

After migration, update connection strings in your codebase:

### Files to Update:

1. **`test-ui/server.js`**
   ```javascript
   // OLD:
   connectionString: 'postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway',
   
   // NEW: Get from Terraform output
   connectionString: process.env.DATABASE_URL || 'postgresql://postgresadmin:PASSWORD@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway',
   ```

2. **`dsa-questions/IMPORT_TO_DB.js`**
   ```javascript
   // Update connection string
   connectionString: process.env.DATABASE_URL || 'postgresql://postgresadmin:PASSWORD@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway',
   ```

3. **`test-ui/add-dsa-questions.js`**
   ```javascript
   // Update connection string
   connectionString: process.env.DATABASE_URL || 'postgresql://postgresadmin:PASSWORD@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway',
   ```

### Get Connection String from Terraform:

```bash
cd terraform
terraform output postgresql_connection_string
```

## ✅ Step 4: Verify Migration

### Check Tables

```bash
# Get connection string
cd terraform
AZURE_DB=$(terraform output -raw postgresql_connection_string)
cd ..

# List tables
psql "$AZURE_DB" -c "\dt"

# Count records in main tables
psql "$AZURE_DB" -c "SELECT COUNT(*) FROM coding_question_bank;"
```

### Test Application

1. Start the test UI:
   ```bash
   cd test-ui
   npm start
   ```

2. Verify questions load from Azure database

3. Test code execution and database writes

## 🔒 Security Best Practices

1. **Use Environment Variables**: Store connection strings in `.env` files
   ```bash
   export DATABASE_URL="postgresql://postgresadmin:PASSWORD@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway"
   ```

2. **Firewall Rules**: Azure PostgreSQL allows Azure services by default. For external access, add your IP:
   ```bash
   az postgres flexible-server firewall-rule create \
     --resource-group ai-ta-2 \
     --name ai-ta-ra-postgre \
     --rule-name AllowMyIP \
     --start-ip-address YOUR_IP \
     --end-ip-address YOUR_IP
   ```

3. **SSL Connection**: Azure PostgreSQL requires SSL. Update connection strings:
   ```
   postgresql://user:pass@host:5432/db?sslmode=require
   ```

## 💰 Cost Comparison

| Service | Cost/Month | Notes |
|---------|------------|-------|
| **Railway PostgreSQL** | ~$20-30 | Pay-as-you-go |
| **Azure PostgreSQL (B1ms)** | ~$12 | Burstable, cost-optimized |
| **Azure PostgreSQL (B2s)** | ~$24 | Better performance |

## 🐛 Troubleshooting

### Connection Issues

1. **Firewall**: Ensure your IP is allowed
   ```bash
   az postgres flexible-server firewall-rule list \
     --resource-group ai-ta-2 \
     --name ai-ta-ra-postgre
   ```

2. **SSL Required**: Add `?sslmode=require` to connection string

3. **Password**: Verify password is correct
   ```bash
   # Reset password if needed
   az postgres flexible-server update \
     --resource-group ai-ta-2 \
     --name ai-ta-ra-postgre \
     --admin-password NEW_PASSWORD
   ```

### Migration Issues

1. **Large Database**: For large databases, use `pg_dump` with compression:
   ```bash
   pg_dump "$RAILWAY_DB" | gzip > railway_dump.sql.gz
   gunzip -c railway_dump.sql.gz | psql "$AZURE_DB"
   ```

2. **Timeout**: Increase connection timeout:
   ```bash
   export PGCONNECT_TIMEOUT=60
   ```

## 📝 Summary

1. ✅ Create Azure PostgreSQL using Terraform
2. ✅ Migrate data from Railway
3. ✅ Update connection strings
4. ✅ Test application
5. ✅ Decommission Railway database (after verification)

## 🎉 Benefits of Migration

- ✅ **Cost Savings**: ~50% cheaper than Railway
- ✅ **Same Region**: Database in same Azure region as ACA
- ✅ **Better Integration**: All resources in one resource group
- ✅ **More Control**: Full control over database configuration
- ✅ **Better Monitoring**: Azure Monitor integration

