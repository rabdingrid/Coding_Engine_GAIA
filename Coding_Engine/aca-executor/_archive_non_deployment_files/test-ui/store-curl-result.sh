#!/bin/bash
# Helper script to store curl execution results in monitoring dashboard
# Usage: ./store-curl-result.sh <execution_response_json>

API_BASE_URL="http://localhost:3001/api"

if [ -z "$1" ]; then
    echo "Usage: ./store-curl-result.sh <execution_response_json>"
    echo ""
    echo "Example:"
    echo "  RESPONSE=\$(curl -X POST \"https://.../execute\" ...)"
    echo "  echo \$RESPONSE | ./store-curl-result.sh"
    echo ""
    echo "Or pipe directly:"
    echo "  curl -X POST \"https://.../execute\" ... | ./store-curl-result.sh"
    exit 1
fi

# Read JSON from stdin or argument
if [ "$1" = "-" ] || [ -z "$1" ]; then
    JSON_INPUT=$(cat)
else
    JSON_INPUT="$1"
fi

# Store in monitoring dashboard
curl -s -X POST "${API_BASE_URL}/monitoring/store" \
  -H "Content-Type: application/json" \
  -d "$JSON_INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('success'):
        print('✅ Execution stored in monitoring dashboard')
    else:
        print('❌ Failed to store:', d.get('error', 'Unknown error'))
except:
    print('❌ Error parsing response')
"


