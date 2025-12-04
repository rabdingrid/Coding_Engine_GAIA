#!/bin/bash

# Quick test script - 5 curl commands for testing the code executor

URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$URL" ]; then
    URL="https://ai-ta-ra-code-executor2--0000025.happypond-428960e8.eastus2.azurecontainerapps.io"
fi

echo "🧪 Testing Code Executor - 5 Different Scenarios"
echo "📍 URL: $URL"
echo ""

# Test 1: Python - Simple Addition
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1: Python - Simple Addition"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "a = int(input())\nb = int(input())\nprint(a + b)",
    "test_cases": [
      {"id": "test_1", "input": "5\n3", "expected_output": "8"},
      {"id": "test_2", "input": "10\n20", "expected_output": "30"},
      {"id": "test_3", "input": "-5\n5", "expected_output": "0"}
    ],
    "user_id": "test_user_1",
    "question_id": "test_1"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('✅' if d.get('summary', {}).get('all_passed') else '❌', f\"Passed: {d.get('summary', {}).get('passed', 0)}/{d.get('summary', {}).get('total_tests', 0)}\", f\"Time: {d.get('metadata', {}).get('execution_time_ms', 0)}ms\")"
echo ""

# Test 2: Java - Climbing Stairs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2: Java - Climbing Stairs (Fibonacci)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "java",
    "code": "public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }",
    "test_cases": [
      {"id": "test_1", "input": "2", "expected_output": "2"},
      {"id": "test_2", "input": "3", "expected_output": "3"},
      {"id": "test_3", "input": "4", "expected_output": "5"}
    ],
    "user_id": "test_user_2",
    "question_id": "15"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('✅' if d.get('summary', {}).get('all_passed') else '❌', f\"Passed: {d.get('summary', {}).get('passed', 0)}/{d.get('summary', {}).get('total_tests', 0)}\", f\"Time: {d.get('metadata', {}).get('execution_time_ms', 0)}ms\")"
echo ""

# Test 3: JavaScript - Maximum Subarray
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3: JavaScript - Maximum Subarray (Kadane'\''s Algorithm)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "code": "const readline = require(\"readline\");\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nrl.on(\"line\", (line) => {\n  const nums = JSON.parse(line.trim());\n  let maxSum = nums[0];\n  let currentSum = nums[0];\n  for (let i = 1; i < nums.length; i++) {\n    currentSum = Math.max(nums[i], currentSum + nums[i]);\n    maxSum = Math.max(maxSum, currentSum);\n  }\n  console.log(maxSum);\n  rl.close();\n});",
    "test_cases": [
      {"id": "test_1", "input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"},
      {"id": "test_2", "input": "[1]", "expected_output": "1"},
      {"id": "test_3", "input": "[5,4,-1,7,8]", "expected_output": "23"}
    ],
    "user_id": "test_user_3",
    "question_id": "2"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('✅' if d.get('summary', {}).get('all_passed') else '❌', f\"Passed: {d.get('summary', {}).get('passed', 0)}/{d.get('summary', {}).get('total_tests', 0)}\", f\"Time: {d.get('metadata', {}).get('execution_time_ms', 0)}ms\")"
echo ""

# Test 4: C++ - Two Sum
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4: C++ - Two Sum Problem"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <bits/stdc++.h>\nusing namespace std;\nint main() {\n  vector<int> nums;\n  int num;\n  while (cin >> num) {\n    nums.push_back(num);\n  }\n  int target = nums.back();\n  nums.pop_back();\n  for (int i = 0; i < nums.size(); i++) {\n    for (int j = i + 1; j < nums.size(); j++) {\n      if (nums[i] + nums[j] == target) {\n        cout << \"[\" << i << \",\" << j << \"]\" << endl;\n        return 0;\n      }\n    }\n  }\n  cout << \"[]\" << endl;\n  return 0;\n}",
    "test_cases": [
      {"id": "test_1", "input": "2 7 11 15 9", "expected_output": "[0,1]"},
      {"id": "test_2", "input": "3 2 4 6", "expected_output": "[1,2]"},
      {"id": "test_3", "input": "3 3 6", "expected_output": "[0,1]"}
    ],
    "user_id": "test_user_4",
    "question_id": "1"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('✅' if d.get('summary', {}).get('all_passed') else '❌', f\"Passed: {d.get('summary', {}).get('passed', 0)}/{d.get('summary', {}).get('total_tests', 0)}\", f\"Time: {d.get('metadata', {}).get('execution_time_ms', 0)}ms\")"
echo ""

# Test 5: Python - Longest Substring
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 5: Python - Longest Substring Without Repeating Characters"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X POST "$URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def lengthOfLongestSubstring(s):\n    if not s:\n        return 0\n    char_map = {}\n    max_len = 0\n    start = 0\n    for end in range(len(s)):\n        if s[end] in char_map and char_map[s[end]] >= start:\n            start = char_map[s[end]] + 1\n        char_map[s[end]] = end\n        max_len = max(max_len, end - start + 1)\n    return max_len\n\ntry:\n    s = input()\n    if s is None:\n        s = \"\"\nexcept EOFError:\n    s = \"\"\nprint(lengthOfLongestSubstring(s))",
    "test_cases": [
      {"id": "test_1", "input": "abcabcbb", "expected_output": "3"},
      {"id": "test_2", "input": "bbbbb", "expected_output": "1"},
      {"id": "test_3", "input": "pwwkew", "expected_output": "3"},
      {"id": "test_4", "input": "", "expected_output": "0"},
      {"id": "test_5", "input": " ", "expected_output": "1"}
    ],
    "user_id": "test_user_5",
    "question_id": "leetcode_3"
  }' | python3 -c "import sys, json; d=json.load(sys.stdin); print('✅' if d.get('summary', {}).get('all_passed') else '❌', f\"Passed: {d.get('summary', {}).get('passed', 0)}/{d.get('summary', {}).get('total_tests', 0)}\", f\"Time: {d.get('metadata', {}).get('execution_time_ms', 0)}ms\")"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All 5 tests completed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


