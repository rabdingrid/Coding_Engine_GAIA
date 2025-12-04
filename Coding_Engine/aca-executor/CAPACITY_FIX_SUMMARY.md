# Capacity Issue Fix Summary

## 🔍 Root Cause Identified

### Problem:
**Before FastAPI migration (Gunicorn):**
- ✅ **4 workers × 2 threads = 8 concurrent requests per replica**
- ✅ Handled multiple users easily and quickly

**After FastAPI migration (Uvicorn only):**
- ❌ **4 workers × 0 threads = 4 concurrent requests per replica**
- ❌ **50% capacity reduction!**
- ❌ Failed under load (>5 concurrent requests)

## ✅ Fixes Applied

### 1. Restored Gunicorn + Uvicorn Workers
**Changed Dockerfile.fastapi:**
```dockerfile
# Before:
CMD ["uvicorn", "executor-service:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "60"]

# After:
CMD ["gunicorn", "executor-service:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "60"]
```

**Benefits:**
- ✅ Restores **8 concurrent requests per replica** (4 workers × 2 threads)
- ✅ Maintains FastAPI async support
- ✅ Production-grade process management
- ✅ Same capacity as old Gunicorn setup

### 2. Fixed Variable Scope Bug
**Fixed in executor-service-fastapi.py:**
- Changed `detect_error_type(execution_result, timeout)` to `detect_error_type(execution_result, exec_timeout)`
- Ensures `exec_timeout` parameter is used instead of outer scope `timeout` variable

## 📊 Capacity Comparison

| Setup | Workers | Threads | Concurrent/Replica | Total (2 replicas) |
|-------|---------|---------|-------------------|---------------------|
| **Old (Gunicorn)** | 4 | 2 | **8** | **16** |
| **New (Uvicorn only)** | 4 | 0 | **4** | **8** |
| **Fixed (Gunicorn + Uvicorn)** | 4 | 2 | **8** | **16** ✅ |

## 🐛 Remaining Issue

### HTTP 400 Errors Under High Load
- **Single requests**: ✅ Work perfectly
- **Multiple simultaneous requests**: ❌ HTTP 400 errors

**Possible causes:**
1. Thread-safety issue with `block_network_access()` / `restore_network_access()`
2. Shared state in parallel execution
3. Rate limiting kicking in
4. Database connection pool exhaustion

**Next steps:**
- Investigate thread-safety of network blocking mechanism
- Check if rate limiting is too aggressive
- Monitor database connection pool usage
- Test with smaller concurrent loads (5, 8, 10 users)

## 📝 Files Changed

1. **Dockerfile.fastapi**: Switched to Gunicorn + Uvicorn workers
2. **requirements-fastapi.txt**: Added `gunicorn==21.2.0`
3. **executor-service-fastapi.py**: Fixed timeout variable scope

## 🚀 Deployment

- **Image**: `executor-fastapi:v27-fix-timeout-scope`
- **Status**: Deployed ✅
- **Configuration**: Gunicorn (4 workers × 2 threads) + Uvicorn workers

## 🧪 Testing Results

### Single Request:
- ✅ **Success**: HTTP 200
- ✅ **Execution**: ~14ms
- ✅ **All tests passed**

### Multiple Requests (10 users):
- ⚠️ **Status**: HTTP 400 errors
- ⚠️ **Issue**: Needs further investigation

## 💡 Recommendations

1. **For immediate use**: System works well for <5 concurrent requests
2. **For production**: Need to fix HTTP 400 errors under high load
3. **For 200-300 users**: 
   - Fix remaining concurrency issues
   - Scale to 30-50 replicas (30 × 8 = 240 concurrent capacity)
   - Monitor and adjust based on actual load

## 📅 Date
December 4, 2025

