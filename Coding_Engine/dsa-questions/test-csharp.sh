#!/bin/bash
# Quick test script for C# execution

echo "🧪 Testing C# Execution..."
echo ""

# Simple C# program
CS_CODE='using System;

public class Solution {
    public static void Main() {
        Console.WriteLine("Hello from C#!");
        Console.WriteLine(42);
    }
}'

echo "📝 Test 1: Simple C# Hello World"
echo "Code:"
echo "$CS_CODE"
echo ""

# Get executor URL
EXECUTOR_URL="https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io"

echo "🚀 Testing executor at: $EXECUTOR_URL"
echo ""

# Test with simple program
PAYLOAD=$(cat <<EOF
{
  "language": "csharp",
  "code": "$CS_CODE",
  "test_cases": [
    {
      "input": "",
      "expected_output": "Hello from C#!\n42"
    }
  ]
}
EOF
)

echo "📤 Sending request..."
timeout 30 curl -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  -w "\n⏱️  Time: %{time_total}s\n" \
  2>&1 | head -50

echo ""
echo "✅ Test complete"

