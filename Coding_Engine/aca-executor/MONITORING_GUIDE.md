# Monitoring Guide - Code Execution Platform

## 📊 Overview

The monitoring system tracks:
- Which container is running which candidate's code
- Execution time per submission
- Test cases passed/failed
- User ID, Question ID, Submission ID
- Container/Replica information
- Real-time execution status

---

## 🔧 Implementation Status

### ✅ Completed:
1. **Logging in Executor Service** - All executions are logged with metadata
2. **Monitoring Dashboard UI** - Admin dashboard to view executions
3. **Metadata Tracking** - user_id, submission_id, container_id, execution_time

### 📋 To Complete:
1. **Database Table** - Store executions in PostgreSQL
2. **Backend API** - Fetch executions from database
3. **Azure Monitor Integration** - View logs in Azure Portal

---

## 🚀 How to View Monitoring

### Option 1: Local Monitoring Dashboard

1. **Start the monitoring dashboard:**
   ```bash
   cd aca-executor
   # Open monitoring-dashboard.html in browser
   open monitoring-dashboard.html
   ```

2. **Or serve via local server:**
   ```bash
   cd aca-executor/test-ui
   # The dashboard is available at http://localhost:3001/monitoring-dashboard.html
   ```

### Option 2: Azure Monitor (Production)

1. **Go to Azure Portal:**
   - Navigate to your Container App: `ai-ta-ra-code-executor2`
   - Click on "Log stream" or "Monitoring"

2. **View Logs:**
   - All execution logs are automatically sent to Azure Monitor
   - Search for: `execution_started`, `execution_completed`, `execution_error`

3. **Query Logs (KQL):**
   ```kql
   ContainerAppConsoleLogs
   | where Log_s contains "execution_started"
   | project TimeGenerated, Log_s
   | order by TimeGenerated desc
   ```

---

## 📝 Log Format

Each execution logs JSON with:
```json
{
  "event": "execution_started",
  "execution_id": "uuid",
  "user_id": "U123",
  "question_id": "Q2",
  "submission_id": "SUB789",
  "container_id": "container-name",
  "replica_name": "replica-name",
  "language": "python",
  "test_cases_count": 3,
  "timestamp": "2025-11-28T12:00:00Z"
}
```

---

## 🔍 What You Can Monitor

### Real-Time:
- ✅ Which container is processing which user
- ✅ Execution status (running/completed/error)
- ✅ Execution time per submission
- ✅ Test cases passed/failed

### Historical:
- ✅ All submissions by user
- ✅ Average execution time
- ✅ Success rate
- ✅ Container utilization

---

## 📊 Next Steps

1. **Create Executions Table:**
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
     execution_time_ms INTEGER,
     tests_passed INTEGER,
     tests_total INTEGER,
     all_passed BOOLEAN,
     status VARCHAR(50),
     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

2. **Update Backend to Store Executions:**
   - Modify executor service to save to database
   - Or create a separate service to consume logs

3. **View in Azure Portal:**
   - Go to Container App → Logs
   - Use KQL queries to filter by user_id, question_id, etc.

---

## 💡 Tips

- **Filter by User**: Search logs for specific `user_id`
- **Filter by Container**: Search logs for specific `container_id`
- **Track Performance**: Monitor `execution_time_ms` over time
- **Debug Issues**: Check `execution_error` events

