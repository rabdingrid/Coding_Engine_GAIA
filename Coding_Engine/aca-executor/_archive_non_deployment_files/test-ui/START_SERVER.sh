#!/bin/bash
# Quick start script for the test UI server

cd "$(dirname "$0")"

echo "=== Starting Code Executor Test UI Server ==="
echo ""

# Kill any existing server on port 3001
lsof -ti:3001 | xargs kill -9 2>/dev/null
sleep 1

# Start server
echo "Starting server on port 3001..."
node server.js > server.log 2>&1 &
SERVER_PID=$!

sleep 3

# Check if server started
if lsof -ti:3001 > /dev/null; then
    echo "✅ Server started successfully!"
    echo ""
    echo "🌐 Open in browser:"
    echo "  - Main UI: http://localhost:3001"
    echo "  - Monitoring: http://localhost:3001/monitoring-dashboard.html"
    echo ""
    echo "📊 Server PID: $SERVER_PID"
    echo "📝 Logs: server.log"
    echo ""
    echo "To stop server: kill $SERVER_PID"
else
    echo "❌ Server failed to start. Check server.log for errors."
    cat server.log
fi


