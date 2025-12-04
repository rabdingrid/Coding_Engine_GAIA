# Queue Test - 1 Replica with Gunicorn

## 🧪 **Test Scenario**

**Configuration:**
- **Replicas**: 1 (all requests hit the same replica)
- **Server**: Gunicorn (4 workers × 2 threads = 8 concurrent capacity)
- **Test**: 3 concurrent requests from 3 different systems

**Expected Result:**
- ✅ All 3 requests should complete successfully
- ✅ No hanging (Gunicorn handles queue properly)
- ✅ All requests processed by the same replica
- ✅ Same container_id for all 3 requests

---

## 📋 **Curl Commands**

### **USER 1 - Climbing Stairs (Java)**
```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000022.happypond-428960e8.eastus2.azurecontainerapps.io/execute" -H "Content-Type: application/json" -d '{"language":"java","code":"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }","test_cases":[{"id":"test_1","input":"2","expected_output":"2"},{"id":"test_2","input":"3","expected_output":"3"},{"id":"test_3","input":"4","expected_output":"5"}],"user_id":"user_1_test","question_id":"15"}'
```

### **USER 2 - Two Sum (Python)**
```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000022.happypond-428960e8.eastus2.azurecontainerapps.io/execute" -H "Content-Type: application/json" -d '{"language":"python","code":"nums = list(map(int, input().split()))\ntarget = int(input())\nfor i in range(len(nums)):\n    for j in range(i+1, len(nums)):\n        if nums[i] + nums[j] == target:\n            print(\"[\" + str(i) + \",\" + str(j) + \"]\")\n            exit()\nprint(\"[]\")","test_cases":[{"id":"test_1","input":"2 7 11 15\n9","expected_output":"[0,1]"},{"id":"test_2","input":"3 2 4\n6","expected_output":"[1,2]"}],"user_id":"user_2_test","question_id":"1"}'
```

### **USER 3 - Maximum Subarray (JavaScript)**
```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000022.happypond-428960e8.eastus2.azurecontainerapps.io/execute" -H "Content-Type: application/json" -d '{"language":"javascript","code":"const readline = require(\"readline\");\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nrl.on(\"line\", (line) => {\n  const nums = JSON.parse(line.trim());\n  let maxSum = nums[0];\n  let currentSum = nums[0];\n  for (let i = 1; i < nums.length; i++) {\n    currentSum = Math.max(nums[i], currentSum + nums[i]);\n    maxSum = Math.max(maxSum, currentSum);\n  }\n  console.log(maxSum);\n  rl.close();\n});","test_cases":[{"id":"test_1","input":"[-2,1,-3,4,-1,2,1,-5,4]","expected_output":"6"},{"id":"test_2","input":"[1]","expected_output":"1"}],"user_id":"user_3_test","question_id":"2"}'
```

---

## ✅ **What to Verify**

### **1. All Requests Complete**
- ✅ All 3 return HTTP 200 OK
- ✅ All return `"all_passed": true`
- ✅ No timeouts or errors

### **2. Same Container ID**
- ✅ All 3 requests should have the **same container_id**
- ✅ This proves they all hit the same replica
- ✅ Example: `ai-ta-ra-code-executor2--0000022-xxx-xxxxx`

### **3. No Hanging**
- ✅ All requests complete within reasonable time
- ✅ No need for Ctrl+C
- ✅ Gunicorn queue handling works properly

### **4. Concurrent Processing**
- ✅ Requests processed concurrently (not sequentially)
- ✅ Check timestamps in logs - should overlap
- ✅ Python (fast) may complete before Java (slow)

---

## 📊 **Comparison: Before vs After**

### **Before (Flask Dev Server, 1 Replica):**
- ❌ Request 1: ✅ Executed
- ❌ Request 2: ✅ Executed (but queued)
- ❌ Request 3: ❌ **HUNG** (queue broke)

### **After (Gunicorn, 1 Replica):**
- ✅ Request 1: ✅ Executed
- ✅ Request 2: ✅ Executed (concurrently)
- ✅ Request 3: ✅ **Executed** (concurrently, no hanging!)

---

## 🎯 **Expected Timeline**

```
T=0s:  All 3 requests arrive simultaneously
T=0s:  Request 1 (Java) → Worker 1 → Processing (~3s)
T=0s:  Request 2 (Python) → Worker 2 → Processing (~0.05s)
T=0s:  Request 3 (JavaScript) → Worker 3 → Processing (~0.1s)
T=0.05s: Request 2 completes ✅
T=0.1s: Request 3 completes ✅
T=3s: Request 1 completes ✅
```

**All complete successfully, no hanging!**

---

## 📝 **Test Results**

After running all 3 commands simultaneously, check:

1. **All 3 completed?** ✅ / ❌
2. **Same container_id?** ✅ / ❌
3. **No hanging?** ✅ / ❌
4. **All passed tests?** ✅ / ❌

**If all ✅ → Gunicorn queue system is working perfectly!** 🎉


