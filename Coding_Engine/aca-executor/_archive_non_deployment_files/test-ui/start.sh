#!/bin/bash

echo "🚀 Starting Code Executor Test UI Server..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if port 3000 is in use
if lsof -ti:3000 > /dev/null 2>&1; then
    echo "⚠️  Port 3000 is already in use!"
    echo "   Please stop the existing server or use a different port."
    echo ""
    read -p "Kill existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill -9 $(lsof -ti:3000) 2>/dev/null
        echo "✅ Killed existing process"
        sleep 2
    else
        echo "❌ Exiting..."
        exit 1
    fi
fi

echo "✅ Starting server on http://localhost:3000"
echo "📊 Database: PostgreSQL (Railway)"
echo "🔧 Executor: Azure Container Apps"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm start
