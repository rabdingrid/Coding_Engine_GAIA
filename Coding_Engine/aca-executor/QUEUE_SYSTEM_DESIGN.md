# Queue System Design for 200-300 Concurrent Users

## 🎯 Requirements

- **Users**: 200-300 students
- **Test Duration**: 3 hours
- **Questions per Student**: 2 coding questions
- **Max Wait Time**: 5 seconds
- **User Tracking**: user_id and question_id for result routing

---

## 📊 Capacity Analysis

### Worst Case Scenario

**Peak Load:**
- All 300 students submit simultaneously at contest start
- 300 students × 2 questions = **600 concurrent submissions**

**Current Performance:**
- Average execution time: ~2-3 seconds (with parallel test execution)
- Each submission processes 13 test cases in parallel (~2-3s total)

### Current Infrastructure

**Per Replica Capacity:**
- Uvicorn: 4 workers
- Each worker handles async requests
- **Estimated**: 8-12 concurrent requests per replica (with async)

**Current Configuration:**
- Min replicas: 1
- Max replicas: 3
- **Current capacity**: 3 × 8 = **24 concurrent requests**

**Gap Analysis:**
- Required: 600 concurrent requests
- Current: 24 concurrent requests
- **Gap**: 576 requests (need 25x more capacity!)

---

## 🚀 Solution: Multi-Tier Queue System

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Load Balancer                       │
│              (Routes requests to replicas)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │Replica 1│    │Replica 2│    │Replica N│
   │         │    │         │    │         │
   │Uvicorn  │    │Uvicorn  │    │Uvicorn  │
   │4 workers│    │4 workers│    │4 workers│
   │         │    │         │    │         │
   │Queue    │    │Queue    │    │Queue    │
   │(async)  │    │(async)  │    │(async)  │
   └─────────┘    └─────────┘    └─────────┘
```

### Tier 1: FastAPI Async Queue (Per Replica)

**How it works:**
- FastAPI handles requests asynchronously
- Each request is queued in the async event loop
- Uvicorn workers process requests concurrently
- **Capacity per replica**: ~10-15 concurrent requests (async)

**Configuration:**
```python
# executor-service-fastapi.py
# Already using async/await - no changes needed
# Uvicorn handles async requests efficiently
```

### Tier 2: Azure Container Apps Auto-Scaling

**Configuration:**
```terraform
# terraform/main.tf
min_replicas = 20   # Pre-warmed for contest start
max_replicas = 50   # Scale up for peak load

# Auto-scaling rules
scale {
  min_replicas = 20
  max_replicas = 50
  rules {
    http {
      concurrent_requests = 10  # Scale when >10 requests per replica
    }
  }
}
```

**Capacity Calculation:**
- 20 replicas × 10 concurrent = **200 concurrent requests** (pre-warmed)
- 50 replicas × 10 concurrent = **500 concurrent requests** (peak)
- **Target**: 600 requests → Need 60 replicas at peak

---

## 📈 Recommended Configuration

### For 300 Users (600 Concurrent Submissions)

**Option 1: Pre-warm + Auto-scale (Recommended)**
```terraform
min_replicas = 30   # Pre-warmed (30 × 10 = 300 concurrent)
max_replicas = 70   # Peak capacity (70 × 10 = 700 concurrent)
```

**Wait Time Analysis:**
- **30 replicas**: 300 concurrent capacity
- **600 requests**: 300 in queue
- **Wait time**: 300 ÷ 300 × 3s = **3 seconds** ✅
- **With auto-scale to 60 replicas**: **< 1 second** ✅

**Cost (3-hour contest):**
```
Pre-warmed (30 replicas × 3 hours):
  30 × $0.108/hour × 3 = $9.72

Peak (70 replicas × 30 minutes):
  70 × $0.108/hour × 0.5 = $3.78

Average (50 replicas × 2.5 hours):
  50 × $0.108/hour × 2.5 = $13.50
────────────────────────────────────
Total:                            $27.00
```

**Cost per Student**: $27 / 300 = **$0.09 per student**

---

### Option 2: Higher Pre-warm (Lower Wait Time)

```terraform
min_replicas = 50   # Pre-warmed (50 × 10 = 500 concurrent)
max_replicas = 70   # Peak capacity (70 × 10 = 700 concurrent)
```

**Wait Time Analysis:**
- **50 replicas**: 500 concurrent capacity
- **600 requests**: 100 in queue
- **Wait time**: 100 ÷ 500 × 3s = **0.6 seconds** ✅

**Cost (3-hour contest):**
```
Pre-warmed (50 replicas × 3 hours):
  50 × $0.108/hour × 3 = $16.20

Peak (70 replicas × 30 minutes):
  70 × $0.108/hour × 0.5 = $3.78

Average (60 replicas × 2.5 hours):
  60 × $0.108/hour × 2.5 = $16.20
────────────────────────────────────
Total:                            $36.18
```

**Cost per Student**: $36.18 / 300 = **$0.12 per student**

---

## 🔄 User ID and Question ID Tracking

### Current Implementation

**Already Supported:**
- `/submit` endpoint accepts `user_id` and `question_id`
- Results are saved to database with these IDs
- Frontend can track submissions by user/question

**Database Schema:**
```sql
-- submissions table (already exists)
CREATE TABLE submissions (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    question_id VARCHAR(255),
    language VARCHAR(50),
    code TEXT,
    test_results JSONB,
    summary JSONB,
    created_at TIMESTAMP
);
```

### Result Routing

**How it works:**
1. Frontend sends request with `user_id` and `question_id`
2. Backend processes code execution
3. Results saved to database with `user_id` and `question_id`
4. Frontend queries database by `user_id` and `question_id` to retrieve results

**Example Request:**
```json
{
  "language": "cpp",
  "code": "...",
  "test_cases": [...],
  "user_id": "student_123",
  "question_id": "warehouse_box_removal",
  "timeout": 5
}
```

**Example Response:**
```json
{
  "execution_id": "...",
  "summary": {...},
  "test_results": [...],
  "metadata": {
    "submission_id": "...",
    "saved_to_db": true
  }
}
```

---

## ⚡ Performance Optimizations

### 1. Parallel Test Execution (Already Implemented)

- Test cases run in parallel (max 8 concurrent)
- Reduces execution time from 15s → 2-3s
- **Status**: ✅ Deployed

### 2. Async Request Handling

- FastAPI async endpoints
- Non-blocking I/O
- **Status**: ✅ Already implemented

### 3. Database Connection Pooling

- `asyncpg` connection pool (min: 1, max: 10)
- Reuses connections efficiently
- **Status**: ✅ Already implemented

### 4. Auto-Scaling

- Azure Container Apps auto-scales based on load
- Scales up/down automatically
- **Status**: ⚠️ Needs configuration update

---

## 🛠️ Implementation Steps

### Step 1: Fix Current Error ✅
- Fix variable scope issue in parallel execution
- Deploy fix

### Step 2: Update Terraform Configuration
```bash
cd terraform
# Update main.tf with new replica counts
min_replicas = 30
max_replicas = 70
```

### Step 3: Deploy Updated Configuration
```bash
terraform plan
terraform apply
```

### Step 4: Test Load
- Run load test with 300 concurrent users
- Verify wait times < 5 seconds
- Monitor auto-scaling behavior

### Step 5: Monitor and Adjust
- Monitor Azure Container Apps metrics
- Adjust replica counts based on actual load
- Fine-tune auto-scaling rules

---

## 📊 Monitoring and Metrics

### Key Metrics to Monitor

1. **Request Queue Length**
   - Azure Container Apps → Metrics → Request Count
   - Alert if queue > 100 requests

2. **Average Response Time**
   - Target: < 5 seconds
   - Alert if > 10 seconds

3. **Replica Count**
   - Monitor auto-scaling behavior
   - Ensure replicas scale up quickly

4. **Error Rate**
   - Monitor 500 errors
   - Alert if error rate > 1%

### Azure Monitor Queries

```kusto
// Average response time
requests
| where timestamp > ago(1h)
| summarize avg(duration) by bin(timestamp, 1m)

// Request queue length
requests
| where timestamp > ago(1h)
| summarize count() by bin(timestamp, 1m)

// Error rate
requests
| where timestamp > ago(1h)
| summarize error_rate = countif(resultCode >= 500) / count() * 100
```

---

## ✅ Summary

### Recommended Configuration

**For 300 Users (600 Concurrent Submissions):**
- **Min Replicas**: 30 (pre-warmed)
- **Max Replicas**: 70 (peak capacity)
- **Expected Wait Time**: < 3 seconds
- **Cost**: ~$27 for 3-hour contest ($0.09 per student)

### Key Features

1. ✅ **User ID Tracking**: Already implemented in `/submit` endpoint
2. ✅ **Question ID Tracking**: Already implemented in `/submit` endpoint
3. ✅ **Result Routing**: Results saved to database with user/question IDs
4. ✅ **Queue System**: FastAPI async + Azure auto-scaling
5. ✅ **Performance**: Parallel test execution (2-3s per submission)

### Next Steps

1. Fix current error (variable scope)
2. Update Terraform configuration
3. Deploy and test
4. Monitor and adjust

