#!/bin/bash

# Test script for "Odd Frequency Sum" problem
# Original code used fs.readFileSync() which is blocked by security
# Fixed version uses process.stdin for multi-line input

CONTAINER_APP_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$CONTAINER_APP_URL" ]; then
    echo "❌ Error: Could not fetch Container App URL"
    exit 1
fi

echo "🧪 Testing Odd Frequency Sum Problem"
echo "📍 URL: $CONTAINER_APP_URL"
echo ""

# Create JSON payload file to avoid shell escaping issues
cat > /tmp/test_payload.json << 'PAYLOAD_EOF'
{
  "language": "javascript",
  "code": "const readline = require(\"readline\");\nconst rl = readline.createInterface({ input: process.stdin, output: process.stdout });\nlet input = \"\";\nprocess.stdin.on(\"data\", (data) => {\n  input += data.toString();\n});\nprocess.stdin.on(\"end\", () => {\n  const lines = input.trim().split(\"\\n\").map(line => line.trim());\n  const n = parseInt(lines[0]);\n  const arr = lines.slice(1).map(Number);\n  const freq = {};\n  for (let x of arr) {\n    freq[x] = (freq[x] || 0) + 1;\n  }\n  let sum = 0;\n  for (let key in freq) {\n    if (freq[key] % 2 !== 0) {\n      sum += parseInt(key);\n    }\n  }\n  console.log(sum);\n});",
  "test_cases": [
    {
      "id": "test_1",
      "input": "5\n1\n2\n3\n2\n1",
      "expected_output": "3"
    },
    {
      "id": "test_2",
      "input": "7\n4\n4\n4\n5\n5\n6\n6",
      "expected_output": "4"
    },
    {
      "id": "test_3",
      "input": "60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12",
      "expected_output": "309"
    }
  ],
  "user_id": "test_odd_frequency",
  "question_id": "test"
}
PAYLOAD_EOF

echo "📤 Sending request..."
RESPONSE=$(curl -s -m 30 -X POST "$CONTAINER_APP_URL/execute" \
  -H "Content-Type: application/json" \
  -d @/tmp/test_payload.json)

# Save response
echo "$RESPONSE" > /tmp/test_response.json

# Parse and display results
python3 << 'PYEOF'
import json
import sys

try:
    with open('/tmp/test_response.json', 'r') as f:
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
        
        print(f"\nTest {i}: {status_icon}")
        print(f"  Expected: {expected}")
        print(f"  Got: {actual}")
        print(f"  Time: {exec_time}ms")
        if error:
            print(f"  Error: {error[:150]}")
    
    print("\n" + "=" * 60)
    if summary.get('all_passed'):
        print("✅ SUCCESS: All tests passed!")
    else:
        print("❌ FAILURE: Some tests failed")
        sys.exit(1)
        
except json.JSONDecodeError as e:
    print(f"❌ JSON Parse Error: {e}")
    with open('/tmp/test_response.json', 'r') as f:
        content = f.read()
        print(f"\nRaw Response (first 500 chars):")
        print(content[:500])
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
PYEOF

EXIT_CODE=$?

# Cleanup
rm -f /tmp/test_payload.json /tmp/test_response.json

exit $EXIT_CODE


