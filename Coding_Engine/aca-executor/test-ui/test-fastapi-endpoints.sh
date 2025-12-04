#!/bin/bash

# Test FastAPI Endpoints Locally
# Tests /run, /runall, and /submit endpoints with 20 test cases each

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "🧪 Testing FastAPI Endpoints"
echo "============================"
echo "Base URL: $BASE_URL"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Simple Python code - Sum of two numbers
echo -e "${YELLOW}📝 Test 1: /run endpoint - Python (Sample Test Cases)${NC}"
echo "---------------------------------------------------"

# Generate 20 sample test cases for sum problem
SAMPLE_TEST_CASES='['
for i in {1..20}; do
    a=$((RANDOM % 1000 + 1))
    b=$((RANDOM % 1000 + 1))
    sum=$((a + b))
    if [ $i -gt 1 ]; then
        SAMPLE_TEST_CASES+=','
    fi
    SAMPLE_TEST_CASES+="{\"id\":\"sample_$i\",\"input\":\"$a\n$b\",\"expected_output\":\"$sum\"}"
done
SAMPLE_TEST_CASES+=']'

# Python code for sum
PYTHON_CODE='a = int(input())
b = int(input())
print(a + b)'

RUN_REQUEST=$(cat <<EOF
{
  "language": "python",
  "code": "$(echo "$PYTHON_CODE" | sed 's/"/\\"/g' | tr '\n' '\\n')",
  "sample_test_cases": $SAMPLE_TEST_CASES,
  "user_id": "test_user_1",
  "question_id": "test_q1",
  "timeout": 5
}
EOF
)

echo "Sending request to /run..."
RESPONSE=$(curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d "$RUN_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    
    # Extract summary
    PASSED=$(echo "$RESPONSE" | grep -o '"passed":[0-9]*' | head -1 | cut -d':' -f2)
    TOTAL=$(echo "$RESPONSE" | grep -o '"total_tests":[0-9]*' | head -1 | cut -d':' -f2)
    echo -e "${GREEN}Summary: $PASSED/$TOTAL test cases passed${NC}"
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""

# Test 2: /runall endpoint - All test cases (excluding sample)
echo -e "${YELLOW}📝 Test 2: /runall endpoint - Python (All Test Cases)${NC}"
echo "---------------------------------------------------"

# Generate 20 test cases for runall (different from sample)
ALL_TEST_CASES='['
for i in {1..20}; do
    a=$((RANDOM % 5000 + 1))
    b=$((RANDOM % 5000 + 1))
    sum=$((a + b))
    if [ $i -gt 1 ]; then
        ALL_TEST_CASES+=','
    fi
    ALL_TEST_CASES+="{\"id\":\"test_$i\",\"input\":\"$a\n$b\",\"expected_output\":\"$sum\"}"
done
ALL_TEST_CASES+=']'

RUNALL_REQUEST=$(cat <<EOF
{
  "language": "python",
  "code": "$(echo "$PYTHON_CODE" | sed 's/"/\\"/g' | tr '\n' '\\n')",
  "test_cases": $ALL_TEST_CASES,
  "sample_test_cases": [],
  "user_id": "test_user_1",
  "question_id": "test_q1",
  "timeout": 5
}
EOF
)

echo "Sending request to /runall..."
RESPONSE=$(curl -s -X POST "$BASE_URL/runall" \
  -H "Content-Type: application/json" \
  -d "$RUNALL_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    
    # Extract summary
    PASSED=$(echo "$RESPONSE" | grep -o '"passed":[0-9]*' | head -1 | cut -d':' -f2)
    TOTAL=$(echo "$RESPONSE" | grep -o '"total_tests":[0-9]*' | head -1 | cut -d':' -f2)
    echo -e "${GREEN}Summary: $PASSED/$TOTAL test cases passed${NC}"
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""

# Test 3: /submit endpoint - Save to database
echo -e "${YELLOW}📝 Test 3: /submit endpoint - Python (Save to DB)${NC}"
echo "---------------------------------------------------"

# Generate 20 test cases for submission
SUBMIT_TEST_CASES='['
for i in {1..20}; do
    a=$((RANDOM % 10000 + 1))
    b=$((RANDOM % 10000 + 1))
    sum=$((a + b))
    if [ $i -gt 1 ]; then
        SUBMIT_TEST_CASES+=','
    fi
    SUBMIT_TEST_CASES+="{\"id\":\"submit_test_$i\",\"input\":\"$a\n$b\",\"expected_output\":\"$sum\"}"
done
SUBMIT_TEST_CASES+=']'

SUBMIT_REQUEST=$(cat <<EOF
{
  "language": "python",
  "code": "$(echo "$PYTHON_CODE" | sed 's/"/\\"/g' | tr '\n' '\\n')",
  "test_cases": $SUBMIT_TEST_CASES,
  "sample_test_cases": [],
  "user_id": "test_user_submit_1",
  "question_id": "test_q_submit_1",
  "timeout": 5
}
EOF
)

echo "Sending request to /submit..."
RESPONSE=$(curl -s -X POST "$BASE_URL/submit" \
  -H "Content-Type: application/json" \
  -d "$SUBMIT_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    
    # Extract summary
    PASSED=$(echo "$RESPONSE" | grep -o '"passed":[0-9]*' | head -1 | cut -d':' -f2)
    TOTAL=$(echo "$RESPONSE" | grep -o '"total_tests":[0-9]*' | head -1 | cut -d':' -f2)
    SAVED=$(echo "$RESPONSE" | grep -o '"saved_to_db":[a-z]*' | head -1 | cut -d':' -f2)
    echo -e "${GREEN}Summary: $PASSED/$TOTAL test cases passed${NC}"
    echo -e "${GREEN}Saved to DB: $SAVED${NC}"
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""

# Test 4: Test with error cases (TLE, syntax error)
echo -e "${YELLOW}📝 Test 4: Error Detection - Syntax Error${NC}"
echo "---------------------------------------------------"

SYNTAX_ERROR_CODE='print(10  # syntax error'

ERROR_TEST_CASES='[{"id":"error_test_1","input":"","expected_output":"10"}]'

ERROR_REQUEST=$(cat <<EOF
{
  "language": "python",
  "code": "$(echo "$SYNTAX_ERROR_CODE" | sed 's/"/\\"/g' | tr '\n' '\\n')",
  "sample_test_cases": $ERROR_TEST_CASES,
  "timeout": 5
}
EOF
)

echo "Sending request with syntax error..."
RESPONSE=$(curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d "$ERROR_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    
    # Check for syntax_error status
    if echo "$RESPONSE" | grep -q "syntax_error"; then
        echo -e "${GREEN}✅ Syntax error detected correctly${NC}"
    fi
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""
echo -e "${GREEN}✅ All tests completed!${NC}"

