# Performance Issues Analysis - 500 User Load Test

## 🔍 Root Causes Identified

### 1. **Out of Memory (OOM) Errors** ❌
**Problem**: Workers were being killed by the system due to memory exhaustion
```
ERROR: Worker (pid:8119) was sent SIGKILL! Perhaps out of memory?
ERROR: Worker (pid:9041) was sent SIGKILL! Perhaps out of memory?
```

**Why it happened:**
- 4 Gunicorn workers × 2 threads = 8 concurrent requests per replica
- Each request processes 20 test cases sequentially
- Each test case can use significant memory (especially Java/C++ compilation)
- With 500 concurrent requests, memory was exhausted quickly

**Impact:**
- Workers killed mid-execution
- Requests failed with HTTP 503 (Service Unavailable)
- Many requests timed out (180 seconds)

### 2. **Rate Limiting Too Aggressive** ⚠️
**Problem**: `/runall` endpoint had rate limit of "50 per minute"
- 500 users sending requests simultaneously
- Rate limiter rejected many requests
- Caused HTTP 503 errors

### 3. **Too Many Concurrent Requests** ⚠️
**Problem**: 500 concurrent requests overwhelmed the system
- 3 replicas × 8 concurrent = 24 total concurrent capacity
- 500 requests arrived simultaneously
- Queue built up, causing timeouts

### 4. **Long Test Cases** ⚠️
**Problem**: 20 test cases per user (including 3 long ones with 100-500 elements)
- Each test case takes time to execute
- Sequential execution means 20 × execution_time per user
- With compilation overhead (C++/Java/C#), this adds up quickly

## ✅ Fixes Applied

### 1. Reduced Gunicorn Workers (Prevent OOM)
**Before:**
```dockerfile
CMD ["gunicorn", ..., "--workers", "4", "--threads", "2", ...]
# 4 workers × 2 threads = 8 concurrent/replica
```

**After:**
```dockerfile
CMD ["gunicorn", ..., "--workers", "2", "--threads", "2", ...]
# 2 workers × 2 threads = 4 concurrent/replica
```

**Benefits:**
- Less memory per replica (2 workers instead of 4)
- With 3 replicas = 12 concurrent capacity (still good)
- Prevents OOM errors
- Workers auto-recycle after 100 requests (--max-requests)

### 2. Increased Rate Limits
**Before:**
```python
@limiter.limit("50 per minute")
```

**After:**
```python
@limiter.limit("1000 per minute")
```

**Benefits:**
- Allows 500+ users to submit without rate limiting issues
- Still provides protection against abuse

### 3. Increased Timeout
**Before:**
```dockerfile
"--timeout", "60"
```

**After:**
```dockerfile
"--timeout", "120"
```

**Benefits:**
- Allows more time for 20 test cases to complete
- Prevents premature timeouts

### 4. Added Worker Recycling
**Added:**
```dockerfile
"--max-requests", "100", "--max-requests-jitter", "10"
```

**Benefits:**
- Workers automatically restart after 100 requests
- Prevents memory leaks from accumulating
- Jitter prevents all workers restarting at once

## 📊 Expected Improvements

### Before (v31):
- **Success Rate**: 29.6% (148/500)
- **OOM Errors**: Many workers killed
- **Rate Limit**: 50/min (too low)
- **Concurrent/Replica**: 8 (too high, causes OOM)

### After (v32):
- **Expected Success Rate**: 80-90%+
- **OOM Errors**: Should be eliminated
- **Rate Limit**: 1000/min (sufficient)
- **Concurrent/Replica**: 4 (better memory management)

## 🎯 Recommendations for 500 Users

### Option 1: Stagger Requests (Recommended)
Instead of 500 concurrent requests:
- Send 50 requests at a time
- Wait for completion
- Send next batch
- **Expected**: 100% success rate, ~2-3 minutes total

### Option 2: Increase Replicas
- Start with 10-15 replicas (instead of 3)
- Each replica: 4 concurrent capacity
- Total: 40-60 concurrent capacity
- **Expected**: Better handling of 500 concurrent requests

### Option 3: Reduce Test Cases for Load Testing
- Use 5-10 test cases instead of 20
- Faster execution per user
- **Expected**: Better throughput

## 📝 Configuration Summary

**Current (v32):**
- Min Replicas: 3
- Max Replicas: 10
- Workers per Replica: 2
- Threads per Worker: 2
- Concurrent per Replica: 4
- Total Concurrent (3 replicas): 12
- Rate Limit: 1000/min
- Timeout: 120s
- Max Requests per Worker: 100

**For 500 Users:**
- Recommended: Stagger requests (50 at a time)
- Or: Increase min replicas to 10-15
- Or: Reduce test cases to 5-10 for load testing

## 🚀 Next Steps

1. ✅ Deploy v32 with fixes
2. ✅ Test with smaller batch (50 users)
3. ✅ If successful, test with 100 users
4. ✅ Gradually increase to 500 users with staggering
5. ✅ Monitor memory usage and OOM errors

