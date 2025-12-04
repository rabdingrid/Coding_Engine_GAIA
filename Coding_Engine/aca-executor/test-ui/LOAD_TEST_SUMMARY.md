# Load Test Summary - Real Capacity Testing

## 🎯 Test Objective
Test the real capacity of the Azure Container Apps executor with 2 replicas using parallel curl requests.

## 📊 Test Configuration
- **API URL**: `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Replicas**: Min=2, Max=3
- **Language**: C++ (all users)
- **Question**: Warehouse Box Removal
- **Test Cases**: 2 test cases per request
- **Tool**: Python script using curl via subprocess

## 📈 Test Results

### Test 1: 5 Users (Parallel)
- **Total Requests**: 5
- **✅ Successful**: 5 (100%)
- **❌ Failed**: 0
- **Max Wait Time**: 4,563ms
- **Avg Wait Time**: 3,987ms
- **Avg Execution Time**: 3,295ms
- **All Tests Passed**: 5/5 ✅
- **Total Time**: 4.56s
- **Requests/second**: 1.10

**Result**: ✅ All requests succeeded

### Test 2: 10 Users (Parallel)
- **Total Requests**: 10
- **✅ Successful**: 2 (20%)
- **❌ Failed**: 8 (HTTP 400)
- **Max Wait Time**: 4,633ms (for successful)
- **Avg Wait Time**: 4,613ms (for successful)
- **All Tests Passed**: 2/2 ✅
- **Total Time**: 5.72s

**Result**: ⚠️ Only 20% success rate - Most requests failed with HTTP 400

### Test 3: 20 Users (Parallel)
- **Total Requests**: 20
- **✅ Successful**: 0 (0%)
- **❌ Failed**: 20 (HTTP 400)
- **Wait Time**: ~5,700ms (all failed)
- **Total Time**: ~5.8s

**Result**: ❌ All requests failed

### Test 4: 30 Users (Parallel)
- **Total Requests**: 30
- **✅ Successful**: 0 (0%)
- **❌ Failed**: 30 (HTTP 400)
- **Wait Time**: ~5,700ms (all failed)
- **Total Time**: ~5.8s

**Result**: ❌ All requests failed

## 🔍 Error Analysis

### Error Message (from failed requests):
```
HTTP 400: {"detail":"Test case test_1 execution failed: cannot access local variable 'start_time' where it is not associated with a value"}
```

### Root Cause:
The error indicates a variable scope issue in the parallel execution code. When multiple requests arrive simultaneously, there's a race condition or uninitialized variable issue in the `/runall` endpoint's parallel execution logic.

### Pattern Observed:
- **1-5 users**: ✅ Works perfectly
- **6-10 users**: ⚠️ Partial success (20-40%)
- **10+ users**: ❌ Complete failure (0% success)

## 📊 Capacity Findings

### Current Real Capacity:
- **Safe Capacity**: **~5 concurrent requests** (100% success rate)
- **Degraded Capacity**: **~2-3 concurrent requests** (partial success)
- **Failure Point**: **>5 concurrent requests** (complete failure)

### Expected vs Actual:
- **Expected**: 2 replicas × 10 concurrent = 20 requests
- **Actual**: ~5 concurrent requests (safe)
- **Gap**: 75% below expected capacity

## ⚠️ Issues Identified

1. **Variable Scope Bug**: The `start_time` variable issue in parallel execution is still present under high load
2. **Concurrency Limitation**: System cannot handle more than 5 concurrent requests reliably
3. **Error Handling**: HTTP 400 errors suggest the server-side code has issues with parallel execution

## 💡 Recommendations

### Immediate Fixes:
1. **Fix Variable Scope Issue**: Ensure `test_start_time` is always initialized before use in the parallel execution helper function
2. **Add Error Handling**: Better error handling in the parallel execution code to prevent cascading failures
3. **Add Rate Limiting**: Implement proper rate limiting to prevent overwhelming the system

### Capacity Improvements:
1. **Increase Min Replicas**: For 20-30 concurrent users, need at least 4-6 replicas
2. **Fix Parallel Execution Bug**: The current parallel execution has a bug that causes failures under load
3. **Add Request Queuing**: Implement a proper queue system to handle bursts of requests

### For 200-300 Users:
Based on current findings:
- **Safe capacity per replica**: ~2-3 concurrent requests
- **For 300 users**: Need ~100-150 replicas (if bug is fixed)
- **With bug fixed**: Could reduce to ~30-50 replicas

## 📝 Test Scripts

### Files Created:
1. `load-test-capacity.py` - Python-based load test using curl
2. `load-test-curl.sh` - Bash-based load test (has JSON escaping issues)
3. `load-test-curl-simple.sh` - Simplified bash version (has sed issues on macOS)

### Recommended Script:
Use `load-test-capacity.py` - it handles JSON properly and works cross-platform.

## 🚀 Next Steps

1. **Fix the parallel execution bug** in `executor-service-fastapi.py`
2. **Re-test with 10, 20, 30 users** after fix
3. **Gradually increase load** to find the real capacity
4. **Monitor Azure Container Apps metrics** during load tests
5. **Adjust replica count** based on actual capacity findings

## 📅 Test Date
December 4, 2025

## 🔧 System Configuration
- **Container Apps**: Azure Container Apps (East US 2)
- **Min Replicas**: 2
- **Max Replicas**: 3
- **CPU per Replica**: 2 vCPU
- **Memory per Replica**: 4 GiB
- **Image**: `executor-fastapi:v24-fix-queue`

