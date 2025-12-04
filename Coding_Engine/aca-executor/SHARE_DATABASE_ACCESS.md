# Sharing Azure PostgreSQL Database Access

## 📋 Database Name Clarification

**"railway" is just a database name** - it has **NO connection** to Railway service!

- ✅ It's just the name we used (same as your Railway database name)
- ✅ Your database is 100% in Azure
- ✅ Server: `ai-ta-ra-postgre` (Azure)
- ✅ Location: `eastus2` (Azure)
- ✅ No connection to Railway service

You can rename it if you want, but it's just a name!

## 🌐 Viewing Database Tables in Azure Portal

### Method 1: Azure Portal Query Editor

1. **Go to Azure Portal**: https://portal.azure.com
2. **Search for**: `ai-ta-ra-postgre`
3. **Click** on the PostgreSQL server
4. **Click** "Query editor" in the left menu
5. **Login** with:
   - Username: `postgresadmin`
   - Password: (from `.postgres-connection.txt`)
6. **Run queries**:
   ```sql
   -- List all tables
   \dt
   
   -- Or
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public';
   
   -- View data
   SELECT * FROM coding_question_bank LIMIT 10;
   ```

### Method 2: Azure Data Studio (Recommended for Contributors)

1. **Download**: https://aka.ms/azuredatastudio
2. **Install PostgreSQL extension**
3. **Connect**:
   - Server: `ai-ta-ra-postgre.postgres.database.azure.com`
   - Database: `railway`
   - Username: `postgresadmin`
   - Password: (from `.postgres-connection.txt`)
   - SSL: Required

### Method 3: pgAdmin (Web-based)

1. **Install pgAdmin**: https://www.pgadmin.org/
2. **Add Server**:
   - Name: Azure PostgreSQL
   - Host: `ai-ta-ra-postgre.postgres.database.azure.com`
   - Port: `5432`
   - Database: `railway`
   - Username: `postgresadmin`
   - Password: (from `.postgres-connection.txt`)
   - SSL: Required

## 👥 Sharing Database Access with Contributors

### Option 1: Share Credentials (Simple but Less Secure)

**Share these details**:
```
Server: ai-ta-ra-postgre.postgres.database.azure.com
Port: 5432
Database: railway
Username: postgresadmin
Password: [from .postgres-connection.txt]
SSL: Required
```

**Connection String**:
```
postgresql://postgresadmin:PASSWORD@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require
```

**⚠️ Security Note**: Sharing admin credentials is not recommended for production!

### Option 2: Create Separate Users (Recommended)

Create individual users for each contributor:

```sql
-- Connect as admin first
-- Then create user for contributor

CREATE USER contributor1 WITH PASSWORD 'secure_password_here';
GRANT CONNECT ON DATABASE railway TO contributor1;
GRANT USAGE ON SCHEMA public TO contributor1;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO contributor1;
GRANT SELECT, USAGE ON ALL SEQUENCES IN SCHEMA public TO contributor1;

-- For new tables created in future
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO contributor1;
```

**Then share**:
```
Server: ai-ta-ra-postgre.postgres.database.azure.com
Port: 5432
Database: railway
Username: contributor1
Password: [their password]
SSL: Required
```

### Option 3: Firewall Rules for Contributors

Each contributor needs their IP added to firewall:

```bash
# Get contributor's IP (they need to provide it)
CONTRIBUTOR_IP="their.ip.address.here"

# Add firewall rule
az postgres flexible-server firewall-rule create \
  --resource-group ai-ta-2 \
  --name ai-ta-ra-postgre \
  --rule-name "AllowContributor1" \
  --start-ip-address "$CONTRIBUTOR_IP" \
  --end-ip-address "$CONTRIBUTOR_IP"
```

**Or they can add it themselves** (if they have Azure access):
1. Go to Azure Portal
2. Navigate to PostgreSQL server
3. Click "Networking" → "Firewall rules"
4. Add their IP address

## 🔐 Security Best Practices

### ✅ Recommended Approach

1. **Create separate users** for each contributor
2. **Grant only necessary permissions** (SELECT, INSERT, UPDATE, DELETE)
3. **Add firewall rules** for each contributor's IP
4. **Use strong passwords**
5. **Rotate passwords** periodically

### ❌ Avoid

- Sharing admin credentials
- Using `0.0.0.0 - 255.255.255.255` firewall rule (allows anyone)
- Weak passwords
- No SSL connections

## 📊 Visualization Tools

### 1. Azure Data Studio (Free, Recommended)
- **Download**: https://aka.ms/azuredatastudio
- **Features**: Query editor, data visualization, table browsing
- **Best for**: Contributors who want a full IDE

### 2. pgAdmin (Free)
- **Download**: https://www.pgadmin.org/
- **Features**: Web-based, full PostgreSQL management
- **Best for**: Database administrators

### 3. DBeaver (Free)
- **Download**: https://dbeaver.io/
- **Features**: Universal database tool, great visualization
- **Best for**: Data analysts

### 4. TablePlus (Paid, macOS/Windows)
- **Download**: https://tableplus.com/
- **Features**: Beautiful UI, great for visualization
- **Best for**: Designers/developers who want nice UI

### 5. Azure Portal Query Editor (Free, No Install)
- **URL**: Azure Portal → PostgreSQL server → Query editor
- **Features**: Basic query execution
- **Best for**: Quick checks

## 🔗 Quick Access Links

### Azure Portal Direct Links

**Server Overview**:
```
https://portal.azure.com/#@/resource/subscriptions/YOUR_SUB_ID/resourceGroups/ai-ta-2/providers/Microsoft.DBforPostgreSQL/flexibleServers/ai-ta-ra-postgre/overview
```

**Query Editor**:
```
https://portal.azure.com/#@/resource/subscriptions/YOUR_SUB_ID/resourceGroups/ai-ta-2/providers/Microsoft.DBforPostgreSQL/flexibleServers/ai-ta-ra-postgre/queryEditor
```

**Networking/Firewall**:
```
https://portal.azure.com/#@/resource/subscriptions/YOUR_SUB_ID/resourceGroups/ai-ta-2/providers/Microsoft.DBforPostgreSQL/flexibleServers/ai-ta-ra-postgre/networking
```

## 📝 Example: Sharing with One Contributor

### Step 1: Create User
```sql
CREATE USER contributor_john WITH PASSWORD 'JohnSecurePass123!';
GRANT CONNECT ON DATABASE railway TO contributor_john;
GRANT USAGE ON SCHEMA public TO contributor_john;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO contributor_john;
```

### Step 2: Add Firewall Rule
```bash
az postgres flexible-server firewall-rule create \
  --resource-group ai-ta-2 \
  --name ai-ta-ra-postgre \
  --rule-name "AllowJohn" \
  --start-ip-address "123.456.789.0" \
  --end-ip-address "123.456.789.0"
```

### Step 3: Share Credentials
```
Server: ai-ta-ra-postgre.postgres.database.azure.com
Port: 5432
Database: railway
Username: contributor_john
Password: JohnSecurePass123!
SSL: Required
```

## ✅ Summary

- ✅ Database name "railway" is just a name (no Railway connection)
- ✅ View tables in Azure Portal → Query Editor
- ✅ Share access via separate users + firewall rules
- ✅ Use Azure Data Studio or pgAdmin for visualization
- ✅ Follow security best practices

