#!/bin/bash

# Wrapper script for load testing
# Usage: ./run-load-test.sh [number_of_users] [language]

NUM_USERS=${1:-30}
LANGUAGE=${2:-python}

echo "🚀 Starting Load Test"
echo "   Users: $NUM_USERS"
echo "   Language: $LANGUAGE"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    exit 1
fi

# Check if requests module is available
if ! python3 -c "import requests" 2>/dev/null; then
    echo "⚠️  Installing requests module..."
    pip3 install requests --quiet
fi

# Run the load test
python3 load-test-multi-user.py -n "$NUM_USERS" -l "$LANGUAGE"

