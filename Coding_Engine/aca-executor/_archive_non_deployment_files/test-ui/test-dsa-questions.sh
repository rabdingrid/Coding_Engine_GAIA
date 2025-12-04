#!/bin/bash

# Test script for DSA questions
# Tests various question types to ensure they work correctly

# Get the latest executor URL dynamically
EXECUTOR_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')
if [ -z "$EXECUTOR_URL" ]; then
  EXECUTOR_URL="https://ai-ta-ra-code-executor2--0000010.happypond-428960e8.eastus2.azurecontainerapps.io"
fi

echo "🧪 Testing DSA Questions on Executor"
echo "===================================="
echo "Executor URL: $EXECUTOR_URL"
echo ""

# Test 1: Array - Maximum Subarray
echo "📊 Test 1: Maximum Subarray (Array)"
echo "-----------------------------------"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(nums):\n    max_sum = current_sum = nums[0]\n    for num in nums[1:]:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum\n\nimport sys\nimport json\nnums = json.loads(sys.stdin.read())\nprint(solve(nums))",
    "test_cases": [
      {"id": "test_1", "input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"},
      {"id": "test_2", "input": "[1]", "expected_output": "1"}
    ],
    "user_id": "test_user",
    "question_id": "2"
  }' | python3 -m json.tool | head -30
echo ""

# Test 2: Stack - Valid Parentheses
echo "📚 Test 2: Valid Parentheses (Stack)"
echo "-----------------------------------"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(s):\n    stack = []\n    pairs = {\")\": \"(\", \"}\": \"{\", \"]\": \"[\"}\n    for char in s:\n        if char in pairs:\n            if not stack or stack.pop() != pairs[char]:\n                return False\n        else:\n            stack.append(char)\n    return len(stack) == 0\n\nimport sys\ns = sys.stdin.read().strip().strip(\"\\\"\")\nprint(str(solve(s)).lower())",
    "test_cases": [
      {"id": "test_1", "input": "\"()\"", "expected_output": "true"},
      {"id": "test_2", "input": "\"()[]{}\"", "expected_output": "true"},
      {"id": "test_3", "input": "\"(]\"", "expected_output": "false"}
    ],
    "user_id": "test_user",
    "question_id": "6"
  }' | python3 -m json.tool | head -30
echo ""

# Test 3: DP - Climbing Stairs
echo "💡 Test 3: Climbing Stairs (DP)"
echo "--------------------------------"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for i in range(3, n + 1):\n        a, b = b, a + b\n    return b\n\nimport sys\nn = int(sys.stdin.read().strip())\nprint(solve(n))",
    "test_cases": [
      {"id": "test_1", "input": "2", "expected_output": "2"},
      {"id": "test_2", "input": "3", "expected_output": "3"},
      {"id": "test_3", "input": "4", "expected_output": "5"}
    ],
    "user_id": "test_user",
    "question_id": "15"
  }' | python3 -m json.tool | head -30
echo ""

# Test 4: String - Longest Substring Without Repeating Characters
echo "📝 Test 4: Longest Substring Without Repeating Characters (String)"
echo "-------------------------------------------------------------------"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(s):\n    char_set = set()\n    left = 0\n    max_len = 0\n    for right in range(len(s)):\n        while s[right] in char_set:\n            char_set.remove(s[left])\n            left += 1\n        char_set.add(s[right])\n        max_len = max(max_len, right - left + 1)\n    return max_len\n\nimport sys\ns = sys.stdin.read().strip().strip(\"\\\"\")\nprint(solve(s))",
    "test_cases": [
      {"id": "test_1", "input": "\"abcabcbb\"", "expected_output": "3"},
      {"id": "test_2", "input": "\"bbbbb\"", "expected_output": "1"},
      {"id": "test_3", "input": "\"pwwkew\"", "expected_output": "3"}
    ],
    "user_id": "test_user",
    "question_id": "10"
  }' | python3 -m json.tool | head -30
echo ""

# Test 5: Tree - Maximum Depth of Binary Tree
echo "🌳 Test 5: Maximum Depth of Binary Tree (Tree)"
echo "-----------------------------------------------"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(arr):\n    if not arr or arr[0] is None:\n        return 0\n    def depth(index):\n        if index >= len(arr) or arr[index] is None:\n            return 0\n        left = depth(2 * index + 1)\n        right = depth(2 * index + 2)\n        return 1 + max(left, right)\n    return depth(0)\n\nimport sys\nimport json\narr = json.loads(sys.stdin.read())\nprint(solve(arr))",
    "test_cases": [
      {"id": "test_1", "input": "[3,9,20,null,null,15,7]", "expected_output": "3"},
      {"id": "test_2", "input": "[1,null,2]", "expected_output": "2"},
      {"id": "test_3", "input": "[]", "expected_output": "0"}
    ],
    "user_id": "test_user",
    "question_id": "11"
  }' | python3 -m json.tool | head -30
echo ""

echo "✅ Testing complete!"
echo ""
echo "📊 Summary:"
echo "   • Tested 5 different question categories"
echo "   • All tests should show 'all_passed: true' if working correctly"
echo ""
echo "🔍 Check the output above for:"
echo "   • summary.all_passed: true"
echo "   • test_results[].passed: true"
echo "   • No errors in execution"

