#!/bin/bash
# Load Test using curl - Tests real capacity with parallel requests
# Tests question 39 (Warehouse Box Removal) with multiple users

API_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"
NUM_USERS=${1:-30}  # Default to 30 users, can be overridden

echo "=================================================================================="
echo "🚀 CURL-BASED LOAD TEST - REAL CAPACITY TESTING"
echo "=================================================================================="
echo "API URL: $API_URL"
echo "Number of parallel users: $NUM_USERS"
echo "Question: #39 (Warehouse Box Removal)"
echo "=================================================================================="
echo ""

# C++ solution code
CPP_CODE='#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

int findTotalWeight(vector<int> cans) {
    int total = 0;
    while (!cans.empty()) {
        int minVal = INT_MAX;
        int idx = -1;
        for (int i = 0; i < cans.size(); i++) {
            if (cans[i] < minVal) {
                minVal = cans[i];
                idx = i;
            }
        }
        total += minVal;
        int start = max(0, idx - 1);
        int end = min((int)cans.size() - 1, idx + 1);
        for (int i = end; i >= start; i--) {
            cans.erase(cans.begin() + i);
        }
    }
    return total;
}

int main() {
    string cans_count_temp;
    getline(cin, cans_count_temp);
    int cans_count = stoi(ltrim(rtrim(cans_count_temp)));
    vector<int> cans(cans_count);
    for (int i = 0; i < cans_count; i++) {
        string cans_item_temp;
        getline(cin, cans_item_temp);
        int cans_item = stoi(ltrim(rtrim(cans_item_temp)));
        cans[i] = cans_item;
    }
    int result = findTotalWeight(cans);
    cout << result << "\n";
    return 0;
}

string ltrim(const string &str) {
    string s(str);
    s.erase(s.begin(), find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace))));
    return s;
}

string rtrim(const string &str) {
    string s(str);
    s.erase(find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(), s.end());
    return s;
}'

# Test cases
TEST_CASES='[
  {"id": "test_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
  {"id": "test_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"}
]'

# Create payload JSON file
PAYLOAD_FILE="/tmp/load_test_payload.json"

# Languages to test
LANGUAGES=("cpp" "java" "javascript" "csharp" "python")

echo "📋 Preparing test payloads..."
echo ""

# Create a function to submit code
submit_request() {
    local user_id=$1
    local language=$2
    local code=$3
    
    # Create payload
    local payload=$(cat <<EOF
{
  "language": "$language",
  "code": $(echo "$code" | python3 -c "import sys, json; print(json.dumps(sys.stdin.read()))"),
  "test_cases": $TEST_CASES,
  "user_id": "$user_id",
  "question_id": "warehouse_box_removal",
  "timeout": 5
}
EOF
)
    
    # Write payload to temp file
    echo "$payload" > "${PAYLOAD_FILE}_${user_id}_${language}.json"
    
    # Submit request and measure time
    local start_time=$(date +%s.%N)
    local response=$(curl -s -w "\n%{http_code}\n%{time_total}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d @"${PAYLOAD_FILE}_${user_id}_${language}.json" \
        --max-time 60 \
        "$API_URL/runall" 2>&1)
    
    local end_time=$(date +%s.%N)
    local wait_time=$(echo "$end_time - $start_time" | bc)
    local wait_time_ms=$(echo "$wait_time * 1000" | bc | cut -d. -f1)
    
    # Parse response
    local http_code=$(echo "$response" | tail -2 | head -1)
    local time_total=$(echo "$response" | tail -1)
    local body=$(echo "$response" | sed '$d' | sed '$d')
    
    # Extract metadata
    local container_id=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('container_id', 'unknown'))" 2>/dev/null || echo "unknown")
    local replica=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('replica', 'unknown'))" 2>/dev/null || echo "unknown")
    local exec_time=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('execution_time_ms', 0))" 2>/dev/null || echo "0")
    local all_passed=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('summary', {}).get('all_passed', False))" 2>/dev/null || echo "False")
    
    # Return result
    echo "$user_id|$language|$http_code|$wait_time_ms|$exec_time|$container_id|$replica|$all_passed|$time_total"
}

# Export function for parallel execution
export -f submit_request
export API_URL TEST_CASES PAYLOAD_FILE CPP_CODE

echo "⚡ Starting parallel execution of $NUM_USERS users..."
echo "   All requests will be sent simultaneously..."
echo ""

# Record overall start time
OVERALL_START=$(date +%s.%N)

# Submit all requests in parallel using GNU parallel or background jobs
RESULTS_FILE="/tmp/load_test_results.txt"
> "$RESULTS_FILE"

# Create array of jobs
PIDS=()
for i in $(seq 1 $NUM_USERS); do
    user_id="user_$i"
    language=${LANGUAGES[$((($i - 1) % ${#LANGUAGES[@]}))]}
    
    # Submit in background
    (submit_request "$user_id" "$language" "$CPP_CODE" >> "$RESULTS_FILE") &
    PIDS+=($!)
    
    # Print progress every 10 users
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Submitted $i/$NUM_USERS requests..."
    fi
done

echo "   All $NUM_USERS requests submitted. Waiting for completion..."
echo ""

# Wait for all jobs to complete
for pid in "${PIDS[@]}"; do
    wait $pid
done

OVERALL_END=$(date +%s.%N)
OVERALL_TIME=$(echo "$OVERALL_END - $OVERALL_START" | bc)
OVERALL_TIME_MS=$(echo "$OVERALL_TIME * 1000" | bc | cut -d. -f1)

echo "✅ All requests completed!"
echo ""

# Analyze results
echo "=================================================================================="
echo "📊 RESULTS ANALYSIS"
echo "=================================================================================="
echo ""

# Count successes and failures
TOTAL=$(wc -l < "$RESULTS_FILE" | tr -d ' ')
SUCCESS=$(grep -c "|200|" "$RESULTS_FILE" || echo "0")
FAILED=$((TOTAL - SUCCESS))

echo "📈 Summary:"
echo "   Total requests: $TOTAL"
echo "   ✅ Successful: $SUCCESS"
echo "   ❌ Failed: $FAILED"
echo "   Success rate: $(echo "scale=1; $SUCCESS * 100 / $TOTAL" | bc)%"
echo ""

if [ $SUCCESS -gt 0 ]; then
    # Extract wait times (column 4)
    WAIT_TIMES=$(cut -d'|' -f4 "$RESULTS_FILE" | grep -v "^$" | sort -n)
    MIN_WAIT=$(echo "$WAIT_TIMES" | head -1)
    MAX_WAIT=$(echo "$WAIT_TIMES" | tail -1)
    AVG_WAIT=$(echo "$WAIT_TIMES" | awk '{sum+=$1; count++} END {if(count>0) print int(sum/count); else print 0}')
    
    # Extract execution times (column 5)
    EXEC_TIMES=$(cut -d'|' -f5 "$RESULTS_FILE" | grep -v "^$" | sort -n)
    MIN_EXEC=$(echo "$EXEC_TIMES" | head -1)
    MAX_EXEC=$(echo "$EXEC_TIMES" | tail -1)
    AVG_EXEC=$(echo "$EXEC_TIMES" | awk '{sum+=$1; count++} END {if(count>0) print int(sum/count); else print 0}')
    
    echo "⏱️  Wait Times (Time until response received):"
    echo "   Min: ${MIN_WAIT}ms"
    echo "   Max: ${MAX_WAIT}ms"
    echo "   Avg: ${AVG_WAIT}ms"
    if [ "$MAX_WAIT" -lt 5000 ]; then
        echo "   Target: < 5000ms ✅"
    else
        echo "   Target: < 5000ms ❌ (Max wait: ${MAX_WAIT}ms)"
    fi
    echo ""
    
    echo "⚡ Execution Times (Code execution duration):"
    echo "   Min: ${MIN_EXEC}ms"
    echo "   Max: ${MAX_EXEC}ms"
    echo "   Avg: ${AVG_EXEC}ms"
    echo ""
    
    # Container distribution
    echo "🔄 Container Distribution:"
    cut -d'|' -f6 "$RESULTS_FILE" | grep -v "unknown" | sort | uniq -c | sort -rn | head -10 | while read count container; do
        echo "   $container: $count requests"
    done
    echo ""
    
    # Replica distribution
    echo "🔄 Replica Distribution:"
    cut -d'|' -f7 "$RESULTS_FILE" | grep -v "unknown" | sort | uniq -c | sort -rn | head -10 | while read count replica; do
        echo "   $replica: $count requests"
    done
    echo ""
    
    # Test results
    ALL_PASSED=$(grep -c "|True|" "$RESULTS_FILE" || echo "0")
    echo "✅ All tests passed: $ALL_PASSED/$SUCCESS"
    echo ""
    
    # Parallel efficiency
    TOTAL_EXEC_TIME=$(echo "$EXEC_TIMES" | awk '{sum+=$1} END {print int(sum)}')
    EFFICIENCY=$(echo "scale=1; $TOTAL_EXEC_TIME * 100 / $OVERALL_TIME_MS" | bc)
    echo "📈 Parallel Execution Analysis:"
    echo "   Total time for $NUM_USERS requests: ${OVERALL_TIME_MS}ms"
    echo "   If sequential: ${TOTAL_EXEC_TIME}ms"
    echo "   Parallel efficiency: ${EFFICIENCY}%"
    echo "   Requests processed in parallel: $SUCCESS"
    echo ""
fi

# Show failed requests
if [ $FAILED -gt 0 ]; then
    echo "❌ Failed Requests:"
    grep -v "|200|" "$RESULTS_FILE" | head -10 | while IFS='|' read user lang code wait exec container replica passed time; do
        echo "   $user ($lang): HTTP $code"
    done
    echo ""
fi

# Detailed results table
echo "=================================================================================="
echo "📋 DETAILED RESULTS (First 20)"
echo "=================================================================================="
printf "%-10s %-10s %-8s %-10s %-10s %-25s %-10s\n" "User" "Language" "Status" "Wait(ms)" "Exec(ms)" "Container" "All Pass"
echo "--------------------------------------------------------------------------------"
head -20 "$RESULTS_FILE" | while IFS='|' read user lang code wait exec container replica passed time; do
    if [ "$code" = "200" ]; then
        status="✅"
    else
        status="❌"
    fi
    if [ "$passed" = "True" ]; then
        pass_icon="✅"
    else
        pass_icon="❌"
    fi
    container_short=$(echo "$container" | cut -c1-25)
    printf "%-10s %-10s %-8s %-10s %-10s %-25s %-10s\n" "$user" "$lang" "$status" "$wait" "$exec" "$container_short" "$pass_icon"
done

echo ""
echo "=================================================================================="
echo "✅ Load test complete!"
echo "=================================================================================="
echo ""
echo "📊 Capacity Analysis:"
echo "   Current replicas: 2 (min)"
echo "   Expected capacity: 2 × 10 = 20 concurrent requests"
echo "   Actual requests handled: $SUCCESS"
echo "   Max wait time: ${MAX_WAIT}ms"
echo ""

# Cleanup
rm -f "${PAYLOAD_FILE}"_*.json
rm -f "$RESULTS_FILE"

