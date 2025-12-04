#!/bin/bash

set -e

echo "🚀 Starting Coding Engine UI..."
echo ""

# Check if asyncpg is installed
if ! python3 -c "import asyncpg" 2>/dev/null; then
    echo "⚠️  asyncpg not found. Installing..."
    python3 -m pip install --user asyncpg || {
        echo "❌ Failed to install asyncpg. Please install it manually:"
        echo "   python3 -m pip install --user asyncpg"
        echo ""
        echo "Or use a virtual environment:"
        echo "   python3 -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install asyncpg"
        exit 1
    }
fi

# Start questions API in background
echo "📡 Starting Questions API server (port 3002)..."
python3 questions-api.py &
QUESTIONS_API_PID=$!

# Wait a moment for API to start
sleep 2

# Start frontend server
echo "🌐 Starting Frontend server (port 3001)..."
echo ""
echo "✅ UI is ready!"
echo "   Frontend: http://localhost:3001"
echo "   Questions API: http://localhost:3002"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap Ctrl+C to kill background process
trap "kill $QUESTIONS_API_PID 2>/dev/null; exit" INT TERM

# Start frontend server (foreground)
python3 server.py

# Cleanup on exit
kill $QUESTIONS_API_PID 2>/dev/null

