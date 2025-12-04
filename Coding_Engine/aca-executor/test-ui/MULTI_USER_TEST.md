# Multi-User Test - Climbing Stairs Question

## 🚀 **System Status**
- **Scaled to**: 1 replica (ready for testing)
- **URL**: `https://ai-ta-ra-code-executor2--0000020.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Test**: Can 1 container handle multiple concurrent users?

---

## 📋 **Easy Copy-Paste Commands**

### **For Your System:**
```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000020.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }","test_cases":[{"id":"test_1","input":"2","expected_output":"2"},{"id":"test_2","input":"3","expected_output":"3"},{"id":"test_3","input":"4","expected_output":"5"},{"id":"test_4","input":"5","expected_output":"8"},{"id":"test_5","input":"1","expected_output":"1"}],"user_id":"user_your_system","question_id":"15"}'
```

### **For Your Friend's System:**
```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000020.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }","test_cases":[{"id":"test_1","input":"2","expected_output":"2"},{"id":"test_2","input":"3","expected_output":"3"},{"id":"test_3","input":"4","expected_output":"5"},{"id":"test_4","input":"5","expected_output":"8"},{"id":"test_5","input":"1","expected_output":"1"}],"user_id":"user_friend_system","question_id":"15"}'
```

---

## 🧪 **How to Test**

1. **Copy the first command** → Run on your system
2. **Copy the second command** → Send to your friend
3. **Run both at the same time** (or within 1-2 seconds)
4. **Check the results:**
   - Both should return `"all_passed": true`
   - Check `container_id` in response - should be the same (1 container handling both)
   - Check execution times - should be similar

---

## 📊 **What to Look For**

### **Success Indicators:**
- ✅ Both requests complete successfully
- ✅ Same `container_id` in both responses (proves 1 container handled both)
- ✅ Execution times are reasonable (~500-2000ms)
- ✅ All test cases pass for both users

### **If Issues:**
- ⚠️ Different `container_id` = Auto-scaled to 2 containers (still OK, but not testing 1 container)
- ⚠️ Timeout = Container overloaded (may need more replicas)
- ⚠️ Error = Check the error message

---

## 🔍 **Expected Response Format**

```json
{
  "summary": {
    "all_passed": true,
    "passed": 5,
    "total_tests": 5
  },
  "metadata": {
    "container_id": "ai-ta-ra-code-executor2--0000020-xxx",
    "execution_time_ms": 1234,
    "cpu_usage_percent": 15.5,
    "memory_usage_mb": 45.2
  },
  "test_results": [...]
}
```

**Key Field**: `metadata.container_id` - Should be the same for both users if 1 container handled both.

---

## 💡 **Alternative: Use Test Scripts**

### **Option 1: Simple Test**
```bash
cd /Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/test-ui
./test-climbing-stairs.sh
```

### **Option 2: Concurrent Test (5 users at once)**
```bash
cd /Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/test-ui
./test-concurrent.sh
```

---

**Ready to test!** Run both commands simultaneously and check if 1 container can handle multiple users. 🚀


