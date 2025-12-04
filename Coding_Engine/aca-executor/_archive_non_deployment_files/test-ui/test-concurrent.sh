#!/bin/bash
# Concurrent Multi-User Test Script
# Run multiple requests simultaneously to test if 1 container can handle concurrent load

# Get Container App URL
URL=$(az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query 'properties.latestRevisionFqdn' -o tsv 2>/dev/null | sed 's|^|https://|')

if [ -z "$URL" ]; then
    echo "❌ Error: Could not get Container App URL"
    exit 1
fi

echo "🧪 Concurrent Multi-User Test"
echo "URL: $URL"
echo "Testing: 5 concurrent requests to 1 container"
echo ""

# Function to run a single test
run_test() {
    local user_num=$1
    local user_id="user_${user_num}_$(date +%s)_$$"
    
    echo "[User $user_num] Starting test..."
    START_TIME=$(date +%s%N)
    
    RESPONSE=$(curl -s -m 60 -X POST "$URL/execute" \
      -H "Content-Type: application/json" \
      -d "{
        \"language\": \"java\",
        \"code\": \"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }\",
        \"test_cases\": [
          {\"id\": \"test_1\", \"input\": \"3\", \"expected_output\": \"3\"},
          {\"id\": \"test_2\", \"input\": \"4\", \"expected_output\": \"5\"}
        ],
        \"user_id\": \"$user_id\",
        \"question_id\": \"15\"
      }")
    
    END_TIME=$(date +%s%N)
    ELAPSED=$((($END_TIME - $START_TIME) / 1000000))
    
    # Parse response
    PASSED=$(echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print('✅' if d.get('summary', {}).get('all_passed') else '❌')" 2>/dev/null)
    CONTAINER_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('metadata', {}).get('container_id', 'unknown'))" 2>/dev/null)
    
    echo "[User $user_num] $PASSED - Time: ${ELAPSED}ms - Container: $CONTAINER_ID"
}

# Run 5 concurrent tests
echo "Starting 5 concurrent requests..."
echo ""

# Run tests in background
for i in {1..5}; do
    run_test $i &
done

# Wait for all background jobs
wait

echo ""
echo "✅ All concurrent tests completed!"
echo ""
echo "Check if all requests used the same container ID (1 container handling multiple users)"


