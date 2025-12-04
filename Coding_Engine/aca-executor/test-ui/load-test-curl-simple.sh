#!/bin/bash
# Simplified Load Test using curl - Tests real capacity
# Uses only C++ code (known working) to test capacity

API_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"
NUM_USERS=${1:-30}  # Default to 30 users

echo "=================================================================================="
echo "🚀 CURL LOAD TEST - REAL CAPACITY TESTING"
echo "=================================================================================="
echo "API URL: $API_URL"
echo "Number of parallel users: $NUM_USERS"
echo "Language: C++ (all users)"
echo "Question: Warehouse Box Removal"
echo "=================================================================================="
echo ""

# C++ code (simplified, working version)
CPP_CODE='#include <bits/stdc++.h>
using namespace std;

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
    int n;
    cin >> n;
    vector<int> cans(n);
    for (int i = 0; i < n; i++) {
        cin >> cans[i];
    }
    cout << findTotalWeight(cans) << endl;
    return 0;
}'

# Test cases (JSON escaped)
TEST_CASES_JSON='[{"id":"test_1","input":"7\n6\n4\n9\n10\n34\n56\n54","expected_output":"68\n"},{"id":"test_2","input":"8\n132\n45\n65\n765\n345\n243\n75\n67","expected_output":"1120\n"}]'

# Function to submit request
submit_request() {
    local user_id=$1
    local start_time=$(date +%s.%N)
    
    # Create JSON payload (properly escaped)
    local payload=$(cat <<EOF
{
  "language": "cpp",
  "code": "$(echo "$CPP_CODE" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')",
  "test_cases": $TEST_CASES_JSON,
  "user_id": "$user_id",
  "question_id": "warehouse_box_removal",
  "timeout": 5
}
EOF
)
    
    # Write to temp file
    local temp_file="/tmp/curl_payload_${user_id}.json"
    echo "$payload" > "$temp_file"
    
    # Submit request
    local response=$(curl -s -w "\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d @"$temp_file" \
        --max-time 60 \
        "$API_URL/runall" 2>&1)
    
    local end_time=$(date +%s.%N)
    local wait_time=$(echo "$end_time - $start_time" | bc)
    local wait_time_ms=$(echo "$wait_time * 1000" | bc | cut -d. -f1)
    
    # Parse response
    local http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
    local time_total=$(echo "$response" | grep "TIME_TOTAL:" | cut -d: -f2)
    local body=$(echo "$response" | sed '/HTTP_CODE:/d' | sed '/TIME_TOTAL:/d')
    
    # Extract metadata using Python
    local container_id=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('container_id', 'unknown'))" 2>/dev/null || echo "unknown")
    local replica=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('replica', 'unknown'))" 2>/dev/null || echo "unknown")
    local exec_time=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('execution_time_ms', 0))" 2>/dev/null || echo "0")
    local all_passed=$(echo "$body" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('summary', {}).get('all_passed', False))" 2>/dev/null || echo "False")
    
    # Cleanup
    rm -f "$temp_file"
    
    # Return result
    echo "$user_id|$http_code|$wait_time_ms|$exec_time|$container_id|$replica|$all_passed|$time_total"
}

export -f submit_request
export API_URL CPP_CODE TEST_CASES_JSON

echo "⚡ Starting parallel execution of $NUM_USERS users..."
echo "   All requests sent simultaneously..."
echo ""

OVERALL_START=$(date +%s.%N)
RESULTS_FILE="/tmp/curl_load_test_results.txt"
> "$RESULTS_FILE"

# Submit all requests in parallel
PIDS=()
for i in $(seq 1 $NUM_USERS); do
    user_id="user_$i"
    (submit_request "$user_id" >> "$RESULTS_FILE") &
    PIDS+=($!)
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "   Submitted $i/$NUM_USERS requests..."
    fi
done

echo "   All requests submitted. Waiting for completion..."
echo ""

# Wait for all
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

TOTAL=$(wc -l < "$RESULTS_FILE" | tr -d ' ')
SUCCESS=$(grep -c "|200|" "$RESULTS_FILE" || echo "0")
FAILED=$((TOTAL - SUCCESS))

echo "📈 Summary:"
echo "   Total requests: $TOTAL"
echo "   ✅ Successful: $SUCCESS"
echo "   ❌ Failed: $FAILED"
if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$(echo "scale=1; $SUCCESS * 100 / $TOTAL" | bc)
    echo "   Success rate: ${SUCCESS_RATE}%"
fi
echo ""

if [ $SUCCESS -gt 0 ]; then
    # Wait times
    WAIT_TIMES=$(cut -d'|' -f3 "$RESULTS_FILE" | grep -v "^$" | grep -v "unknown" | sort -n)
    if [ -n "$WAIT_TIMES" ]; then
        MIN_WAIT=$(echo "$WAIT_TIMES" | head -1)
        MAX_WAIT=$(echo "$WAIT_TIMES" | tail -1)
        AVG_WAIT=$(echo "$WAIT_TIMES" | awk '{sum+=$1; count++} END {if(count>0) print int(sum/count); else print 0}')
        
        echo "⏱️  Wait Times (Time until response received):"
        echo "   Min: ${MIN_WAIT}ms"
        echo "   Max: ${MAX_WAIT}ms"
        echo "   Avg: ${AVG_WAIT}ms"
        if [ "$MAX_WAIT" -lt 5000 ] 2>/dev/null; then
            echo "   Target: < 5000ms ✅"
        else
            echo "   Target: < 5000ms ❌ (Max: ${MAX_WAIT}ms)"
        fi
        echo ""
    fi
    
    # Execution times
    EXEC_TIMES=$(cut -d'|' -f4 "$RESULTS_FILE" | grep -v "^$" | grep -v "unknown" | sort -n)
    if [ -n "$EXEC_TIMES" ]; then
        MIN_EXEC=$(echo "$EXEC_TIMES" | head -1)
        MAX_EXEC=$(echo "$EXEC_TIMES" | tail -1)
        AVG_EXEC=$(echo "$EXEC_TIMES" | awk '{sum+=$1; count++} END {if(count>0) print int(sum/count); else print 0}')
        
        echo "⚡ Execution Times:"
        echo "   Min: ${MIN_EXEC}ms"
        echo "   Max: ${MAX_EXEC}ms"
        echo "   Avg: ${AVG_EXEC}ms"
        echo ""
    fi
    
    # Container distribution
    echo "🔄 Container Distribution:"
    cut -d'|' -f5 "$RESULTS_FILE" | grep -v "unknown" | sort | uniq -c | sort -rn | head -10 | while read count container; do
        echo "   $container: $count requests"
    done
    echo ""
    
    # Replica distribution
    echo "🔄 Replica Distribution:"
    cut -d'|' -f6 "$RESULTS_FILE" | grep -v "unknown" | sort | uniq -c | sort -rn | head -10 | while read count replica; do
        echo "   $replica: $count requests"
    done
    echo ""
    
    # Test results
    ALL_PASSED=$(grep -c "|True|" "$RESULTS_FILE" || echo "0")
    echo "✅ All tests passed: $ALL_PASSED/$SUCCESS"
    echo ""
    
    # Capacity analysis
    echo "📈 Capacity Analysis:"
    echo "   Total time: ${OVERALL_TIME_MS}ms"
    echo "   Requests handled: $SUCCESS"
    echo "   Requests/second: $(echo "scale=2; $SUCCESS * 1000 / $OVERALL_TIME_MS" | bc)"
    echo "   Concurrent capacity: ~$SUCCESS requests in ${OVERALL_TIME_MS}ms"
    echo ""
fi

# Show failures
if [ $FAILED -gt 0 ]; then
    echo "❌ Failed Requests (first 10):"
    grep -v "|200|" "$RESULTS_FILE" | head -10 | while IFS='|' read user code wait exec container replica passed time; do
        echo "   $user: HTTP $code"
    done
    echo ""
fi

# Show sample results
echo "=================================================================================="
echo "📋 SAMPLE RESULTS (First 15)"
echo "=================================================================================="
printf "%-10s %-8s %-10s %-10s %-25s %-10s\n" "User" "Status" "Wait(ms)" "Exec(ms)" "Container" "All Pass"
echo "--------------------------------------------------------------------------------"
head -15 "$RESULTS_FILE" | while IFS='|' read user code wait exec container replica passed time; do
    if [ "$code" = "200" ]; then
        status="✅"
    else
        status="❌$code"
    fi
    if [ "$passed" = "True" ]; then
        pass_icon="✅"
    else
        pass_icon="❌"
    fi
    container_short=$(echo "$container" | cut -c1-25)
    printf "%-10s %-8s %-10s %-10s %-25s %-10s\n" "$user" "$status" "$wait" "$exec" "$container_short" "$pass_icon"
done

echo ""
echo "=================================================================================="
echo "✅ Load test complete!"
echo "=================================================================================="

# Cleanup
rm -f "$RESULTS_FILE"

