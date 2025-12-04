#!/bin/bash

# Test script for C++ "Total Weight of Cans" problem

CONTAINER_APP_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$CONTAINER_APP_URL" ]; then
    echo "❌ Error: Could not fetch Container App URL"
    exit 1
fi

echo "🧪 Testing C++ Total Weight of Cans Problem"
echo "📍 URL: $CONTAINER_APP_URL"
echo ""

# Create JSON payload file
cat > /tmp/test_cpp_payload.json << 'PAYLOAD_EOF'
{
  "language": "cpp",
  "code": "#include <bits/stdc++.h>\n\nusing namespace std;\n\nstring ltrim(const string &);\nstring rtrim(const string &);\n\nint findTotalWeight(vector<int> cans) {\n    int total = 0;\n    while (!cans.empty()) {\n        // Find the minimum weight and its index\n        int minWeight = cans[0];\n        int minIndex = 0;\n        for (int i = 1; i < cans.size(); i++) {\n            if (cans[i] < minWeight) {\n                minWeight = cans[i];\n                minIndex = i;\n            }\n        }\n        // Add the minimum weight to total\n        total += minWeight;\n        // Determine the range to remove\n        // Remove the minimum can and its two adjacent cans (or fewer if at edge)\n        int startIdx = max(0, minIndex - 1);\n        int endIdx = min((int)cans.size() - 1, minIndex + 1);\n        // Remove elements from end to start to maintain indices\n        cans.erase(cans.begin() + startIdx, cans.begin() + endIdx + 1);\n    }\n    return total;\n}\n\nint main()\n{\n    string cans_count_temp;\n    getline(cin, cans_count_temp);\n    int cans_count = stoi(ltrim(rtrim(cans_count_temp)));\n    vector<int> cans(cans_count);\n    for (int i = 0; i < cans_count; i++) {\n        string cans_item_temp;\n        getline(cin, cans_item_temp);\n        int cans_item = stoi(ltrim(rtrim(cans_item_temp)));\n        cans[i] = cans_item;\n    }\n    int result = findTotalWeight(cans);\n    cout << result << \"\\n\";\n    return 0;\n}\n\nstring ltrim(const string &str) {\n    string s(str);\n    s.erase(\n        s.begin(),\n        find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))\n    );\n    return s;\n}\n\nstring rtrim(const string &str) {\n    string s(str);\n    s.erase(\n        find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),\n        s.end()\n    );\n    return s;\n}",
  "test_cases": [
    {
      "id": "test_1",
      "input": "3\n5\n2\n8",
      "expected_output": "7"
    },
    {
      "id": "test_2",
      "input": "4\n1\n3\n2\n4",
      "expected_output": "4"
    },
    {
      "id": "test_3",
      "input": "5\n10\n5\n15\n3\n7",
      "expected_output": "13"
    }
  ],
  "user_id": "test_cpp_cans",
  "question_id": "cpp_test"
}
PAYLOAD_EOF

echo "📤 Sending request..."
RESPONSE=$(curl -s -m 30 -X POST "$CONTAINER_APP_URL/execute" \
  -H "Content-Type: application/json" \
  -d @/tmp/test_cpp_payload.json)

# Save response
echo "$RESPONSE" > /tmp/test_cpp_response.json

# Parse and display results
python3 << 'PYEOF'
import json
import sys

try:
    with open('/tmp/test_cpp_response.json', 'r') as f:
        d = json.load(f)
    
    print("📊 Test Results:")
    print("=" * 60)
    
    summary = d.get('summary', {})
    metadata = d.get('metadata', {})
    
    status = "✅ All Passed!" if summary.get('all_passed') else "❌ Some Failed"
    print(f"Status: {status}")
    print(f"Passed: {summary.get('passed', 0)}/{summary.get('total_tests', 0)}")
    print(f"Pass Rate: {summary.get('pass_percentage', 0):.1f}%")
    print(f"Execution Time: {metadata.get('execution_time_ms', 0)}ms")
    print(f"Container ID: {metadata.get('container_id', 'unknown')}")
    print(f"CPU Usage: {metadata.get('cpu_usage_percent', 0):.1f}%")
    print(f"Memory Usage: {metadata.get('memory_usage_mb', 0):.1f} MB")
    
    print("\n📋 Individual Test Results:")
    print("-" * 60)
    for i, t in enumerate(d.get('test_results', []), 1):
        status_icon = "✅" if t.get('passed') else "❌"
        expected = t.get('expected_output', '').strip()
        actual = t.get('actual_output', '').strip() if t.get('actual_output') else "N/A"
        error = t.get('error', '')
        exec_time = t.get('execution_time_ms', 0)
        input_data = t.get('input', '')[:50]  # First 50 chars
        
        print(f"\nTest {i}: {status_icon}")
        print(f"  Input: {input_data}...")
        print(f"  Expected: {expected}")
        print(f"  Got: {actual}")
        print(f"  Time: {exec_time}ms")
        if error:
            print(f"  Error: {error[:200]}")
    
    print("\n" + "=" * 60)
    if summary.get('all_passed'):
        print("✅ SUCCESS: All tests passed!")
    else:
        print("❌ FAILURE: Some tests failed")
        sys.exit(1)
        
except json.JSONDecodeError as e:
    print(f"❌ JSON Parse Error: {e}")
    with open('/tmp/test_cpp_response.json', 'r') as f:
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

# Cleanup
rm -f /tmp/test_cpp_payload.json /tmp/test_cpp_response.json

exit $EXIT_CODE


