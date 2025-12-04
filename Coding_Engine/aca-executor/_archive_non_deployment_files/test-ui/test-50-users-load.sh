#!/bin/bash

# Load Test Script: 50 Concurrent Users
# Purpose: Simulate production load and verify queue/resource usage
# Output: load_test_results.txt with detailed metrics

# Get Container App URL
echo "🔍 Fetching Container App URL..."
CONTAINER_APP_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$CONTAINER_APP_URL" ]; then
    echo "❌ Error: Could not fetch Container App URL. Make sure you are logged in to Azure CLI."
    exit 1
fi

echo "📍 Target URL: $CONTAINER_APP_URL"
echo "🚀 Starting 50 concurrent user test..."
echo "📂 Logs will be saved to: load_test_results.txt"
echo ""

# Create a temporary directory for storing individual responses
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# Initialize log file
LOG_FILE="load_test_results.txt"
echo "Timestamp | User ID | CPU (%) | Mem (MB) | Container ID | Status | Execution Time (ms)" > "$LOG_FILE"
echo "---------------------------------------------------------------------------------------------------" >> "$LOG_FILE"

# Function to run a single user test
run_user_test() {
    local user_num=$1
    local user_id="user_id_${user_num}"
    
    # Simple Python code that does some work to generate CPU/Mem usage
    local payload='{
        "language": "python",
        "code": "import time\nx = 0\nfor i in range(1000000):\n    x += i\nprint(x)",
        "test_cases": [
            {"id": "test_1", "input": "", "expected_output": "499999500000"}
        ],
        "user_id": "'"$user_id"'",
        "question_id": "load_test_q1"
    }'

    # Run curl and save response to a temp file
    # Timeout set to 60s to allow for queuing delay
    curl -s -m 60 -X POST "$CONTAINER_APP_URL/execute" \
      -H "Content-Type: application/json" \
      -d "$payload" > "$TMP_DIR/${user_id}.json"
}

# Export function and variables for subshells if needed, 
# but we are running in background loops in the same shell context.

START_TIME=$(date +%s)

# Launch 50 concurrent requests
for i in {1..50}; do
    run_user_test "$i" &
    # Small sleep to prevent local socket exhaustion if needed, but 50 is usually fine
    # sleep 0.1 
done

echo "⏳ Waiting for all 50 requests to complete..."
wait

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "✅ All requests completed in ${DURATION} seconds."
echo "Processing logs..."

# Process results and generate the log file
SUCCESS_COUNT=0
FAIL_COUNT=0

for i in {1..50}; do
    user_id="user_id_${i}"
    file="$TMP_DIR/${user_id}.json"
    
    if [ -f "$file" ]; then
        # Parse JSON using python
        # We extract timestamp, cpu, mem, container_id, status
        
        # Use python to validate and extract in one go
        read -r timestamp cpu mem container_id status exec_time <<< $(python3 -c "
import json, sys
try:
    with open('$file') as f:
        d = json.load(f)
    
    meta = d.get('metadata', {})
    summary = d.get('summary', {})
    
    ts = d.get('timestamp', 'N/A')
    cpu = meta.get('cpu_usage_percent', 0)
    mem = meta.get('memory_usage_mb', 0)
    cid = meta.get('container_id', 'unknown')
    passed = summary.get('all_passed', False)
    exec_ms = meta.get('execution_time_ms', 0)
    
    status = 'SUCCESS' if passed else 'FAILED'
    
    print(f'{ts} {cpu} {mem} {cid} {status} {exec_ms}')
except Exception:
    print('INVALID_JSON 0 0 error ERROR 0')
")
        
        if [ "$timestamp" == "INVALID_JSON" ]; then
             echo "$(date -u +"%Y-%m-%dT%H:%M:%S") | $user_id | N/A | N/A | N/A | INVALID_JSON | 0" >> "$LOG_FILE"
             ((FAIL_COUNT++))
        else
             echo "$timestamp | $user_id | $cpu | $mem | $container_id | $status | $exec_time" >> "$LOG_FILE"
             
             if [ "$status" == "SUCCESS" ]; then
                 ((SUCCESS_COUNT++))
             else
                 ((FAIL_COUNT++))
             fi
        fi
    else
        echo "$(date -u +"%Y-%m-%dT%H:%M:%S") | $user_id | N/A | N/A | N/A | TIMEOUT/ERROR | 0" >> "$LOG_FILE"
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "📊 Load Test Summary:"
echo "---------------------"
echo "Total Requests: 50"
echo "Successful: $SUCCESS_COUNT"
echo "Failed: $FAIL_COUNT"
echo "Total Duration: ${DURATION}s"
echo ""
echo "📝 Detailed logs saved to: $LOG_FILE"
echo "You can view them with: cat $LOG_FILE"

# Check for unique containers to verify load balancing
echo ""
echo "Container Distribution:"
grep "user_id" "$LOG_FILE" | awk -F'|' '{print $5}' | sort | uniq -c
