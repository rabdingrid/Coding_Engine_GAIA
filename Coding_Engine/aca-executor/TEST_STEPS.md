# Azure Data Studio - Test Steps

## ✅ Setup Complete!

Azure Data Studio has been downloaded and should be opening now.

## 📋 Connection Details (Copy-Paste)

```
Server: ai-ta-ra-postgre.postgres.database.azure.com
Database: railway
Username: postgresadmin
Password: 5oXcNX59QmEl7zmV3DbjemkiJ
SSL: ✅ Enable (Required)
```

## 🧪 Step-by-Step Test Instructions

### Step 1: Install PostgreSQL Extension (2 minutes)

1. **Wait for Azure Data Studio to open**
2. **Click** the Extensions icon (left sidebar) or press `Cmd+Shift+X` (Mac) / `Ctrl+Shift+X` (Windows)
3. **Search** for: `PostgreSQL`
4. **Install**: "PostgreSQL" by Microsoft (first result)
5. **Click** "Reload" if prompted

### Step 2: Connect to Database (1 minute)

1. **Click** "New Connection" button (left sidebar) or press `Cmd+N` / `Ctrl+N`
2. **Select**: Connection type → **PostgreSQL**
3. **Fill in**:
   - **Server name**: `ai-ta-ra-postgre.postgres.database.azure.com`
   - **Database name**: `railway`
   - **Authentication type**: Username/Password
   - **User name**: `postgresadmin`
   - **Password**: `5oXcNX59QmEl7zmV3DbjemkiJ`
   - **SSL**: ✅ **Enable SSL** (check this box!)
   - **Server group**: Default
   - **Name (optional)**: Azure PostgreSQL
4. **Click** "Connect"

### Step 3: Verify Connection (30 seconds)

1. **Check** left sidebar - you should see your connection
2. **Expand**: Your connection → Databases → railway → Tables
3. **You should see** 14 tables including:
   - `coding_question_bank`
   - `test_cases`
   - `users`
   - etc.

### Step 4: View Data (30 seconds)

1. **Click** on `coding_question_bank` table
2. **Right-click** → "Select Top 1000"
3. **You should see** 52 questions with data

### Step 5: Run Test Queries (1 minute)

1. **Click** "New Query" button (top toolbar)
2. **Open** file: `test-queries.sql` (in this folder)
3. **Run** first query:
   ```sql
   SELECT version();
   ```
   - Press `F5` or click "Run"
   - Should show: PostgreSQL 14.19

4. **Run** second query:
   ```sql
   SELECT COUNT(*) as total_questions FROM coding_question_bank;
   ```
   - Should show: 52

5. **Run** third query:
   ```sql
   SELECT * FROM coding_question_bank LIMIT 10;
   ```
   - Should show 10 questions with all columns

## ✅ Success Indicators

If you see:
- ✅ Connection appears in left sidebar
- ✅ 14 tables listed under railway database
- ✅ Can view data in `coding_question_bank`
- ✅ Queries return results

**Then your connection is working!** 🎉

## 🐛 Troubleshooting

### Connection Timeout?
- **Check**: Firewall rule for your IP is added
- **Verify**: SSL is enabled
- **Test**: Connection from terminal (already tested ✅)

### Can't Find PostgreSQL Extension?
- **Search**: "PostgreSQL" (not "postgres")
- **Install**: The one by Microsoft (official)

### Can't See Tables?
- **Expand**: Connection → Databases → railway → Tables
- **Refresh**: Right-click connection → Refresh

### Password Not Working?
- **Check**: Password is `5oXcNX59QmEl7zmV3DbjemkiJ`
- **Verify**: No extra spaces

## 📊 Quick Test Queries

Copy-paste these in Azure Data Studio:

```sql
-- 1. Check connection
SELECT version();

-- 2. List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- 3. Count questions
SELECT COUNT(*) FROM coding_question_bank;

-- 4. View sample data
SELECT id, question, difficulty 
FROM coding_question_bank 
LIMIT 5;
```

## 🎯 Next Steps

Once connected:
- ✅ Browse all tables
- ✅ View and edit data
- ✅ Run complex queries
- ✅ Export data to CSV/JSON
- ✅ Share connection with team

## 📝 Files Available

- `test-queries.sql` - Sample queries to test
- `azure-data-studio-connection.json` - Connection config
- `TEST_STEPS.md` - This file

---

**Ready to test!** Open Azure Data Studio and follow the steps above. 🚀

