# Testing Guide - User ID & Monitoring

## ✅ Deployment Complete

**Executor Service:**
- ✅ Deployed: `executor-secure:v4` (with monitoring)
- ✅ URL: `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io`
- ✅ Status: Healthy

**Frontend:**
- ✅ Running: `http://localhost:3001`
- ✅ User ID: Auto-generated per browser

---

## 🧪 Test Scenario 1: Your Browser

1. **Open:** `http://localhost:3001`
2. **Check:** Top-right corner shows your User ID (e.g., `user_1732800000_abc123`)
3. **Select:** A question from sidebar
4. **Write Code:**
   ```python
   a = int(input())
   b = int(input())
   print(a + b)
   ```
5. **Run Code:** Click "▶ Run Code"
6. **Check Results:** Should show test results

**What to Verify:**
- ✅ User ID displayed in top-right
- ✅ Code executes successfully
- ✅ Results show pass/fail

---

## 🧪 Test Scenario 2: Friend's Browser

1. **Friend Opens:** `http://localhost:3001` (or deployed URL)
2. **Friend Gets:** Different User ID (e.g., `user_1732800001_xyz789`)
3. **Friend Submits:** Code
4. **Check Monitoring:** Should see different user_id

**What to Verify:**
- ✅ Friend has different User ID
- ✅ Monitoring shows both user IDs separately
- ✅ Each submission tracked independently

---

## 📊 View Monitoring

### Option 1: Local Dashboard
1. Open: `http://localhost:3001/monitoring-dashboard.html`
2. See: All executions with user_id, container_id, execution_time

### Option 2: Azure Monitor
1. Go to: Azure Portal
2. Navigate to: `ai-ta-ra-code-executor2` Container App
3. Click: "Log stream" or "Monitoring"
4. Search for: `execution_started` or `execution_completed`
5. Filter by: `user_id` in logs

---

## 🔍 What to Check in Logs

**Each execution logs:**
```json
{
  "event": "execution_started",
  "user_id": "user_1732800000_abc123",
  "question_id": "1",
  "container_id": "container-name",
  "replica_name": "replica-name",
  "language": "python",
  "timestamp": "2025-11-28T..."
}
```

**Completion log:**
```json
{
  "event": "execution_completed",
  "user_id": "user_1732800000_abc123",
  "execution_time_ms": 320,
  "tests_passed": 3,
  "tests_total": 3,
  "all_passed": true
}
```

---

## ✅ Expected Results

### Your Browser:
- User ID: `user_1732800000_abc123` (example)
- Submissions tracked with this ID

### Friend's Browser:
- User ID: `user_1732800001_xyz789` (different)
- Submissions tracked with different ID

### Monitoring:
- Shows both user IDs separately
- Can filter by user_id
- Each execution shows container_id, execution_time_ms

---

## 🐛 Troubleshooting

### User ID Not Showing?
- Check browser console for errors
- Clear localStorage and refresh
- Check if `getUserId()` function exists

### Same User ID for Both?
- Each browser should have different localStorage
- Try "New ID" button to generate new one
- Check if localStorage is working

### Monitoring Not Showing?
- Check Azure Portal → Logs
- Wait 30 seconds for deployment to propagate
- Check executor service is v4

---

## 📋 Quick Test Commands

```bash
# Test executor health
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Test execution with user_id
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [{"id": "test_1", "input": "", "expected_output": "42"}],
    "user_id": "test_user_123",
    "question_id": "1"
  }'
```

---

**Status:** ✅ Ready to Test!
