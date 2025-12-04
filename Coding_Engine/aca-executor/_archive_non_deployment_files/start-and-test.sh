#!/bin/bash

# Start FastAPI Service and Run Tests
# This script will:
# 1. Install dependencies
# 2. Start the FastAPI service
# 3. Run quick test
# 4. Run full test

set -e

cd "$(dirname "$0")"
BASE_DIR="$(pwd)"

echo "🚀 FastAPI Testing Setup"
echo "========================"
echo ""

# Step 1: Install dependencies
echo "📦 Step 1: Installing dependencies..."
if [ -f "requirements-fastapi.txt" ]; then
    pip3 install -q -r requirements-fastapi.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  requirements-fastapi.txt not found, installing manually..."
    pip3 install -q fastapi "uvicorn[standard]" pydantic slowapi asyncpg psutil
    echo "✅ Dependencies installed"
fi

# Step 2: Check if service is already running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Service already running on port 8000"
    SERVICE_RUNNING=true
else
    SERVICE_RUNNING=false
fi

# Step 3: Start service if not running
if [ "$SERVICE_RUNNING" = false ]; then
    echo ""
    echo "🚀 Step 2: Starting FastAPI service..."
    echo "   This will run in the background"
    echo ""
    
    # Start service in background
    python3 -m uvicorn executor-service-fastapi:app --host 0.0.0.0 --port 8000 > /tmp/fastapi-service.log 2>&1 &
    SERVICE_PID=$!
    echo $SERVICE_PID > /tmp/fastapi-service.pid
    echo "✅ Service starting (PID: $SERVICE_PID)"
    
    # Wait for service to be ready
    echo "⏳ Waiting for service to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Service is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "❌ Service failed to start. Check logs: tail -f /tmp/fastapi-service.log"
            exit 1
        fi
        echo "   Attempt $i/30..."
        sleep 1
    done
fi

# Step 4: Run quick test
echo ""
echo "🧪 Step 3: Running QUICK TEST (Python Only)..."
echo "=============================================="
cd test-ui
python3 test-fastapi-python.py
QUICK_TEST_RESULT=$?

# Step 5: Run full test
if [ $QUICK_TEST_RESULT -eq 0 ]; then
    echo ""
    echo ""
    echo "🧪 Step 4: Running FULL TEST (All Languages)..."
    echo "=============================================="
    python3 test-all-languages-fastapi.py
    FULL_TEST_RESULT=$?
else
    echo ""
    echo "⚠️  Quick test failed. Skipping full test."
    FULL_TEST_RESULT=1
fi

# Summary
echo ""
echo "=========================================="
echo "📊 TEST SUMMARY"
echo "=========================================="
if [ $QUICK_TEST_RESULT -eq 0 ]; then
    echo "✅ Quick Test: PASSED"
else
    echo "❌ Quick Test: FAILED"
fi

if [ $FULL_TEST_RESULT -eq 0 ]; then
    echo "✅ Full Test: PASSED"
else
    echo "❌ Full Test: FAILED"
fi

# Cleanup option
echo ""
read -p "Stop the FastAPI service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f /tmp/fastapi-service.pid ]; then
        kill $(cat /tmp/fastapi-service.pid) 2>/dev/null || true
        rm /tmp/fastapi-service.pid
        echo "✅ Service stopped"
    fi
fi

exit $((QUICK_TEST_RESULT + FULL_TEST_RESULT))

