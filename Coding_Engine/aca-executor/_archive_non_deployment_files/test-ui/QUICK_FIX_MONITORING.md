# Quick Fix: See Your Curl Results in Monitoring Dashboard

## Problem
You ran a curl command but it's not showing in the monitoring dashboard.

## Solution
The monitoring dashboard only shows results that are **stored** in the Node.js server. Curl commands don't automatically store results.

---

## ✅ **Easiest Solution: Use Helper Script**

### **Option 1: Quick Test Script** (Recommended)
```bash
cd /Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/test-ui
./quick-test-with-monitoring.sh
```

This will:
1. Run a test
2. Show the result
3. **Automatically store it in monitoring dashboard**

---

### **Option 2: Wrapper Script for Any Curl Command**
```bash
cd /Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/test-ui

# Use your existing curl command, but wrap it:
./run-and-monitor.sh -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"...","test_cases":[...],"user_id":"user_1","question_id":"15"}'
```

---

## 🔧 **Manual Solution** (If Scripts Don't Work)

After running your curl command, store the result:

```bash
# 1. Run your curl command and save response
RESPONSE=$(curl -s -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"...","test_cases":[...],"user_id":"user_1","question_id":"15"}')

# 2. Store in monitoring dashboard
echo "$RESPONSE" | curl -s -X POST "http://localhost:3001/api/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @-

# 3. Verify it was stored
echo "✅ Stored! Open monitoring-dashboard.html to see it"
```

---

## ⚠️ **Important: Node.js Server Must Be Running**

The monitoring dashboard requires the Node.js server to be running:

```bash
cd /Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/test-ui
npm start
```

**Check if it's running:**
```bash
curl http://localhost:3001/api/monitoring/executions
```

If you get a response, the server is running. If not, start it with `npm start`.

---

## 📊 **View Results**

1. **Open** `monitoring-dashboard.html` in your browser
2. **Wait 5 seconds** (auto-refresh) OR click "🔄 Refresh"
3. **Your result should appear** at the top (newest first)

---

## 🎯 **For Your 3-User Test**

If you want all 3 users' results to appear in monitoring:

```bash
cd /Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/test-ui

# User 1
RESPONSE1=$(curl -s -X POST "https://..." -d '...') && \
echo "$RESPONSE1" | curl -s -X POST "http://localhost:3001/api/monitoring/store" -H "Content-Type: application/json" -d @-

# User 2  
RESPONSE2=$(curl -s -X POST "https://..." -d '...') && \
echo "$RESPONSE2" | curl -s -X POST "http://localhost:3001/api/monitoring/store" -H "Content-Type: application/json" -d @-

# User 3
RESPONSE3=$(curl -s -X POST "https://..." -d '...') && \
echo "$RESPONSE3" | curl -s -X POST "http://localhost:3001/api/monitoring/store" -H "Content-Type: application/json" -d @-
```

Then refresh the monitoring dashboard!

---

**That's it! Your curl results will now appear in the monitoring dashboard.** 🎉


