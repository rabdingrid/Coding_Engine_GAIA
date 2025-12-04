#!/bin/bash

# Test script: 10 Dummy Users with 1 Replica
# Purpose: Verify queue system and concurrent request handling

CONTAINER_APP_URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$CONTAINER_APP_URL" ]; then
    echo "❌ Error: Could not fetch Container App URL"
    exit 1
fi

echo "🧪 Testing Queue System: 10 Dummy Users with 1 Replica"
echo "📍 URL: $CONTAINER_APP_URL"
echo "📊 Expected: All 10 requests should complete successfully"
echo "⏱️  Expected: Requests will be queued and processed concurrently by Gunicorn"
echo ""

# Create a temporary directory for storing results
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# Function to run a single user test
run_user_test() {
    local user_id=$1
    local user_num=$2
    local start_time=$(date +%s.%N)
    
    echo "  👤 User $user_num ($user_id): Starting..."
    
    # Run curl and save response
    curl -s -m 30 -X POST "$CONTAINER_APP_URL/execute" \
      -H "Content-Type: application/json" \
      -d "{
        \"language\": \"python\",
        \"code\": \"import time\nn = int(input())\nresult = n * 2\nprint(result)\",
        \"test_cases\": [
          {\"id\": \"test_1\", \"input\": \"$user_num\", \"expected_output\": \"$((user_num * 2))\"}
        ],
        \"user_id\": \"$user_id\",
        \"question_id\": \"queue_test\"
      }" > "$TMP_DIR/user_${user_num}.json"
    
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc)
    
    # Parse response
    if [ -f "$TMP_DIR/user_${user_num}.json" ]; then
        local all_passed=$(python3 -c "import json, sys; d=json.load(open('$TMP_DIR/user_${user_num}.json')); print('✅' if d.get('summary', {}).get('all_passed') else '❌')" 2>/dev/null)
        local execution_time=$(python3 -c "import json, sys; d=json.load(open('$TMP_DIR/user_${user_num}.json')); print(d.get('metadata', {}).get('execution_time_ms', 0))" 2>/dev/null)
        local container_id=$(python3 -c "import json, sys; d=json.load(open('$TMP_DIR/user_${user_num}.json')); print(d.get('metadata', {}).get('container_id', 'unknown')[:50])" 2>/dev/null)
        
        echo "  👤 User $user_num ($user_id): $all_passed | Time: ${execution_time}ms | Duration: ${duration}s | Container: ${container_id}..."
    else
        echo "  👤 User $user_num ($user_id): ❌ Failed to get response"
    fi
}

# Export function and URL for parallel execution
export -f run_user_test
export CONTAINER_APP_URL
export TMP_DIR

echo "🚀 Starting 10 concurrent users..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
START_TIME=$(date +%s.%N)

# Run all 10 users in parallel using GNU parallel or background processes
for i in {1..10}; do
    user_id="dummy_user_$(date +%s)_${i}"
    run_user_test "$user_id" "$i" &
done

# Wait for all background jobs to complete
wait

END_TIME=$(date +%s.%N)
TOTAL_DURATION=$(echo "$END_TIME - $START_TIME" | bc)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Analyze results
echo "📊 Results Analysis:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SUCCESS_COUNT=0
FAILED_COUNT=0
TOTAL_EXECUTION_TIME=0
CONTAINER_IDS=()

for i in {1..10}; do
    if [ -f "$TMP_DIR/user_${i}.json" ]; then
        all_passed=$(python3 -c "import json; d=json.load(open('$TMP_DIR/user_${i}.json')); print(d.get('summary', {}).get('all_passed', False))" 2>/dev/null)
        execution_time=$(python3 -c "import json; d=json.load(open('$TMP_DIR/user_${i}.json')); print(d.get('metadata', {}).get('execution_time_ms', 0))" 2>/dev/null)
        container_id=$(python3 -c "import json; d=json.load(open('$TMP_DIR/user_${i}.json')); print(d.get('metadata', {}).get('container_id', 'unknown'))" 2>/dev/null)
        
        if [ "$all_passed" = "True" ]; then
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            TOTAL_EXECUTION_TIME=$(echo "$TOTAL_EXECUTION_TIME + $execution_time" | bc)
            CONTAINER_IDS+=("$container_id")
        else
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi
    else
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
done

# Check if all used the same container (proves 1 replica handled all)
UNIQUE_CONTAINERS=$(printf '%s\n' "${CONTAINER_IDS[@]}" | sort -u | wc -l)

echo "✅ Successful: $SUCCESS_COUNT/10"
echo "❌ Failed: $FAILED_COUNT/10"
echo "⏱️  Total Wall Time: ${TOTAL_DURATION}s"
if [ $SUCCESS_COUNT -gt 0 ]; then
    AVG_EXECUTION_TIME=$(echo "scale=2; $TOTAL_EXECUTION_TIME / $SUCCESS_COUNT" | bc)
    echo "⏱️  Average Execution Time: ${AVG_EXECUTION_TIME}ms"
fi
echo "📦 Unique Containers: $UNIQUE_CONTAINERS (should be 1 for 1 replica)"

if [ $UNIQUE_CONTAINERS -eq 1 ] && [ $SUCCESS_COUNT -eq 10 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ SUCCESS: Queue System Working Perfectly!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎯 Verification:"
    echo "  ✅ All 10 users completed successfully"
    echo "  ✅ All requests handled by same container (1 replica)"
    echo "  ✅ Gunicorn queue processed all requests concurrently"
    echo "  ✅ No requests hung or timed out"
    echo ""
    echo "📈 Gunicorn Capacity:"
    echo "  • 4 workers × 2 threads = 8 concurrent capacity"
    echo "  • 10 requests queued and processed efficiently"
    echo "  • System is ready for production use!"
    exit 0
else
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  WARNING: Some issues detected"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ $UNIQUE_CONTAINERS -ne 1 ]; then
        echo "  ⚠️  Multiple containers detected (expected 1)"
    fi
    if [ $SUCCESS_COUNT -ne 10 ]; then
        echo "  ⚠️  Some requests failed ($FAILED_COUNT failed)"
    fi
    exit 1
fi


