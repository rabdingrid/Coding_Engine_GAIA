# 📋 Test Session Table - Setup Guide

## 🎯 What This Table Does

The `test_session` table tracks **candidate test sessions** with the following capabilities:

### Key Features:
1. **Session Tracking**: Tracks when a candidate starts a test
2. **Timing Management**: Monitors test duration and time limits
3. **Activity Monitoring**: Tracks last heartbeat and activity timestamps
4. **Status Management**: Tracks session status (active, completed, abandoned)
5. **Completion Tracking**: Records how the test was completed
6. **Progress Tracking**: Stores completed sections and pending answers as JSON
7. **Auto-timestamps**: Automatically updates `updated_at` on changes

---

## 📊 Table Structure

| Column | Type | Description |
|--------|------|-------------|
| `candidate_id` | VARCHAR(36) | Primary key, references candidate table |
| `test_start_time` | TIMESTAMP | When the test started |
| `test_duration_minutes` | INTEGER | Test duration (default: 60 minutes) |
| `last_heartbeat` | TIMESTAMP | Last heartbeat signal from frontend |
| `last_activity` | TIMESTAMP | Last user activity timestamp |
| `status` | VARCHAR(20) | Status: 'active', 'completed', 'abandoned' |
| `completion_method` | VARCHAR(50) | How test ended: 'manual', 'tab_close', 'timer_expired', etc. |
| `completed_at` | TIMESTAMP | When test was completed |
| `sections_completed` | JSONB | JSON array of completed sections |
| `pending_answers` | JSONB | JSON object of pending answers |
| `created_at` | TIMESTAMP | Auto-set on creation |
| `updated_at` | TIMESTAMP | Auto-updated on changes |

---

## 🔧 How to Run This Query

### Method 1: Azure Portal Query Editor (Easiest)

1. **Go to Azure Portal**: https://portal.azure.com
2. **Search**: `ai-ta-ra-postgre`
3. **Click**: PostgreSQL server
4. **Click**: "Query editor" (left menu)
5. **Login**:
   - Username: `postgresadmin`
   - Password: `5oXcNX59QmEl7zmV3DbjemkiJ`
6. **Paste** the SQL query
7. **Click**: "Run"

### Method 2: Azure Data Studio

1. **Open** Azure Data Studio
2. **Connect** to database (if not already)
3. **Click**: "New Query"
4. **Paste** the SQL query
5. **Press**: `F5` or click "Run"

### Method 3: Command Line (psql)

```bash
# Get connection string
cd Coding_Engine/aca-executor
export AZURE_DB=$(cat .postgres-connection.txt)

# Run the SQL file
psql "$AZURE_DB" < test-session-table.sql
```

### Method 4: Python Script

```python
import psycopg2

conn = psycopg2.connect(
    "postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require"
)

with open('test-session-table.sql', 'r') as f:
    sql = f.read()
    
cur = conn.cursor()
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
```

---

## ✅ What Will Happen

### 1. Table Creation
- Creates `test_session` table with all columns
- Sets up primary key on `candidate_id`
- Creates foreign key to `candidate` table

### 2. Constraints
- **Foreign Key**: Links to `candidate(candidate_id)`
- **Status Check**: Only allows 'active', 'completed', 'abandoned'
- **Completion Method Check**: Validates completion methods

### 3. Indexes
- Index on `status` (for filtering active/completed tests)
- Index on `last_heartbeat` (for timeout detection)
- Index on `test_start_time` (for time-based queries)

### 4. Auto-Update Trigger
- Automatically updates `updated_at` timestamp when row is modified
- No need to manually update this field

---

## 🧪 Verify Table Creation

After running the query, verify with:

```sql
-- Check if table exists
SELECT table_name 
FROM information_schema.tables 
WHERE table_name = 'test_session';

-- View table structure
\d test_session

-- Or
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'test_session'
ORDER BY ordinal_position;

-- Check indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'test_session';

-- Check triggers
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_table = 'test_session';
```

---

## 📝 Example Usage

### Insert a Test Session

```sql
INSERT INTO test_session (
    candidate_id,
    test_start_time,
    test_duration_minutes,
    status
) VALUES (
    'candidate-uuid-here',
    CURRENT_TIMESTAMP,
    60,
    'active'
);
```

### Update Heartbeat

```sql
UPDATE test_session
SET 
    last_heartbeat = CURRENT_TIMESTAMP,
    last_activity = CURRENT_TIMESTAMP
WHERE candidate_id = 'candidate-uuid-here';
```

### Mark Section as Completed

```sql
UPDATE test_session
SET sections_completed = '["section1", "section2"]'::jsonb
WHERE candidate_id = 'candidate-uuid-here';
```

### Complete Test

```sql
UPDATE test_session
SET 
    status = 'completed',
    completion_method = 'manual',
    completed_at = CURRENT_TIMESTAMP
WHERE candidate_id = 'candidate-uuid-here';
```

### Find Active Sessions

```sql
SELECT * FROM test_session
WHERE status = 'active'
AND test_start_time + (test_duration_minutes || ' minutes')::interval > CURRENT_TIMESTAMP;
```

### Find Abandoned Sessions (No heartbeat for 5 minutes)

```sql
SELECT * FROM test_session
WHERE status = 'active'
AND last_heartbeat < CURRENT_TIMESTAMP - INTERVAL '5 minutes';
```

---

## ⚠️ Prerequisites

Before running, ensure:

1. **`candidate` table exists** with `candidate_id` column
2. **You have permissions** to create tables
3. **Database connection** is working

### Check Candidate Table

```sql
-- Verify candidate table exists
SELECT table_name 
FROM information_schema.tables 
WHERE table_name = 'candidate';

-- Check candidate_id column
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'candidate' 
AND column_name = 'candidate_id';
```

If `candidate` table doesn't exist or has different structure, you may need to:
- Create the candidate table first
- Or modify the foreign key constraint

---

## 🔍 Troubleshooting

### Error: "relation candidate does not exist"
**Solution**: Create candidate table first or remove foreign key constraint temporarily

### Error: "permission denied"
**Solution**: Ensure you're using admin user (`postgresadmin`)

### Error: "column candidate_id does not exist in candidate"
**Solution**: Check candidate table structure and update foreign key reference

---

## 📊 Use Cases

### 1. **Test Session Management**
- Track when candidates start tests
- Monitor test duration
- Detect abandoned sessions

### 2. **Activity Monitoring**
- Heartbeat system to detect if candidate is still active
- Track last activity for timeout detection

### 3. **Progress Tracking**
- Store completed sections
- Track pending answers
- Resume tests if needed

### 4. **Analytics**
- Analyze completion rates
- Track average test duration
- Identify abandonment patterns

---

## 🎯 Summary

**What it does:**
- ✅ Creates `test_session` table for tracking candidate test sessions
- ✅ Sets up foreign key to `candidate` table
- ✅ Creates indexes for performance
- ✅ Adds auto-update trigger for `updated_at`
- ✅ Enforces data integrity with constraints

**How to run:**
1. Copy SQL from `test-session-table.sql`
2. Use Azure Portal Query Editor (easiest)
3. Or use Azure Data Studio / psql / Python

**Result:**
- Table ready for test session tracking
- Automatic timestamp management
- Optimized for queries

---

**Ready to create the table!** 🚀

