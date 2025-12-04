#!/bin/bash
# Wrapper script to run curl command and automatically store result in monitoring dashboard
# Usage: ./run-and-monitor.sh <curl_command_without_curl>

API_BASE_URL="http://localhost:3001/api"
EXECUTOR_URL="https://ai-ta-ra-code-executor2--0000021.happypond-428960e8.eastus2.azurecontainerapps.io"

# Check if Node.js server is running
if ! curl -s "${API_BASE_URL%/api}/health" > /dev/null 2>&1; then
    echo "⚠️  Warning: Node.js server might not be running on port 3001"
    echo "   Start it with: cd test-ui && npm start"
    echo ""
fi

# Get the curl command from arguments (everything after script name)
CURL_CMD="$@"

if [ -z "$CURL_CMD" ]; then
    echo "Usage: ./run-and-monitor.sh <curl_command>"
    echo ""
    echo "Example:"
    echo "  ./run-and-monitor.sh -X POST \"$EXECUTOR_URL/execute\" -H \"Content-Type: application/json\" -d '{\"language\":\"java\",\"code\":\"...\",\"test_cases\":[...],\"user_id\":\"user_1\",\"question_id\":\"15\"}'"
    exit 1
fi

echo "🚀 Executing request..."
echo ""

# Execute the curl command and capture response
RESPONSE=$(eval curl -s $CURL_CMD)

# Check if response is valid JSON
if ! echo "$RESPONSE" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
    echo "❌ Error: Invalid JSON response"
    echo "$RESPONSE" | head -20
    exit 1
fi

# Display the response
echo "✅ Execution completed!"
echo ""
echo "Response:"
echo "$RESPONSE" | python3 -m json.tool | head -30
echo ""

# Store in monitoring dashboard
echo "📊 Storing in monitoring dashboard..."
STORE_RESULT=$(echo "$RESPONSE" | curl -s -X POST "${API_BASE_URL}/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @-)

if echo "$STORE_RESULT" | python3 -c "import sys, json; d=json.load(sys.stdin); exit(0 if d.get('success') else 1)" 2>/dev/null; then
    echo "✅ Stored successfully in monitoring dashboard!"
    echo ""
    echo "💡 Open monitoring-dashboard.html to see the result"
    echo "   (Auto-refreshes every 5 seconds)"
else
    echo "⚠️  Warning: Failed to store in monitoring dashboard"
    echo "   Response: $STORE_RESULT"
    echo ""
    echo "   Make sure Node.js server is running: cd test-ui && npm start"
fi


