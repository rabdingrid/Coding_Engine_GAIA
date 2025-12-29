# pgAdmin Connection Setup - Quick Guide

## ✅ pgAdmin Installed Successfully!

pgAdmin 4 has been installed to: `/Applications/pgAdmin 4.app`

---

## 🚀 Quick Connection Steps

### Step 1: Launch pgAdmin

1. Open **Finder**
2. Go to **Applications**
3. Double-click **pgAdmin 4.app**
4. If prompted, set a **master password** for pgAdmin (this is for pgAdmin itself, not the database)

### Step 2: Add Server Connection

1. In the left panel, **right-click** on **"Servers"**
2. Select **"Create" → "Server..."**

### Step 3: General Tab

- **Name**: `Azure PostgreSQL - Coding Engine` (or any name you prefer)
- Click **Next** or go to **Connection** tab

### Step 4: Connection Tab (IMPORTANT!)

Fill in these exact values:

| Field | Value |
|-------|-------|
| **Host name/address** | `ai-ta-ra-postgre.postgres.database.azure.com` |
| **Port** | `5432` |
| **Maintenance database** | `railway` |
| **Username** | `postgresadmin` |
| **Password** | `5oXcNX59QmEl7zmV3DbjemkiJ` |
| ✅ **Save password** | Check this box |

### Step 5: SSL Tab (CRITICAL!)

1. Click on **SSL** tab
2. Set **SSL mode** to: **`Require`**
3. This is **required** for Azure PostgreSQL!

### Step 6: Save

1. Click **"Save"**
2. pgAdmin will connect automatically
3. You should see the server appear in the left panel

---

## 🔍 Verify Connection

Once connected:

1. **Expand** the server: `Azure PostgreSQL - Coding Engine`
2. **Expand** "Databases"
3. **Expand** "railway"
4. **Expand** "Schemas"
5. **Expand** "public"
6. **Click** "Tables"

You should see:
- `coding_question_bank`
- `submissions`
- `test_session`
- And other tables

---

## 🛠️ Troubleshooting

### If connection fails:

1. **Check Firewall:**
   - Go to Azure Portal → PostgreSQL server → Networking
   - Ensure "Allow Azure services" is enabled

2. **Check SSL:**
   - Make sure SSL mode is set to "Require"

3. **Test from terminal:**
   ```bash
   psql "host=ai-ta-ra-postgre.postgres.database.azure.com port=5432 dbname=railway user=postgresadmin sslmode=require"
   # Enter password when prompted: 5oXcNX59QmEl7zmV3DbjemkiJ
   ```

---

## 📝 Connection Details Summary

```
Host:     ai-ta-ra-postgre.postgres.database.azure.com
Port:     5432
Database: railway
Username: postgresadmin
Password: 5oXcNX59QmEl7zmV3DbjemkiJ
SSL:      Require
```

---

**Ready to connect!** Launch pgAdmin and follow the steps above.




