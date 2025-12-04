# Enhanced Logging and Questions List

## ✅ Changes Made

### 1. **Enhanced Logging with Metrics**
- ✅ Added `psutil` for CPU and memory monitoring
- ✅ Added `threading` for process monitoring
- ✅ Enhanced `execute_python()` to track:
  - CPU usage (%)
  - Memory usage (bytes and MB)
  - Execution time (ms)
- ✅ Updated logging to include all metrics in Azure logs
- ✅ Updated monitoring dashboard to display:
  - Container ID
  - Execution Time (ms)
  - CPU Usage (%)
  - Memory Usage (MB)
  - Tests Passed/Total

### 2. **Questions from Database**
- ✅ Updated `server.js` to fetch from `coding_question_bank` table
- ✅ Supports both `coding_question_bank` (main table) and `questions` (legacy)
- ✅ Automatically formats test cases from JSONB fields
- ✅ Frontend will now show ALL questions from the database

---

## 📊 What You'll See in Azure Logs

### **Before:**
```json
{
  "event": "execution_completed",
  "execution_id": "...",
  "user_id": "...",
  "execution_time_ms": 123
}
```

### **After:**
```json
{
  "event": "execution_completed",
  "execution_id": "...",
  "user_id": "...",
  "question_id": "...",
  "submission_id": "...",
  "container_id": "ai-ta-ra-code-executor2-abc123",
  "replica_name": "ai-ta-ra-code-executor2-abc123",
  "language": "python",
  "execution_time_ms": 123,
  "cpu_usage_percent": 15.5,
  "memory_usage_bytes": 52428800,
  "memory_usage_mb": 50.0,
  "tests_passed": 3,
  "tests_total": 3,
  "all_passed": true,
  "timestamp": "2024-01-15T14:40:55.123Z"
}
```

---

## 🎯 Monitoring Dashboard Columns

| Column | Description |
|--------|-------------|
| **Time** | Execution timestamp |
| **User ID** | Unique user identifier |
| **Question ID** | Question being solved |
| **Submission ID** | Unique submission ID |
| **Language** | Programming language |
| **Container ID** | Azure Container ID |
| **Status** | completed/failed/error |
| **Tests Passed** | X/Y format |
| **Time (ms)** | Execution time |
| **CPU %** | CPU usage percentage |
| **Memory (MB)** | Memory usage in MB |

---

## 📋 Questions List

### **Tables Used:**
1. **`coding_question_bank`** (Primary)
   - `uuid` - Question ID
   - `question` - Question text
   - `difficulty` - Easy/Medium/Hard
   - `test_cases` (JSONB) - Test cases
   - `sample_test_cases` (JSONB) - Sample test cases
   - `boiler_plate` - Starter code
   - `tags` - Question tags

2. **`questions`** (Legacy/Additional)
   - `id` - Question ID
   - `title` - Question title
   - `description` - Question description
   - `difficulty` - Easy/Medium/Hard

### **Frontend Display:**
- Shows ALL questions from both tables
- Questions from `coding_question_bank` are formatted to match expected structure
- Test cases are automatically extracted from JSONB fields

---

## 🚀 Next Steps

1. **Deploy Updated Executor:**
   ```bash
   cd aca-executor
   docker build -t executor-secure:v5 .
   docker tag executor-secure:v5 aitaraacr1763805702.azurecr.io/executor-secure:v5
   docker push aitaraacr1763805702.azurecr.io/executor-secure:v5
   ```

2. **Update Terraform:**
   - Update `executor_image` to `v5` in `variables.tf`
   - Run `terraform apply`

3. **Restart Local Server:**
   ```bash
   cd test-ui
   npm start
   ```

4. **Test:**
   - Open `http://localhost:3001`
   - You should see ALL questions from `coding_question_bank`
   - Run code and check Azure logs for full metrics

---

## 📝 Notes

- **CPU Usage:** Tracked per execution using `psutil`
- **Memory Usage:** Tracked as RSS (Resident Set Size) in bytes
- **Container ID:** Automatically extracted from `HOSTNAME` environment variable
- **Test Cases:** Automatically parsed from JSONB in `coding_question_bank`


