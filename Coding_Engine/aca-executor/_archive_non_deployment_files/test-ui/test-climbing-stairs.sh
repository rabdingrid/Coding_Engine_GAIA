#!/bin/bash
# Multi-User Test Script for Climbing Stairs Question
# Run this from multiple systems simultaneously to test concurrent load

# Get Container App URL
URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$URL" ]; then
    echo "❌ Error: Could not get Container App URL"
    exit 1
fi

# Generate unique user ID
USER_ID="user_$(date +%s)_$(whoami)_$$"

echo "🧪 Testing Climbing Stairs Question"
echo "URL: $URL"
echo "User ID: $USER_ID"
echo ""

# Test with Java
echo "1. Testing Java (5 test cases):"
RESPONSE=$(curl -s -m 60 -X POST "$URL/execute" \
  -H "Content-Type: application/json" \
  -d "{
    \"language\": \"java\",
    \"code\": \"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }\",
    \"test_cases\": [
      {\"id\": \"test_1\", \"input\": \"2\", \"expected_output\": \"2\"},
      {\"id\": \"test_2\", \"input\": \"3\", \"expected_output\": \"3\"},
      {\"id\": \"test_3\", \"input\": \"4\", \"expected_output\": \"5\"},
      {\"id\": \"test_4\", \"input\": \"5\", \"expected_output\": \"8\"},
      {\"id\": \"test_5\", \"input\": \"1\", \"expected_output\": \"1\"}
    ],
    \"user_id\": \"$USER_ID\",
    \"question_id\": \"15\"
  }")

# Parse and display results
echo "$RESPONSE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    summary = d.get('summary', {})
    print(f\"  ✅ PASSED: {summary.get('passed', 0)}/{summary.get('total_tests', 0)} tests\" if summary.get('all_passed') else f\"  ❌ FAILED: {summary.get('passed', 0)}/{summary.get('total_tests', 0)} tests\")
    print(f\"  Execution Time: {d.get('metadata', {}).get('execution_time_ms', 'N/A')}ms\")
    print(f\"  Container ID: {d.get('metadata', {}).get('container_id', 'unknown')}\")
    print(f\"  CPU Usage: {d.get('metadata', {}).get('cpu_usage_percent', 'N/A')}%\")
    print(f\"  Memory: {d.get('metadata', {}).get('memory_usage_mb', 'N/A')} MB\")
except:
    print(\"  ❌ Error parsing response\")
    print(\"  Response:\", sys.stdin.read()[:200])
"

echo ""
echo "✅ Test completed for User: $USER_ID"


