# Database Information

## 📊 Database Details

### **Database Type:** PostgreSQL
### **Host:** Railway (External Service)
### **Connection String:**
```
postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway
```

**Note:** This is the database connection string you provided earlier. I did NOT create this database - it's your existing Railway PostgreSQL database.

---

## 📋 Tables in Database

---

## 🔄 Database Flow

### **1. Questions Flow:**
```
Frontend → GET /api/questions
    ↓
Backend queries: SELECT * FROM questions
    ↓
Returns: List of questions
    ↓
Frontend displays in sidebar
```

### **2. Test Cases Flow:**
```
User selects question
    ↓
Frontend → GET /api/questions/:id
    ↓
Backend queries:
  - SELECT * FROM questions WHERE id = ?
  - SELECT * FROM test_cases WHERE question_id = ?
    ↓
Returns: Question + Test Cases
    ↓
Frontend displays test cases
```

### **3. Code Execution Flow:**
```
User runs code
    ↓
Frontend → POST /proxy/execute
    ↓
Backend → Executor Service (Azure)
    ↓
Executor runs code against test cases
    ↓
Returns: Results (pass/fail)
    ↓
Frontend displays results
```

**Note:** Execution results are currently stored in **memory** (not database). For production, you'd want to store them in an `executions` table.

---

## 💾 Storage Locations

| Data | Storage | Location |
|------|---------|----------|
| **Questions** | Database | PostgreSQL (Railway) |
| **Test Cases** | Database | PostgreSQL (Railway) |
| **Executions** | Memory | In-memory array (clears on restart) |
| **User IDs** | Browser | localStorage (per browser) |

---

## 🚀 For Production

### **Recommended: Create `executions` Table**

```sql
CREATE TABLE executions (
  id SERIAL PRIMARY KEY,
  execution_id VARCHAR(255) UNIQUE,
  user_id VARCHAR(255),
  question_id VARCHAR(255),
  submission_id VARCHAR(255),
  container_id VARCHAR(255),
  replica_name VARCHAR(255),
  language VARCHAR(50),
  code TEXT,
  execution_time_ms INTEGER,
  tests_passed INTEGER,
  tests_total INTEGER,
  all_passed BOOLEAN,
  status VARCHAR(50),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Benefits:**
- ✅ Persistent storage (survives server restarts)
- ✅ Historical data
- ✅ Analytics and reporting
- ✅ Audit trail

---

## 📋 Summary

### **Database:** PostgreSQL (Railway) - **You provided this**
### **Tables Created:** `questions`, `test_cases` (if didn't exist)
### **Current Data:** 1 question, 3 test cases
### **Executions:** Stored in memory (not database yet)

**I did NOT create the database** - I only created tables in your existing Railway PostgreSQL database.


