# 🧪 Testing FastAPI Endpoints Locally

## Prerequisites

1. **Install FastAPI dependencies**:
   ```bash
   cd Coding_Engine/aca-executor
   pip install -r requirements-fastapi.txt
   ```

2. **Set up database** (optional, for /submit endpoint):
   ```bash
   export DATABASE_URL="postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require"
   ```

## Start FastAPI Service

```bash
cd Coding_Engine/aca-executor
uvicorn executor-service-fastapi:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at: `http://localhost:8000`

## Test Methods

### Method 1: Python Script (Recommended)

```bash
cd Coding_Engine/aca-executor/test-ui
python3 test-fastapi-python.py
```

This script will:
- ✅ Test health endpoint
- ✅ Test `/run` with 20 sample test cases
- ✅ Test `/runall` with 20 test cases
- ✅ Test `/submit` with 20 test cases + DB save
- ✅ Test error detection (syntax errors)

### Method 2: Bash Script

```bash
cd Coding_Engine/aca-executor/test-ui
./test-fastapi-endpoints.sh
```

### Method 3: Manual curl Commands

#### Test `/run` endpoint:

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "a = int(input())\nb = int(input())\nprint(a + b)",
    "sample_test_cases": [
      {"id": "test_1", "input": "5\n3", "expected_output": "8"},
      {"id": "test_2", "input": "10\n20", "expected_output": "30"}
    ],
    "user_id": "test_user",
    "question_id": "test_q1",
    "timeout": 5
  }'
```

#### Test `/runall` endpoint:

```bash
curl -X POST http://localhost:8000/runall \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "a = int(input())\nb = int(input())\nprint(a + b)",
    "test_cases": [
      {"id": "test_1", "input": "5\n3", "expected_output": "8"},
      {"id": "test_2", "input": "10\n20", "expected_output": "30"}
    ],
    "sample_test_cases": [],
    "timeout": 5
  }'
```

#### Test `/submit` endpoint:

```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "a = int(input())\nb = int(input())\nprint(a + b)",
    "test_cases": [
      {"id": "test_1", "input": "5\n3", "expected_output": "8"},
      {"id": "test_2", "input": "10\n20", "expected_output": "30"}
    ],
    "user_id": "test_user",
    "question_id": "test_q1",
    "timeout": 5
  }'
```

## Expected Output

### Successful Response:

```json
{
  "execution_id": "uuid-here",
  "summary": {
    "total_tests": 20,
    "passed": 20,
    "failed": 0,
    "all_passed": true,
    "pass_percentage": 100.0
  },
  "test_results": [
    {
      "test_case_id": "test_1",
      "test_case_number": 1,
      "input": "5\n3",
      "expected_output": "8",
      "actual_output": "8",
      "error": null,
      "status": "passed",
      "passed": true,
      "execution_time_ms": 150,
      "cpu_usage_percent": 25.5,
      "memory_usage_bytes": 1024000
    }
  ],
  "metadata": {
    "replica": "unknown",
    "container_id": "unknown",
    "timeout": 5,
    "execution_time_ms": 3000,
    "cpu_usage_percent": 25.5,
    "memory_usage_bytes": 1024000,
    "memory_usage_mb": 1.0,
    "endpoint": "run",
    "test_type": "sample"
  },
  "timestamp": "2025-01-XX..."
}
```

## Error Status Types

The response will include one of these statuses for each test case:

- `passed` - Test case passed
- `failed` - Output mismatch
- `tle` - Time Limit Exceeded
- `mle` - Memory Limit Exceeded
- `syntax_error` - Compilation/syntax error
- `runtime_error` - Runtime exception
- `error` - General error

## Troubleshooting

### Service not running:
```
❌ Service is not running!
   Start the service with: uvicorn executor-service-fastapi:app --reload
```

### Connection refused:
- Check if service is running on port 8000
- Try: `curl http://localhost:8000/health`

### Database connection error:
- `/submit` endpoint will still work but won't save to DB
- Check `DATABASE_URL` environment variable
- Check database firewall rules

## Next Steps

After local testing passes:
1. Build Docker image: `docker build -f Dockerfile.fastapi -t executor-fastapi .`
2. Test Docker image locally
3. Push to container registry
4. Deploy to production
5. Test production endpoints

