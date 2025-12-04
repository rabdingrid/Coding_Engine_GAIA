#!/bin/bash

# Test script for "Compress Word" problem (Question ID: 622797)
# Tests all 15 test cases from the 622797 directory

CONTAINER_APP_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$CONTAINER_APP_URL" ]; then
    echo "❌ Error: Could not fetch Container App URL"
    exit 1
fi

TEST_CASES_DIR="/Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/622797"

if [ ! -d "$TEST_CASES_DIR" ]; then
    echo "❌ Error: Test cases directory not found: $TEST_CASES_DIR"
    exit 1
fi

echo "🧪 Testing: Compress Word Problem (Question ID: 622797)"
echo "📍 URL: $CONTAINER_APP_URL"
echo "📁 Test Cases Directory: $TEST_CASES_DIR"
echo ""

# Use Python to create the JSON payload properly
python3 << 'PYEOF' > /tmp/test_compress_payload.json
import json
import os

test_cases_dir = "/Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/622797"
test_cases = []

for i in range(15):
    input_file = f"{test_cases_dir}/input{i:03d}.txt"
    output_file = f"{test_cases_dir}/output{i:03d}.txt"
    
    if os.path.exists(input_file) and os.path.exists(output_file):
        with open(input_file, 'r') as f:
            lines = f.readlines()
            word = lines[0].strip()
            k = lines[1].strip() if len(lines) > 1 else ""
            input_str = f"{word}\n{k}"
        
        with open(output_file, 'r') as f:
            expected = f.read().strip()
        
        test_cases.append({
            "id": f"test_{i}",
            "input": input_str,
            "expected_output": expected
        })

python_code = '''def compressWord(word, k):
    stack = []  # Stack of [char, count]
    
    for char in word:
        if stack and stack[-1][0] == char:
            stack[-1][1] += 1
            if stack[-1][1] == k:
                stack.pop()
        else:
            stack.append([char, 1])
    
    result = "".join(char * count for char, count in stack)
    return result

# Read input
try:
    word = input().strip()
    k = int(input().strip())
    print(compressWord(word, k))
except EOFError:
    print("")'''

payload = {
    "language": "python",
    "code": python_code,
    "test_cases": test_cases,
    "user_id": "test_compress_word",
    "question_id": "622797"
}

print(json.dumps(payload))
PYEOF

TOTAL_TESTS=$(python3 << 'PYEOF'
import os
test_cases_dir = "/Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/622797"
count = sum(1 for i in range(15) if os.path.exists(f"{test_cases_dir}/input{i:03d}.txt") and os.path.exists(f"{test_cases_dir}/output{i:03d}.txt"))
print(count)
PYEOF
)

echo "📊 Found $TOTAL_TESTS test cases"
echo ""

echo "📤 Sending request with $TOTAL_TESTS test cases..."
START_TIME=$(date +%s)
RESPONSE=$(curl -s -m 60 -X POST "$CONTAINER_APP_URL/execute" \
  -H "Content-Type: application/json" \
  -d @/tmp/test_compress_payload.json)
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

# Save response
echo "$RESPONSE" > /tmp/test_compress_response.json

# Parse and display results
python3 << 'PYEOF'
import json
import sys

try:
    with open('/tmp/test_compress_response.json', 'r') as f:
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
    passed_count = 0
    failed_tests = []
    
    for i, t in enumerate(test_results, 1):
        status_icon = "✅" if t.get('passed') else "❌"
        expected = t.get('expected_output', '').strip()
        actual = t.get('actual_output', '').strip() if t.get('actual_output') else "N/A"
        error = t.get('error', '')
        exec_time = t.get('execution_time_ms', 0)
        input_data = t.get('input', '')
        
        # Parse input to show word and k
        input_lines = input_data.split('\n')
        word = input_lines[0] if len(input_lines) > 0 else ""
        k = input_lines[1] if len(input_lines) > 1 else ""
        
        # Truncate long words for display
        if len(word) > 30:
            word_display = word[:27] + "..."
        else:
            word_display = word
        
        if t.get('passed'):
            passed_count += 1
            print(f"Test {i:2d}: {status_icon} word=\"{word_display}\" k={k}")
        else:
            failed_tests.append(i)
            print(f"Test {i:2d}: {status_icon} word=\"{word_display}\" k={k}")
            print(f"         Expected: \"{expected}\"")
            print(f"         Got:      \"{actual}\"")
            if error:
                print(f"         Error: {error[:150]}")
    
    print("\n" + "=" * 70)
    if summary.get('all_passed'):
        print("✅ SUCCESS: All $TOTAL_TESTS tests passed!")
        print("🎯 System handled all test cases successfully!")
    else:
        print(f"❌ FAILURE: {len(failed_tests)} test(s) failed")
        print(f"   Failed tests: {failed_tests}")
        sys.exit(1)
        
except json.JSONDecodeError as e:
    print(f"❌ JSON Parse Error: {e}")
    with open('/tmp/test_compress_response.json', 'r') as f:
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
rm -f /tmp/test_compress_payload.json /tmp/test_compress_response.json

exit $EXIT_CODE

