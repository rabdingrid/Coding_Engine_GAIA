# 🗄️ Azure PostgreSQL Database - Team Guide

Complete guide for team members to view, access, and manage the Azure PostgreSQL database.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Setting Up Azure Data Studio](#setting-up-azure-data-studio)
3. [Connecting to Database](#connecting-to-database)
4. [Viewing Data](#viewing-data)
5. [Adding Data](#adding-data)
6. [Updating Data](#updating-data)
7. [Common Operations](#common-operations)
8. [Troubleshooting](#troubleshooting)
9. [Security & Access](#security--access)

---

## 🚀 Quick Start

### Prerequisites
- Azure Data Studio installed (see [Setup](#setting-up-azure-data-studio))
- Database access credentials (get from team lead)
- Your IP address added to firewall (contact team lead)

### Connection Details
```
Server: ai-ta-ra-postgre.postgres.database.azure.com
Port: 5432
Database: railway
Username: postgresadmin (or your assigned username)
Password: [Get from team lead]
SSL: Required
```

---

## 💻 Setting Up Azure Data Studio

### Step 1: Install Azure Data Studio

**macOS:**
```bash
brew install --cask azure-data-studio
```

**Windows:**
- Download from: https://aka.ms/azuredatastudio
- Run installer

**Linux:**
```bash
# Download and extract
wget https://azuredatastudio-update.azurewebsites.net/latest/linux-x64/archive -O azuredatastudio.tar.gz
tar -xzf azuredatastudio.tar.gz
./azuredatastudio-linux-x64/azuredatastudio
```

### Step 2: Install PostgreSQL Extension

1. **Open** Azure Data Studio
2. **Click** Extensions icon (left sidebar) or press `Cmd+Shift+X` (Mac) / `Ctrl+Shift+X` (Windows)
3. **Search** for: `PostgreSQL`
4. **Install**: "PostgreSQL" by Microsoft (first result)
5. **Click** "Reload" if prompted

✅ **Extension installed!**

---

## 🔌 Connecting to Database

### Step 1: Create New Connection

1. **Click** "New Connection" button (left sidebar) or press `Cmd+N` / `Ctrl+N`
2. **Select**: Connection type → **PostgreSQL**

### Step 2: Enter Connection Details

Fill in the following:

| Field | Value |
|-------|-------|
| **Server name** | `ai-ta-ra-postgre.postgres.database.azure.com` |
| **Database name** | `railway` |
| **Authentication type** | Username/Password |
| **User name** | `postgresadmin` (or your assigned username) |
| **Password** | [Get from team lead] |
| **SSL** | ✅ **Enable SSL** (check this box!) |
| **Server group** | Default |
| **Name (optional)** | Azure PostgreSQL |

### Step 3: Connect

1. **Click** "Connect" button
2. **Wait** for connection to establish
3. **Verify** connection appears in left sidebar

✅ **Connected!**

---

## 👀 Viewing Data

### Method 1: Browse Tables (Easiest)

1. **Expand** your connection in left sidebar:
   ```
   Azure PostgreSQL
   └── Databases
       └── railway
           └── Tables
   ```

2. **Click** on any table (e.g., `coding_question_bank`)

3. **Right-click** → "Select Top 1000"

4. **View** data in the results panel

### Method 2: Run SQL Queries

1. **Click** "New Query" button (top toolbar)

2. **Type** your query:
   ```sql
   SELECT * FROM coding_question_bank LIMIT 10;
   ```

3. **Press** `F5` or click "Run"

4. **View** results below

### Common View Queries

```sql
-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Count records in a table
SELECT COUNT(*) FROM coding_question_bank;

-- View all questions
SELECT id, uuid, question, difficulty, tags 
FROM coding_question_bank 
ORDER BY id;

-- View specific question
SELECT * FROM coding_question_bank 
WHERE id = 1;

-- View test cases for a question
SELECT * FROM test_cases 
WHERE question_id = 1;
```

---

## ➕ Adding Data

### Adding a New Question

```sql
-- Insert a new question into coding_question_bank
INSERT INTO coding_question_bank (
    uuid,
    question,
    difficulty,
    tags,
    test_cases,
    sample_test_cases,
    boiler_plate
) VALUES (
    gen_random_uuid(),  -- Generates a new UUID
    'Your question description here',
    'Medium',  -- Easy, Medium, or Hard
    ARRAY['Array', 'Two Pointers'],  -- Array of tags
    '[
        {
            "input": "test input",
            "expected_output": "test output"
        }
    ]'::jsonb,  -- Full test cases as JSON
    '[
        {
            "input": "sample input",
            "expected_output": "sample output"
        }
    ]'::jsonb,  -- Sample test cases as JSON
    '{
        "python": "def solve():\n    pass",
        "java": "public class Solution {\n    public int solve() {\n        return 0;\n    }\n}",
        "cpp": "int solve() {\n    return 0;\n}",
        "javascript": "function solve() {\n    return 0;\n}",
        "csharp": "public int Solve() {\n    return 0;\n}"
    }'::jsonb  -- Boilerplates as JSON
);
```

### Adding Test Cases

```sql
-- Add test case to existing question
INSERT INTO test_cases (
    question_id,
    input_data,
    expected_output,
    is_sample
) VALUES (
    1,  -- Question ID
    'test input data',
    'expected output',
    false  -- true for sample test case
);
```

### Adding a User

```sql
INSERT INTO users (username, email, role)
VALUES ('newuser', 'user@example.com', 'student');
```

### Adding a Candidate

```sql
INSERT INTO candidate (
    name,
    email,
    phone,
    status
) VALUES (
    'John Doe',
    'john@example.com',
    '+1234567890',
    'active'
);
```

---

## ✏️ Updating Data

### Update a Question

```sql
-- Update question details
UPDATE coding_question_bank
SET 
    question = 'Updated question description',
    difficulty = 'Hard',
    tags = ARRAY['Dynamic Programming', 'Graph']
WHERE id = 1;
```

### Update Test Cases

```sql
-- Update test cases for a question
UPDATE coding_question_bank
SET test_cases = '[
    {
        "input": "new input",
        "expected_output": "new output"
    }
]'::jsonb
WHERE id = 1;
```

### Update User Status

```sql
UPDATE users
SET role = 'admin'
WHERE username = 'john';
```

---

## 🔧 Common Operations

### Delete Data (Use with Caution!)

```sql
-- Delete a question (be careful!)
DELETE FROM coding_question_bank
WHERE id = 1;

-- Delete test cases
DELETE FROM test_cases
WHERE question_id = 1;
```

### Search Data

```sql
-- Search questions by tag
SELECT * FROM coding_question_bank
WHERE 'Array' = ANY(tags);

-- Search by difficulty
SELECT * FROM coding_question_bank
WHERE difficulty = 'Medium';

-- Search by keyword in question
SELECT * FROM coding_question_bank
WHERE question ILIKE '%two sum%';
```

### Export Data

1. **Run** your query
2. **Right-click** on results
3. **Select** "Save as CSV" or "Save as JSON"
4. **Choose** location and save

### Import Data from File

```sql
-- For CSV files, use COPY command
COPY coding_question_bank(id, question, difficulty)
FROM '/path/to/file.csv'
DELIMITER ','
CSV HEADER;
```

---

## 🐛 Troubleshooting

### Connection Issues

**Problem**: Connection timeout
- **Solution**: Check if your IP is added to firewall
- **Action**: Contact team lead to add your IP

**Problem**: SSL connection error
- **Solution**: Make sure "Enable SSL" is checked
- **Action**: Reconnect with SSL enabled

**Problem**: Authentication failed
- **Solution**: Verify username and password
- **Action**: Contact team lead for correct credentials

### Query Issues

**Problem**: Table not found
- **Solution**: Check table name spelling
- **Action**: Run `\dt` to list all tables

**Problem**: Permission denied
- **Solution**: Your user might not have write permissions
- **Action**: Contact team lead for access

**Problem**: JSON parsing error
- **Solution**: Verify JSON syntax is valid
- **Action**: Use JSON validator before inserting

### Performance Issues

**Problem**: Query is slow
- **Solution**: Add LIMIT clause for large tables
- **Action**: Use `LIMIT 100` in your queries

---

## 🔐 Security & Access

### Getting Access

1. **Contact** team lead to:
   - Get database credentials
   - Add your IP to firewall
   - Get appropriate permissions

2. **Request** specific access:
   - Read-only (SELECT)
   - Read-write (SELECT, INSERT, UPDATE)
   - Admin (all permissions)

### Best Practices

✅ **DO:**
- Use parameterized queries
- Validate data before inserting
- Test queries on small datasets first
- Backup before major changes
- Use transactions for multiple operations

❌ **DON'T:**
- Share passwords publicly
- Delete data without backup
- Run untested queries on production
- Use admin account for regular operations
- Store passwords in code

### Creating Transactions

```sql
-- Start transaction
BEGIN;

-- Your operations
INSERT INTO coding_question_bank (...) VALUES (...);
UPDATE coding_question_bank SET ... WHERE id = 1;

-- Commit if everything is OK
COMMIT;

-- Or rollback if something went wrong
-- ROLLBACK;
```

---

## 📊 Database Schema Reference

### Main Tables

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `coding_question_bank` | DSA questions | id, uuid, question, difficulty, tags |
| `test_cases` | Test cases for questions | id, question_id, input_data, expected_output |
| `users` | User accounts | id, username, email, role |
| `candidate` | Candidate information | id, name, email, status |
| `jobs` | Job postings | id, title, description, status |
| `interview_coding` | Coding interviews | id, candidate_id, question_id, status |
| `interview_mcq` | MCQ interviews | id, candidate_id, question_id, score |

### View Table Structure

```sql
-- Get column information for a table
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'coding_question_bank'
ORDER BY ordinal_position;
```

---

## 📝 Example Workflows

### Workflow 1: Add a Complete Question

```sql
-- Step 1: Insert question
INSERT INTO coding_question_bank (
    uuid, question, difficulty, tags, test_cases, sample_test_cases, boiler_plate
) VALUES (
    gen_random_uuid(),
    'Reverse Linked List',
    'Easy',
    ARRAY['Linked List', 'Recursion'],
    '[
        {"input": "[1,2,3]", "expected_output": "[3,2,1]"},
        {"input": "[1]", "expected_output": "[1]"}
    ]'::jsonb,
    '[
        {"input": "[1,2,3]", "expected_output": "[3,2,1]"}
    ]'::jsonb,
    '{
        "python": "def reverseList(head):\n    pass",
        "java": "public ListNode reverseList(ListNode head) {\n    return null;\n}"
    }'::jsonb
) RETURNING id;

-- Step 2: Note the returned ID and add test cases
INSERT INTO test_cases (question_id, input_data, expected_output)
VALUES (LASTVAL(), '[1,2,3]', '[3,2,1]');
```

### Workflow 2: Bulk Import Questions

```sql
-- Insert multiple questions at once
INSERT INTO coding_question_bank (uuid, question, difficulty, tags)
VALUES 
    (gen_random_uuid(), 'Question 1', 'Easy', ARRAY['Array']),
    (gen_random_uuid(), 'Question 2', 'Medium', ARRAY['Tree']),
    (gen_random_uuid(), 'Question 3', 'Hard', ARRAY['Graph']);
```

### Workflow 3: Update Multiple Records

```sql
-- Update difficulty for all Easy questions to Medium
UPDATE coding_question_bank
SET difficulty = 'Medium'
WHERE difficulty = 'Easy'
AND id IN (1, 2, 3);
```

---

## 🎯 Quick Reference

### Connection String Format
```
postgresql://username:password@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require
```

### Common SQL Commands

```sql
-- List tables
\dt

-- Describe table
\d table_name

-- List databases
\l

-- Exit
\q
```

### Useful Queries

```sql
-- Count all records
SELECT 
    'coding_question_bank' as table_name, COUNT(*) as count FROM coding_question_bank
UNION ALL
SELECT 'test_cases', COUNT(*) FROM test_cases
UNION ALL
SELECT 'users', COUNT(*) FROM users;

-- Find questions by tag
SELECT id, question, difficulty 
FROM coding_question_bank 
WHERE 'Array' = ANY(tags);

-- Get recent questions
SELECT * FROM coding_question_bank 
ORDER BY id DESC 
LIMIT 10;
```

---

## 📞 Support

### Need Help?

1. **Check** this guide first
2. **Review** `TEST_STEPS.md` for connection setup
3. **Contact** team lead for:
   - Access issues
   - Permission problems
   - Database errors

### Resources

- **Azure Data Studio Docs**: https://docs.microsoft.com/azure-data-studio
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Team Guide**: This file
- **Test Queries**: `test-queries.sql`

---

## ✅ Checklist for New Team Members

- [ ] Azure Data Studio installed
- [ ] PostgreSQL extension installed
- [ ] Database connection configured
- [ ] Can view tables
- [ ] Can run queries
- [ ] Understands permissions
- [ ] Knows who to contact for help

---

**Last Updated**: December 2024  
**Database**: Azure PostgreSQL (ai-ta-ra-postgre)  
**Location**: eastus2

---

🎉 **You're all set! Happy querying!** 🎉

