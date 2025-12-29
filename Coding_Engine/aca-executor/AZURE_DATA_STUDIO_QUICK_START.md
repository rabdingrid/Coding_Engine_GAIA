# Azure Data Studio - Quick Start Guide

## 🚀 Quick Steps to Connect to Azure PostgreSQL

### Step 1: Download & Install (2 minutes)

1. **Download**: https://aka.ms/azuredatastudio
2. **Install**: Run the installer (macOS/Windows/Linux)
3. **Open**: Azure Data Studio

### Step 2: Install PostgreSQL Extension (1 minute)

1. **Click** the Extensions icon (left sidebar) or `Cmd+Shift+X` (Mac) / `Ctrl+Shift+X` (Windows)
2. **Search**: "PostgreSQL"
3. **Install**: "PostgreSQL" by Microsoft (first result)
4. **Reload** if prompted

### Step 3: Connect to Database (1 minute)

1. **Click** "New Connection" (left sidebar) or `Cmd+N` / `Ctrl+N`
2. **Fill in**:
   - **Connection type**: PostgreSQL
   - **Server name**: `ai-ta-ra-postgre.postgres.database.azure.com`
   - **Database name**: `railway`
   - **Authentication type**: Username/Password
   - **User name**: `postgresadmin`
   - **Password**: (from `.postgres-connection.txt`)
   - **SSL**: ✅ Enable SSL (Required)
   - **Server group**: Default
   - **Name (optional)**: Azure PostgreSQL
3. **Click** "Connect"

### Step 4: View Tables (30 seconds)

1. **Expand** your connection in left sidebar
2. **Expand** "Databases" → "railway" → "Tables"
3. **Click** any table (e.g., `coding_question_bank`)
4. **Right-click** → "Select Top 1000" to view data

### Step 5: Run Queries (30 seconds)

1. **Click** "New Query" button (top toolbar)
2. **Type**:
   ```sql
   SELECT * FROM coding_question_bank LIMIT 10;
   ```
3. **Click** "Run" or press `F5`

## ✅ That's It! You're Connected!

## 🎯 Quick Tips

### View All Tables
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

### Count Records
```sql
SELECT COUNT(*) FROM coding_question_bank;
```

### View Table Structure
- Right-click table → "Script as" → "CREATE"

### Export Data
- Right-click query results → "Save as CSV/JSON"

## 🔗 Connection Details (Copy-Paste Ready)

**Server**: `ai-ta-ra-postgre.postgres.database.azure.com`  
**Database**: `railway`  
**Username**: `postgresadmin`  
**Password**: Check `.postgres-connection.txt`  
**SSL**: ✅ Required

## 📝 Troubleshooting

### Connection Timeout?
- Check firewall: Your IP must be added
- Verify SSL is enabled
- Check password is correct

### Extension Not Found?
- Search "PostgreSQL" (not "postgres")
- Install from Microsoft (official)

### Can't See Tables?
- Expand: Connection → Databases → railway → Tables
- Refresh connection (right-click → Refresh)

## 🎉 You're Ready!

Azure Data Studio is now connected to your Azure PostgreSQL database. You can:
- ✅ Browse all tables
- ✅ View and edit data
- ✅ Run SQL queries
- ✅ Export data
- ✅ Visualize data

