#!/bin/bash

# Test FastAPI Endpoints in Production
# Replace PROD_URL with your actual production URL

PROD_URL="${PROD_URL:-https://your-container-app.azurecontainerapps.io}"

echo "🧪 Testing FastAPI Endpoints in Production"
echo "=========================================="
echo "Production URL: $PROD_URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test health endpoint first
echo -e "${YELLOW}🏥 Health Check${NC}"
echo "-------------------"
HEALTH_RESPONSE=$(curl -s "$PROD_URL/health")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Service is healthy${NC}"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo -e "${RED}❌ Health check failed${NC}"
    exit 1
fi

echo ""
echo ""

# Test /run endpoint
echo -e "${YELLOW}📝 Test 1: /run endpoint${NC}"
echo "-------------------"

RUN_REQUEST='{
  "language": "python",
  "code": "a = int(input())\nb = int(input())\nprint(a + b)",
  "sample_test_cases": [
    {"id": "test_1", "input": "5\n3", "expected_output": "8"},
    {"id": "test_2", "input": "10\n20", "expected_output": "30"},
    {"id": "test_3", "input": "100\n200", "expected_output": "300"}
  ],
  "user_id": "prod_test_user",
  "question_id": "prod_test_q1",
  "timeout": 5
}'

echo "Sending request to $PROD_URL/run..."
RESPONSE=$(curl -s -X POST "$PROD_URL/run" \
  -H "Content-Type: application/json" \
  -d "$RUN_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""

# Test /runall endpoint
echo -e "${YELLOW}📝 Test 2: /runall endpoint${NC}"
echo "-------------------"

RUNALL_REQUEST='{
  "language": "python",
  "code": "a = int(input())\nb = int(input())\nprint(a + b)",
  "test_cases": [
    {"id": "test_1", "input": "5\n3", "expected_output": "8"},
    {"id": "test_2", "input": "10\n20", "expected_output": "30"},
    {"id": "test_3", "input": "100\n200", "expected_output": "300"}
  ],
  "sample_test_cases": [],
  "timeout": 5
}'

echo "Sending request to $PROD_URL/runall..."
RESPONSE=$(curl -s -X POST "$PROD_URL/runall" \
  -H "Content-Type: application/json" \
  -d "$RUNALL_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""

# Test /submit endpoint
echo -e "${YELLOW}📝 Test 3: /submit endpoint${NC}"
echo "-------------------"

SUBMIT_REQUEST='{
  "language": "python",
  "code": "a = int(input())\nb = int(input())\nprint(a + b)",
  "test_cases": [
    {"id": "test_1", "input": "5\n3", "expected_output": "8"},
    {"id": "test_2", "input": "10\n20", "expected_output": "30"},
    {"id": "test_3", "input": "100\n200", "expected_output": "300"}
  ],
  "user_id": "prod_test_user",
  "question_id": "prod_test_q1",
  "timeout": 5
}'

echo "Sending request to $PROD_URL/submit..."
RESPONSE=$(curl -s -X POST "$PROD_URL/submit" \
  -H "Content-Type: application/json" \
  -d "$SUBMIT_REQUEST")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Request successful${NC}"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
else
    echo -e "${RED}❌ Request failed${NC}"
fi

echo ""
echo ""
echo -e "${GREEN}✅ Production tests completed!${NC}"

