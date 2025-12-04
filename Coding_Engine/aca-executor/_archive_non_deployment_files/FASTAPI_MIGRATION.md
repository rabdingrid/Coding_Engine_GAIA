# 🚀 FastAPI Migration Guide

## Overview

This document describes the migration from Flask to FastAPI with enhanced endpoints for the coding engine.

## Branch Information

- **Branch**: `fastapi-migration`
- **Base Branch**: `main` (Flask version preserved)
- **Repository**: https://github.com/rabdingrid/Coding_Engine_GAIA

## What Changed

### 1. Framework Migration
- **From**: Flask + Gunicorn
- **To**: FastAPI + Uvicorn
- **Benefits**: 
  - Better async support
  - Automatic API documentation
  - Type validation with Pydantic
  - Better performance

### 2. New Endpoints

#### POST `/run`
- **Purpose**: Run code with sample test cases only
- **Input**: 
  ```json
  {
    "language": "python",
    "code": "complete code (user code + boilerplate merged)",
    "sample_test_cases": [
      {
        "id": "test_1",
        "input": "...",
        "expected_output": "..."
      }
    ],
    "user_id": "optional",
    "question_id": "optional",
    "timeout": 5
  }
  ```
- **Output**: Execution results with status (passed/failed/tle/mle/syntax_error/runtime_error)

#### POST `/runall`
- **Purpose**: Run code with all test cases (excluding sample)
- **Input**: 
  ```json
  {
    "language": "python",
    "code": "complete code (user code + boilerplate merged)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "...",
        "expected_output": "..."
      }
    ],
    "sample_test_cases": [],  // For reference only, not executed
    "user_id": "optional",
    "question_id": "optional",
    "timeout": 5
  }
  ```
- **Output**: Execution results for all test cases

#### POST `/submit`
- **Purpose**: Submit code with all test cases and save to database
- **Input**: 
  ```json
  {
    "language": "python",
    "code": "complete code (user code + boilerplate merged)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "...",
        "expected_output": "..."
      }
    ],
    "sample_test_cases": [],  // For reference only
    "user_id": "required",
    "question_id": "required",
    "candidate_id": "optional",
    "timeout": 5
  }
  ```
- **Output**: Execution results + submission saved to database
- **Database**: Creates `submissions` table automatically

### 3. Enhanced Error Detection

All endpoints now return detailed error status:
- `passed`: Test case passed
- `failed`: Output mismatch
- `tle`: Time Limit Exceeded
- `mle`: Memory Limit Exceeded
- `syntax_error`: Compilation/syntax error
- `runtime_error`: Runtime exception
- `error`: General error

### 4. Response Format

```json
{
  "execution_id": "uuid",
  "summary": {
    "total_tests": 10,
    "passed": 8,
    "failed": 2,
    "all_passed": false,
    "pass_percentage": 80.0
  },
  "test_results": [
    {
      "test_case_id": "test_1",
      "test_case_number": 1,
      "input": "...",
      "expected_output": "...",
      "actual_output": "...",
      "error": null,
      "status": "passed",
      "passed": true,
      "execution_time_ms": 150,
      "cpu_usage_percent": 25.5,
      "memory_usage_bytes": 1024000
    }
  ],
  "metadata": {
    "replica": "replica-1",
    "container_id": "container-123",
    "timeout": 5,
    "execution_time_ms": 1500,
    "cpu_usage_percent": 25.5,
    "memory_usage_bytes": 1024000,
    "memory_usage_mb": 1.0,
    "endpoint": "run",
    "test_type": "sample"
  },
  "timestamp": "2025-01-XX..."
}
```

## Files Changed

### New Files
1. `executor-service-fastapi.py` - FastAPI implementation
2. `Dockerfile.fastapi` - Dockerfile for FastAPI deployment
3. `requirements-fastapi.txt` - FastAPI dependencies

### Preserved Files (on main branch)
- `executor-service-secure.py` - Original Flask version (safe to revert)
- `Dockerfile` - Original Dockerfile
- `requirements.txt` - Original requirements

## Deployment

### Option 1: Deploy FastAPI Version (Replace Old)
```bash
# Build new image
docker build -f Dockerfile.fastapi -t your-registry/executor-fastapi:v3.0.0 .

# Push to registry
docker push your-registry/executor-fastapi:v3.0.0

# Update Terraform to use new image
# Or update Container App directly
```

### Option 2: Keep Both Versions
- Deploy FastAPI version to new Container App
- Keep Flask version running on old Container App
- Gradually migrate traffic

### Option 3: Revert to Flask (If Needed)
```bash
# Switch back to main branch
git checkout main

# Deploy Flask version
# (Original files are preserved)
```

## Database Schema

The `/submit` endpoint automatically creates a `submissions` table:

```sql
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    submission_id VARCHAR(255) UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    question_id VARCHAR(255) NOT NULL,
    language VARCHAR(50) NOT NULL,
    code TEXT NOT NULL,
    test_results JSONB NOT NULL,
    summary JSONB NOT NULL,
    execution_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

### Test `/run` endpoint:
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "sample_test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ]
  }'
```

### Test `/runall` endpoint:
```bash
curl -X POST http://localhost:8000/runall \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ]
  }'
```

### Test `/submit` endpoint:
```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "user123",
    "question_id": "q1"
  }'
```

## Migration Checklist

- [x] Create `fastapi-migration` branch
- [x] Stage current Flask code on `main` branch
- [x] Convert to FastAPI
- [x] Implement `/run` endpoint
- [x] Implement `/runall` endpoint
- [x] Implement `/submit` endpoint with DB integration
- [x] Add enhanced error detection (TLE, MLE, syntax errors)
- [x] Create FastAPI Dockerfile
- [x] Create FastAPI requirements
- [x] Push to GitHub
- [ ] Test all endpoints locally
- [ ] Deploy to staging
- [ ] Test in production
- [ ] Migrate traffic from Flask to FastAPI
- [ ] Monitor performance
- [ ] Update frontend to use new endpoints

## Rollback Plan

If issues occur:
1. Switch Terraform/Container App back to Flask image
2. Or merge `main` branch back to production
3. All original Flask code is preserved on `main` branch

## Next Steps

1. **Test locally**: Run FastAPI service and test all endpoints
2. **Update frontend**: Modify frontend to use new endpoint structure
3. **Deploy**: Deploy FastAPI version to staging first
4. **Monitor**: Watch for any issues
5. **Migrate**: Gradually move traffic to FastAPI

## Support

- **Branch**: `fastapi-migration`
- **Original Code**: Preserved on `main` branch
- **Issues**: Create GitHub issue or revert to `main` branch

