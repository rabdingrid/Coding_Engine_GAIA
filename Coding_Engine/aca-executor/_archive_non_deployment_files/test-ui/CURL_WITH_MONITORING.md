# Running Curl Commands with Monitoring Dashboard

## Problem
When you run curl commands directly, the results don't appear in the monitoring dashboard because they bypass the frontend storage mechanism.

## Solution
Store the execution results after running curl commands.

---

## Method 1: Store Results Manually (Recommended)

After running a curl command, store the result:

```bash
# Run your curl command and save the response
RESPONSE=$(curl -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"...","test_cases":[...],"user_id":"user_1","question_id":"15"}')

# Store in monitoring dashboard
echo "$RESPONSE" | curl -X POST "http://localhost:3001/api/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @-
```

---

## Method 2: Use Helper Script

1. Make the script executable:
```bash
chmod +x test-ui/store-curl-result.sh
```

2. Run curl and pipe to the script:
```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"...","test_cases":[...],"user_id":"user_1","question_id":"15"}' \
  | ./test-ui/store-curl-result.sh
```

---

## Method 3: One-Liner (Store After Execution)

```bash
# Run and store in one command
RESPONSE=$(curl -s -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"...","test_cases":[...],"user_id":"user_1","question_id":"15"}') && \
echo "$RESPONSE" | curl -s -X POST "http://localhost:3001/api/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @- > /dev/null && \
echo "✅ Stored in monitoring dashboard" && \
echo "$RESPONSE" | python3 -m json.tool
```

---

## Updated 3-User Test Commands (With Monitoring)

### USER 1 - Climbing Stairs (Java)
```bash
RESPONSE=$(curl -s -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"java","code":"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }","test_cases":[{"id":"test_1","input":"2","expected_output":"2"},{"id":"test_2","input":"3","expected_output":"3"},{"id":"test_3","input":"4","expected_output":"5"},{"id":"test_4","input":"5","expected_output":"8"},{"id":"test_5","input":"1","expected_output":"1"}],"user_id":"user_1_climbing_stairs","question_id":"15"}') && \
echo "$RESPONSE" | curl -s -X POST "http://localhost:3001/api/monitoring/store" -H "Content-Type: application/json" -d @- > /dev/null && \
echo "✅ User 1 - Stored" && echo "$RESPONSE" | python3 -m json.tool | head -20
```

### USER 2 - Two Sum (Python)
```bash
RESPONSE=$(curl -s -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"nums = list(map(int, input().split()))\ntarget = int(input())\nfor i in range(len(nums)):\n    for j in range(i+1, len(nums)):\n        if nums[i] + nums[j] == target:\n            print(\"[\" + str(i) + \",\" + str(j) + \"]\")\n            exit()\nprint(\"[]\")","test_cases":[{"id":"test_1","input":"2 7 11 15\n9","expected_output":"[0,1]"},{"id":"test_2","input":"3 2 4\n6","expected_output":"[1,2]"},{"id":"test_3","input":"3 3\n6","expected_output":"[0,1]"}],"user_id":"user_2_two_sum","question_id":"1"}') && \
echo "$RESPONSE" | curl -s -X POST "http://localhost:3001/api/monitoring/store" -H "Content-Type: application/json" -d @- > /dev/null && \
echo "✅ User 2 - Stored" && echo "$RESPONSE" | python3 -m json.tool | head -20
```

### USER 3 - Maximum Subarray (JavaScript)
```bash
RESPONSE=$(curl -s -X POST "https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"javascript","code":"const readline = require(\"readline\");\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nrl.on(\"line\", (line) => {\n  const nums = JSON.parse(line.trim());\n  let maxSum = nums[0];\n  let currentSum = nums[0];\n  for (let i = 1; i < nums.length; i++) {\n    currentSum = Math.max(nums[i], currentSum + nums[i]);\n    maxSum = Math.max(maxSum, currentSum);\n  }\n  console.log(maxSum);\n  rl.close();\n});","test_cases":[{"id":"test_1","input":"[-2,1,-3,4,-1,2,1,-5,4]","expected_output":"6"},{"id":"test_2","input":"[1]","expected_output":"1"},{"id":"test_3","input":"[5,4,-1,7,8]","expected_output":"23"},{"id":"test_4","input":"[-1]","expected_output":"-1"}],"user_id":"user_3_max_subarray","question_id":"2"}') && \
echo "$RESPONSE" | curl -s -X POST "http://localhost:3001/api/monitoring/store" -H "Content-Type: application/json" -d @- > /dev/null && \
echo "✅ User 3 - Stored" && echo "$RESPONSE" | python3 -m json.tool | head -20
```

---

## Important Notes

1. **Node.js Server Must Be Running**: The monitoring dashboard requires the Node.js server (`npm start` in `test-ui/`) to be running on `http://localhost:3001`

2. **Auto-Refresh**: The monitoring dashboard auto-refreshes every 5 seconds, so stored results will appear automatically

3. **Latest Results First**: Results are sorted by timestamp (newest first) so latest executions appear at the top

4. **No Duplicates**: The same execution won't be stored twice (based on execution_id)

---

## Troubleshooting

- **Dashboard shows old data**: Click "🔄 Refresh" button or wait 5 seconds for auto-refresh
- **Results not appearing**: Check that Node.js server is running: `cd test-ui && npm start`
- **Storage fails**: Check server logs for errors


