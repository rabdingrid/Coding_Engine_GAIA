# 🚀 Quick Start - Local Testing Guide

## Step 1: Install Dependencies

```bash
cd Coding_Engine/aca-executor
pip install -r requirements-fastapi.txt
```

Required packages:
- `fastapi==0.104.1`
- `uvicorn[standard]==0.24.0`
- `pydantic==2.5.0`
- `slowapi==0.1.9`
- `asyncpg==0.29.0`
- `psutil==5.9.8`

## Step 2: Start FastAPI Service

**Terminal 1:**
```bash
cd Coding_Engine/aca-executor
uvicorn executor-service-fastapi:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
✅ Database connection pool created
INFO:     Application startup complete.
```

## Step 3: Run Tests

**Terminal 2:**

### Option A: Comprehensive Test (All Languages)
```bash
cd Coding_Engine/aca-executor/test-ui
python3 test-all-languages-fastapi.py
```

This will test:
- ✅ Python, Java, C++, JavaScript, C#
- ✅ 4 problems per language (Sum, Max Array, Reverse String, Factorial)
- ✅ 3 endpoints per problem (/run, /runall, /submit)
- ✅ 20 test cases per endpoint
- ⏱️ Takes ~5-10 minutes

### Option B: Quick Test (Python Only)
```bash
cd Coding_Engine/aca-executor/test-ui
python3 test-fastapi-python.py
```

This will test:
- ✅ Health check
- ✅ /run endpoint (20 test cases)
- ✅ /runall endpoint (20 test cases)
- ✅ /submit endpoint (20 test cases)
- ✅ Error detection
- ⏱️ Takes ~1-2 minutes

### Option C: Bash Script
```bash
cd Coding_Engine/aca-executor/test-ui
./test-fastapi-endpoints.sh
```

## Expected Output

### Successful Test:
```
🧪 Comprehensive FastAPI Testing - All Languages
======================================================================
Base URL: http://localhost:8000
Testing: Python, Java, C++, JavaScript, C#
Problems: Sum, Max Array, Reverse String, Factorial
Endpoints: /run, /runall, /submit
======================================================================
✅ Health check passed!
   Status: healthy
   Version: 3.0.0

======================================================================
🔤 Testing PYTHON
======================================================================

📝 Problem: Sum of Two Numbers (sum)
----------------------------------------------------------------------
   Testing /RUN endpoint...
   ✅ 10/10 passed, 0 failed (took 0.45s)
   Testing /RUNALL endpoint...
   ✅ 10/10 passed, 0 failed (took 0.42s)
   Testing /SUBMIT endpoint...
   ✅ 20/20 passed, 0 failed (took 0.85s)

📊 PYTHON Summary:
----------------------------------------------------------------------
   ✅ /run - sum
   ✅ /runall - sum
   ✅ /submit - sum
   ...

🎉 All languages passed all tests!
```

## Troubleshooting

### Issue: ModuleNotFoundError
```bash
# Install dependencies
pip install -r requirements-fastapi.txt
```

### Issue: Port 8000 already in use
```bash
# Use different port
uvicorn executor-service-fastapi:app --reload --port 8001

# Update BASE_URL in test script
export BASE_URL="http://localhost:8001"
```

### Issue: Database connection error
- `/submit` endpoint will still work but won't save to DB
- Set `DATABASE_URL` environment variable if needed
- For testing, DB is optional

### Issue: Service not responding
```bash
# Check if service is running
curl http://localhost:8000/health

# Check logs in Terminal 1 for errors
```

## Test Coverage

| Language | Problems | Endpoints | Test Cases | Total Tests |
|----------|----------|-----------|------------|-------------|
| Python   | 4        | 3         | 20 each    | 240         |
| Java     | 4        | 3         | 20 each    | 240         |
| C++      | 4        | 3         | 20 each    | 240         |
| JavaScript | 4      | 3         | 20 each    | 240         |
| C#       | 4        | 3         | 20 each    | 240         |
| **Total** | **20**   | **15**    | **300**    | **1200**    |

## Next Steps

After local testing passes:
1. ✅ Build Docker image
2. ✅ Test Docker image locally
3. ✅ Push to container registry
4. ✅ Deploy to production
5. ✅ Run production tests

