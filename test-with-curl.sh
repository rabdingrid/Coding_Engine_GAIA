#!/bin/bash
# Test Python vs C++ with curl commands
# Measures actual network overhead and execution times

API_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall"

# Python O(n²) solution
PYTHON_CODE='def findTotalWeight(boxes):
    total = 0
    while boxes:
        min_weight = min(boxes)
        min_idx = boxes.index(min_weight)
        start = max(0, min_idx - 1)
        end = min(len(boxes), min_idx + 2)
        total += min_weight
        boxes = boxes[:start] + boxes[end:]
    return total

n = int(input())
boxes = [int(input()) for _ in range(n)]
result = findTotalWeight(boxes)
print(result)'

# Python O(n log n) solution
PYTHON_OPTIMIZED='import heapq

def findTotalWeight(boxes):
    if not boxes:
        return 0
    heap = [(weight, idx) for idx, weight in enumerate(boxes)]
    heapq.heapify(heap)
    removed = [False] * len(boxes)
    total = 0
    
    while heap:
        weight, idx = heapq.heappop(heap)
        if removed[idx]:
            continue
        removed[idx] = True
        if idx > 0:
            removed[idx-1] = True
        if idx < len(boxes) - 1:
            removed[idx+1] = True
        total += weight
    
    return total

n = int(input())
boxes = [int(input()) for _ in range(n)]
result = findTotalWeight(boxes)
print(result)'

# C++ O(n²) solution
CPP_CODE='#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

int findTotalWeight(vector<int>& boxes) {
    int total = 0;
    while (!boxes.empty()) {
        int min_weight = INT_MAX;
        int min_idx = -1;
        
        for (int i = 0; i < boxes.size(); i++) {
            if (boxes[i] < min_weight) {
                min_weight = boxes[i];
                min_idx = i;
            }
        }
        
        total += min_weight;
        
        int start = max(0, min_idx - 1);
        int end = min((int)boxes.size(), min_idx + 2);
        boxes.erase(boxes.begin() + start, boxes.begin() + end);
    }
    return total;
}

int main() {
    int n;
    cin >> n;
    vector<int> boxes(n);
    for (int i = 0; i < n; i++) {
        cin >> boxes[i];
    }
    cout << findTotalWeight(boxes) << endl;
    return 0;
}'

# Test case: 200 boxes (medium size)
TEST_INPUT="200
$(seq -s $'\n' 1 200)"

echo "=================================================================================="
echo "🧪 Testing with curl - Actual Performance Measurement"
echo "=================================================================================="
echo ""

# Test 1: Python O(n²)
echo "Test 1: Python O(n²) Algorithm"
echo "----------------------------------------------------------------------------------"
START_TIME=$(date +%s.%N)

RESPONSE=$(curl -s -w "\n%{time_total}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"language\": \"python\",
    \"code\": $(echo "$PYTHON_CODE" | jq -Rs .),
    \"test_cases\": [{
      \"id\": \"test_200\",
      \"input\": $(echo "$TEST_INPUT" | jq -Rs .),
      \"expected_output\": \"0\"
    }],
    \"sample_test_cases\": [],
    \"user_id\": \"curl_test_python_n2\",
    \"question_id\": \"test_200\"
  }")

END_TIME=$(date +%s.%N)
TOTAL_TIME=$(echo "$END_TIME - $START_TIME" | bc)

echo "Response:"
echo "$RESPONSE" | head -n -1 | jq -r '.metadata.execution_time_ms, .metadata.execution_time_ms/1000' 2>/dev/null || echo "Error parsing response"
echo "Total curl time: ${TOTAL_TIME}s"
echo ""

# Test 2: Python O(n log n)
echo "Test 2: Python O(n log n) Algorithm (Optimized)"
echo "----------------------------------------------------------------------------------"
START_TIME=$(date +%s.%N)

RESPONSE2=$(curl -s -w "\n%{time_total}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"language\": \"python\",
    \"code\": $(echo "$PYTHON_OPTIMIZED" | jq -Rs .),
    \"test_cases\": [{
      \"id\": \"test_200_opt\",
      \"input\": $(echo "$TEST_INPUT" | jq -Rs .),
      \"expected_output\": \"0\"
    }],
    \"sample_test_cases\": [],
    \"user_id\": \"curl_test_python_optimized\",
    \"question_id\": \"test_200_opt\"
  }")

END_TIME=$(date +%s.%N)
TOTAL_TIME2=$(echo "$END_TIME - $START_TIME" | bc)

echo "Response:"
echo "$RESPONSE2" | head -n -1 | jq -r '.metadata.execution_time_ms, .metadata.execution_time_ms/1000' 2>/dev/null || echo "Error parsing response"
echo "Total curl time: ${TOTAL_TIME2}s"
echo ""

# Test 3: C++ O(n²)
echo "Test 3: C++ O(n²) Algorithm"
echo "----------------------------------------------------------------------------------"
START_TIME=$(date +%s.%N)

RESPONSE3=$(curl -s -w "\n%{time_total}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"language\": \"cpp\",
    \"code\": $(echo "$CPP_CODE" | jq -Rs .),
    \"test_cases\": [{
      \"id\": \"test_200_cpp\",
      \"input\": $(echo "$TEST_INPUT" | jq -Rs .),
      \"expected_output\": \"0\"
    }],
    \"sample_test_cases\": [],
    \"user_id\": \"curl_test_cpp_n2\",
    \"question_id\": \"test_200_cpp\"
  }")

END_TIME=$(date +%s.%N)
TOTAL_TIME3=$(echo "$END_TIME - $START_TIME" | bc)

echo "Response:"
echo "$RESPONSE3" | head -n -1 | jq -r '.metadata.execution_time_ms, .metadata.execution_time_ms/1000' 2>/dev/null || echo "Error parsing response"
echo "Total curl time: ${TOTAL_TIME3}s"
echo ""

# Summary
echo "=================================================================================="
echo "📊 Summary"
echo "=================================================================================="
echo "Python O(n²):     Total: ${TOTAL_TIME}s"
echo "Python O(n log n): Total: ${TOTAL_TIME2}s"
echo "C++ O(n²):        Total: ${TOTAL_TIME3}s"
echo ""



