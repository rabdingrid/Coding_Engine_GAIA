#!/bin/bash

# Quick test script - tests one question at a time (faster)

# Get the latest executor URL dynamically
EXECUTOR_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')
if [ -z "$EXECUTOR_URL" ]; then
  EXECUTOR_URL="https://ai-ta-ra-code-executor2--0000010.happypond-428960e8.eastus2.azurecontainerapps.io"
fi

echo "🧪 Quick Test - DSA Questions"
echo "=============================="
echo "Executor URL: $EXECUTOR_URL"
echo ""

# Test 1: Array - Maximum Subarray (Simple)
echo "📊 Test 1: Maximum Subarray"
echo "---------------------------"
RESPONSE=$(curl -s -m 20 -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(nums):\n    max_sum = current_sum = nums[0]\n    for num in nums[1:]:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum\n\nimport sys\nimport json\nnums = json.loads(sys.stdin.read())\nprint(solve(nums))",
    "test_cases": [
      {"id": "test_1", "input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"}
    ],
    "user_id": "test_user",
    "question_id": "2"
  }')

if echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); exit(0 if d.get('summary', {}).get('all_passed') else 1)" 2>/dev/null; then
  echo "✅ PASSED"
else
  echo "❌ FAILED"
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -10
fi
echo ""

# Test 2: Stack - Valid Parentheses
echo "📚 Test 2: Valid Parentheses"
echo "----------------------------"
RESPONSE=$(curl -s -m 20 -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(s):\n    stack = []\n    pairs = {\")\": \"(\", \"}\": \"{\", \"]\": \"[\"}\n    for char in s:\n        if char in pairs:\n            if not stack or stack.pop() != pairs[char]:\n                return False\n        else:\n            stack.append(char)\n    return len(stack) == 0\n\nimport sys\ns = sys.stdin.read().strip().strip(\"\\\"\")\nprint(str(solve(s)).lower())",
    "test_cases": [
      {"id": "test_1", "input": "\"()\"", "expected_output": "true"}
    ],
    "user_id": "test_user",
    "question_id": "6"
  }')

if echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); exit(0 if d.get('summary', {}).get('all_passed') else 1)" 2>/dev/null; then
  echo "✅ PASSED"
else
  echo "❌ FAILED"
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -10
fi
echo ""

# Test 3: DP - Climbing Stairs
echo "💡 Test 3: Climbing Stairs"
echo "--------------------------"
RESPONSE=$(curl -s -m 20 -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for i in range(3, n + 1):\n        a, b = b, a + b\n    return b\n\nimport sys\nn = int(sys.stdin.read().strip())\nprint(solve(n))",
    "test_cases": [
      {"id": "test_1", "input": "3", "expected_output": "3"}
    ],
    "user_id": "test_user",
    "question_id": "15"
  }')

if echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); exit(0 if d.get('summary', {}).get('all_passed') else 1)" 2>/dev/null; then
  echo "✅ PASSED"
else
  echo "❌ FAILED"
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -10
fi
echo ""

echo "✅ Quick test complete!"
echo ""
echo "💡 Tip: First request may take 10-30 seconds (cold start)"
echo "   Subsequent requests are much faster (20-100ms)"


