#!/bin/bash

# Quick Local Testing Script
# Run: chmod +x test_local.sh && ./test_local.sh

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Testing ACA Code Executor Locally"
echo "=========================================="
echo ""

echo "1. Testing Health Endpoint..."
curl -s $BASE_URL/health | python3 -m json.tool
echo -e "\n"

echo "2. Testing Python Execution (Simple)..."
curl -s -X POST $BASE_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }' | python3 -m json.tool
echo -e "\n"

echo "3. Testing Python Execution (Multiple Test Cases)..."
curl -s -X POST $BASE_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "a = int(input())\nb = int(input())\nprint(a + b)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "5\n10",
        "expected_output": "15"
      },
      {
        "id": "test_2",
        "input": "100\n200",
        "expected_output": "300"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }' | python3 -m json.tool
echo -e "\n"

echo "4. Testing Failed Case..."
curl -s -X POST $BASE_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(10)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "20"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }' | python3 -m json.tool
echo -e "\n"

echo "=========================================="
echo "Local Testing Complete!"
echo "=========================================="
echo ""
echo "If all tests passed, you're ready to deploy!"
echo "Next steps:"
echo "  1. Build Docker image"
echo "  2. Push to ACR"
echo "  3. Deploy with Terraform"
echo ""


