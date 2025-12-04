#!/bin/bash
# Quick test script that runs a test and stores it in monitoring dashboard
# Usage: ./quick-test-with-monitoring.sh

API_BASE_URL="http://localhost:3001/api"
EXECUTOR_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$EXECUTOR_URL" ]; then
    echo "❌ Error: Could not get Container App URL"
    exit 1
fi

echo "🧪 Quick Test with Monitoring"
echo "URL: $EXECUTOR_URL"
echo ""

# Test with Java (Climbing Stairs)
echo "Running test: Climbing Stairs (Java)"
RESPONSE=$(curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "java",
    "code": "public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }",
    "test_cases": [
      {"id": "test_1", "input": "3", "expected_output": "3"},
      {"id": "test_2", "input": "4", "expected_output": "5"}
    ],
    "user_id": "user_quick_test_'$(date +%s)'",
    "question_id": "15"
  }')

# Display result
echo "$RESPONSE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    summary = d.get('summary', {})
    print(f\"  ✅ PASSED: {summary.get('passed', 0)}/{summary.get('total_tests', 0)} tests\" if summary.get('all_passed') else f\"  ❌ FAILED: {summary.get('passed', 0)}/{summary.get('total_tests', 0)} tests\")
    print(f\"  Execution Time: {d.get('metadata', {}).get('execution_time_ms', 'N/A')}ms\")
    print(f\"  Container ID: {d.get('metadata', {}).get('container_id', 'unknown')[:50]}\")
except:
    print(\"  ❌ Error parsing response\")
    print(\"  Response:\", sys.stdin.read()[:200])
"

# Store in monitoring dashboard
echo ""
echo "📊 Storing in monitoring dashboard..."
STORE_RESULT=$(echo "$RESPONSE" | curl -s -X POST "${API_BASE_URL}/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @-)

if echo "$STORE_RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); exit(0 if d.get('success') else 1)" 2>/dev/null; then
    echo "✅ Stored successfully!"
    echo ""
    echo "💡 Open monitoring-dashboard.html to see the result"
else
    echo "⚠️  Failed to store. Make sure Node.js server is running: cd test-ui && npm start"
fi


