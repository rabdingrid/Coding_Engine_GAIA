# Capacity Issue Analysis: Gunicorn vs FastAPI/Uvicorn

## 🔍 Problem Identified

**Before (Gunicorn):**
- **Workers**: 4 workers × 2 threads = **8 concurrent requests per replica**
- **Configuration**: `gunicorn --workers 4 --threads 2 --worker-class sync`
- **Capacity**: 8 concurrent requests per replica ✅

**After (FastAPI/Uvicorn):**
- **Workers**: 4 workers (no threads) = **4 concurrent requests per replica**
- **Configuration**: `uvicorn --workers 4`
- **Capacity**: 4 concurrent requests per replica ❌

## 📊 Capacity Comparison

| Setup | Workers | Threads | Concurrent per Replica | Total (2 replicas) |
|-------|---------|---------|------------------------|---------------------|
| **Old (Gunicorn)** | 4 | 2 | **8** | **16** |
| **New (Uvicorn)** | 4 | 0 | **4** | **8** |
| **Gap** | - | - | **-50%** | **-50%** |

## 🐛 Additional Issues

1. **Blocking Code Execution**: `execute_code()` is synchronous/blocking, which blocks the async event loop in Uvicorn workers
2. **Variable Scope Bug**: The `start_time` variable issue in parallel execution causes failures under load
3. **Reduced Concurrency**: Only 4 workers instead of 8 (4 workers × 2 threads)

## ✅ Solution Options

### Option 1: Use Gunicorn with Uvicorn Workers (Recommended)
**Best of both worlds:**
- Gunicorn for process management and threading
- Uvicorn workers for async FastAPI support
- **Configuration**: `gunicorn --workers 4 --threads 2 --worker-class uvicorn.workers.UvicornWorker`

**Benefits:**
- ✅ 4 workers × 2 threads = 8 concurrent requests per replica
- ✅ Async support for FastAPI
- ✅ Production-grade process management
- ✅ Restores original capacity

### Option 2: Increase Uvicorn Workers
**Simple but less efficient:**
- **Configuration**: `uvicorn --workers 8`
- **Capacity**: 8 concurrent requests per replica

**Drawbacks:**
- ⚠️ More memory usage (8 processes vs 4 processes × 2 threads)
- ⚠️ Still has blocking code execution issue

### Option 3: Fix Variable Scope + Increase Workers
- Fix the `start_time` variable bug
- Increase to 8 workers
- **Capacity**: 8 concurrent requests per replica

## 🎯 Recommended Fix

**Use Gunicorn with Uvicorn workers:**
```dockerfile
CMD ["gunicorn", "executor-service:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "60"]
```

This will:
- ✅ Restore 8 concurrent requests per replica
- ✅ Maintain FastAPI async support
- ✅ Fix the capacity issue
- ✅ Work with existing FastAPI code

