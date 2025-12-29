# Azure PostgreSQL Database Connection Guide

## 📊 Database Connection Details

### Connection Information

| Field | Value |
|-------|-------|
| **Server Name** | `ai-ta-ra-postgre.postgres.database.azure.com` |
| **Port** | `5432` |
| **Database Name** | `railway` |
| **Username** | `postgresadmin` |
| **Password** | `5oXcNX59QmEl7zmV3DbjemkiJ` |
| **SSL Mode** | **Required** (must enable SSL) |

### Full Connection String
```
postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require
```

---

## 🐘 Connecting via pgAdmin

### Step 1: Install pgAdmin

**macOS:**
```bash
# Using Homebrew
brew install --cask pgadmin4

# Or download from: https://www.pgadmin.org/download/
```

**Windows:**
- Download from: https://www.pgadmin.org/download/pgadmin-4-windows/
- Install the application

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install pgadmin4

# Or download from: https://www.pgadmin.org/download/
```

### Step 2: Open pgAdmin

1. Launch **pgAdmin 4**
2. If prompted, set a master password (for pgAdmin itself, not the database)

### Step 3: Add New Server

1. **Right-click** on "Servers" in the left panel
2. Select **"Create" → "Server..."**

### Step 4: General Tab

Fill in the **General** tab:

| Field | Value |
|-------|-------|
| **Name** | `Azure PostgreSQL - Coding Engine` (or any name you prefer) |

### Step 5: Connection Tab

Fill in the **Connection** tab with these details:

| Field | Value |
|-------|-------|
| **Host name/address** | `ai-ta-ra-postgre.postgres.database.azure.com` |
| **Port** | `5432` |
| **Maintenance database** | `railway` |
| **Username** | `postgresadmin` |
| **Password** | `5oXcNX59QmEl7zmV3DbjemkiJ` |
| ✅ **Save password** | Check this box (optional, for convenience) |

### Step 6: SSL Tab (IMPORTANT!)

**This is critical for Azure PostgreSQL!**

1. Go to the **SSL** tab
2. Set **SSL mode** to: **`Require`** or **`Prefer`**
3. ✅ Check **"SSL mode"** dropdown and select **"require"**

**Alternative SSL Settings:**
- **SSL mode**: `Require`
- **Client certificate**: Leave empty (unless you have one)
- **Client certificate key**: Leave empty
- **Root certificate**: Leave empty (Azure uses public CA)

### Step 7: Advanced Tab (Optional)

- **DB restriction**: Leave empty (to see all databases)
- Or enter `railway` to only show the railway database

### Step 8: Save and Connect

1. Click **"Save"**
2. pgAdmin will attempt to connect
3. If successful, you'll see the server in the left panel

---

## 🔍 Viewing Database Tables

Once connected:

1. **Expand** the server: `Azure PostgreSQL - Coding Engine`
2. **Expand** "Databases"
3. **Expand** "railway"
4. **Expand** "Schemas"
5. **Expand** "public"
6. **Click** "Tables"

You should see tables like:
- `coding_question_bank`
- `submissions`
- `test_session`
- And other tables...

### View Table Data

1. **Right-click** on any table (e.g., `coding_question_bank`)
2. Select **"View/Edit Data" → "All Rows"**
3. The table data will appear in a grid

### Run SQL Queries

1. **Right-click** on "railway" database
2. Select **"Query Tool"**
3. Type your SQL query, e.g.:
   ```sql
   SELECT * FROM coding_question_bank LIMIT 10;
   ```
4. Click **"Execute"** (F5) or press **F5**

---

## 🔐 Security Notes

⚠️ **Important:**
- The password is stored in code for development purposes
- For production, use environment variables or Azure Key Vault
- Never commit passwords to version control
- Azure PostgreSQL requires SSL connections by default

---

## 🛠️ Troubleshooting

### Connection Timeout

**Problem:** Cannot connect to server

**Solutions:**
1. **Check Firewall Rules:**
   - Go to Azure Portal → PostgreSQL server → Networking
   - Ensure your IP is allowed, or "Allow Azure services" is enabled

2. **Check SSL:**
   - Make sure SSL mode is set to "Require" in pgAdmin

3. **Test Connection:**
   ```bash
   # Test from command line
   psql "host=ai-ta-ra-postgre.postgres.database.azure.com port=5432 dbname=railway user=postgresadmin sslmode=require"
   ```

### SSL Certificate Error

**Problem:** SSL certificate verification failed

**Solutions:**
1. In pgAdmin SSL tab, try **"Prefer"** instead of **"Require"**
2. Or download Azure's root certificate and specify it in SSL tab

### Authentication Failed

**Problem:** Password authentication failed

**Solutions:**
1. Double-check the password: `5oXcNX59QmEl7zmV3DbjemkiJ`
2. Ensure username is exactly: `postgresadmin`
3. Check if the database server is running in Azure Portal

---

## 📝 Quick Reference

### Connection Parameters Summary

```
Host:     ai-ta-ra-postgre.postgres.database.azure.com
Port:     5432
Database: railway
User:     postgresadmin
Password: 5oXcNX59QmEl7zmV3DbjemkiJ
SSL:      Required
```

### Common SQL Queries

```sql
-- View all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Count questions
SELECT COUNT(*) FROM coding_question_bank;

-- View recent submissions
SELECT * FROM submissions 
ORDER BY created_at DESC 
LIMIT 10;

-- View test sessions
SELECT * FROM test_session 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## ✅ Verification

After connecting, verify by running:

```sql
SELECT version();
```

You should see PostgreSQL version information.

---

**Last Updated:** 2024
**Database:** Azure PostgreSQL Flexible Server
**Server:** ai-ta-ra-postgre




