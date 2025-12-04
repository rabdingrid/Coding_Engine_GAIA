#!/bin/bash

# Test script for "Longest Substring Without Repeating Characters" DSA problem
# Classic sliding window problem with 10 test cases (last one is large)

CONTAINER_APP_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$CONTAINER_APP_URL" ]; then
    echo "❌ Error: Could not fetch Container App URL"
    exit 1
fi

echo "🧪 Testing: Longest Substring Without Repeating Characters"
echo "📍 URL: $CONTAINER_APP_URL"
echo "📊 Test Cases: 10 (with large final test case)"
echo ""

# Create JSON payload file
cat > /tmp/test_substring_payload.json << 'PAYLOAD_EOF'
{
  "language": "python",
  "code": "def lengthOfLongestSubstring(s):\n    if not s:\n        return 0\n    \n    char_map = {}\n    max_len = 0\n    start = 0\n    \n    for end in range(len(s)):\n        if s[end] in char_map and char_map[s[end]] >= start:\n            start = char_map[s[end]] + 1\n        \n        char_map[s[end]] = end\n        max_len = max(max_len, end - start + 1)\n    \n    return max_len\n\ntry:\n    s = input()\n    if s is None:\n        s = \"\"\nexcept EOFError:\n    s = \"\"\nprint(lengthOfLongestSubstring(s))",
  "test_cases": [
    {
      "id": "test_1",
      "input": "abcabcbb",
      "expected_output": "3"
    },
    {
      "id": "test_2",
      "input": "bbbbb",
      "expected_output": "1"
    },
    {
      "id": "test_3",
      "input": "pwwkew",
      "expected_output": "3"
    },
    {
      "id": "test_4",
      "input": "",
      "expected_output": "0"
    },
    {
      "id": "test_5",
      "input": " ",
      "expected_output": "1"
    },
    {
      "id": "test_6",
      "input": "dvdf",
      "expected_output": "3"
    },
    {
      "id": "test_7",
      "input": "abba",
      "expected_output": "2"
    },
    {
      "id": "test_8",
      "input": "tmmzuxt",
      "expected_output": "5"
    },
    {
      "id": "test_9",
      "input": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
      "expected_output": "62"
    },
    {
      "id": "test_10",
      "input": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`",
      "expected_output": "91"
    }
  ],
  "user_id": "test_longest_substring",
  "question_id": "leetcode_3"
}
PAYLOAD_EOF

echo "📤 Sending request..."
START_TIME=$(date +%s)
RESPONSE=$(curl -s -m 60 -X POST "$CONTAINER_APP_URL/execute" \
  -H "Content-Type: application/json" \
  -d @/tmp/test_substring_payload.json)
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

# Save response
echo "$RESPONSE" > /tmp/test_substring_response.json

# Parse and display results
python3 << 'PYEOF'
import json
import sys

try:
    with open('/tmp/test_substring_response.json', 'r') as f:
        d = json.load(f)
    
    print("📊 Test Results:")
    print("=" * 70)
    
    summary = d.get('summary', {})
    metadata = d.get('metadata', {})
    
    status = "✅ All Passed!" if summary.get('all_passed') else "❌ Some Failed"
    print(f"Status: {status}")
    print(f"Passed: {summary.get('passed', 0)}/{summary.get('total_tests', 0)}")
    print(f"Pass Rate: {summary.get('pass_percentage', 0):.1f}%")
    print(f"Total Execution Time: {metadata.get('execution_time_ms', 0)}ms")
    print(f"Container ID: {metadata.get('container_id', 'unknown')}")
    print(f"CPU Usage: {metadata.get('cpu_usage_percent', 0):.1f}%")
    print(f"Memory Usage: {metadata.get('memory_usage_mb', 0):.1f} MB")
    
    print("\n📋 Individual Test Results:")
    print("-" * 70)
    
    test_results = d.get('test_results', [])
    for i, t in enumerate(test_results, 1):
        status_icon = "✅" if t.get('passed') else "❌"
        expected = t.get('expected_output', '').strip()
        actual = t.get('actual_output', '').strip() if t.get('actual_output') else "N/A"
        error = t.get('error', '')
        exec_time = t.get('execution_time_ms', 0)
        input_data = t.get('input', '')
        
        # Truncate long inputs for display
        if len(input_data) > 50:
            input_display = input_data[:47] + "..."
        else:
            input_display = input_data
        
        print(f"\nTest {i}: {status_icon}")
        print(f"  Input: {input_display}")
        print(f"  Expected: {expected}")
        print(f"  Got: {actual}")
        print(f"  Time: {exec_time}ms")
        if error:
            print(f"  Error: {error[:200]}")
        
        # Highlight large test case
        if i == 10:
            print(f"  📌 Large Test Case: {len(input_data)} characters")
    
    print("\n" + "=" * 70)
    if summary.get('all_passed'):
        print("✅ SUCCESS: All 10 tests passed!")
        print("🎯 System handled large test case successfully!")
    else:
        print("❌ FAILURE: Some tests failed")
        failed_tests = [i+1 for i, t in enumerate(test_results) if not t.get('passed')]
        print(f"   Failed tests: {failed_tests}")
        sys.exit(1)
        
except json.JSONDecodeError as e:
    print(f"❌ JSON Parse Error: {e}")
    with open('/tmp/test_substring_response.json', 'r') as f:
        content = f.read()
        print(f"\nRaw Response (first 500 chars):")
        print(content[:500])
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

EXIT_CODE=$?

echo ""
echo "⏱️  Total Request Time: ${TOTAL_TIME}s"

# Cleanup
rm -f /tmp/test_substring_payload.json /tmp/test_substring_response.json

exit $EXIT_CODE

