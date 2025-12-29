#!/bin/bash

# Simple Question Test - Sum of Two Numbers
# This script tests the /run endpoint with a simple Python solution

EXECUTOR_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

echo "=========================================="
echo "🧪 Testing Simple Question: Sum of Two Numbers"
echo "=========================================="
echo ""

# Test 1: Using /run endpoint with sample test cases
echo "📤 Test 1: /run endpoint (Sample Test Cases)"
echo "--------------------------------------------"

curl -X POST "${EXECUTOR_URL}/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def add(a, b):\n    return a + b\n\na = int(input())\nb = int(input())\nresult = add(a, b)\nprint(result)",
    "sample_test_cases": [
      {
        "id": "sample_1",
        "input": "5\n3",
        "expected_output": "8"
      },
      {
        "id": "sample_2",
        "input": "10\n20",
        "expected_output": "30"
      }
    ],
    "question_id": "simple_sum",
    "user_id": "test_user"
  }' \
  -w "\n\n=== TIMING ===\nTotal: %{time_total}s\n" \
  -s | python3 -m json.tool

echo ""
echo ""

# Test 2: Using /runall endpoint with all test cases
echo "📤 Test 2: /runall endpoint (All Test Cases)"
echo "--------------------------------------------"

curl -X POST "${EXECUTOR_URL}/runall" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def add(a, b):\n    return a + b\n\na = int(input())\nb = int(input())\nresult = add(a, b)\nprint(result)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "1\n1",
        "expected_output": "2"
      },
      {
        "id": "test_2",
        "input": "0\n0",
        "expected_output": "0"
      },
      {
        "id": "test_3",
        "input": "-5\n5",
        "expected_output": "0"
      },
      {
        "id": "test_4",
        "input": "100\n200",
        "expected_output": "300"
      },
      {
        "id": "test_5",
        "input": "-10\n-20",
        "expected_output": "-30"
      }
    ],
    "sample_test_cases": [],
    "question_id": "simple_sum",
    "user_id": "test_user"
  }' \
  -w "\n\n=== TIMING ===\nTotal: %{time_total}s\n" \
  -s | python3 -m json.tool

echo ""
echo "=========================================="
echo "✅ Test Complete!"
echo "=========================================="


