# Load Test Results: 20 Dummy Users with Different DSA Questions

## 📊 Test Summary

**Date**: December 4, 2025  
**Time**: 22:36:11 - 22:36:17  
**Duration**: 5.91 seconds  
**Total Users**: 20  
**Questions**: 20 different simple DSA problems

## 📈 Overall Statistics

| Metric | Value |
|--------|-------|
| **Total Requests** | 20 |
| **✅ Successful** | 13 (65.0%) |
| **❌ Failed** | 7 (35.0%) |
| **Total Duration** | 5,911ms (5.91s) |
| **Average Wait Time** | 2,850ms |
| **Average Execution Time** | 2,103ms |
| **All Tests Passed** | 13/13 (100% of successful) |

## ⏱️ Performance Metrics

### Wait Times (Time until response received)
- **Min**: 711ms
- **Max**: 5,662ms
- **Avg**: 2,850ms

### Execution Times (Code execution duration)
- **Min**: 21ms
- **Max**: 4,931ms
- **Avg**: 2,103ms

## 📝 Language Distribution

| Language | Successful | Failed | Total | Success Rate |
|----------|-----------|--------|-------|--------------|
| **Python** | 7 | 3 | 10 | 70.0% |
| **C++** | 6 | 4 | 10 | 60.0% |

## 🔄 Request Distribution

- **Container**: All requests handled by "unknown" (metadata not available)
- **Replica**: All requests handled by "unknown" (metadata not available)

## ✅ Successful Requests (13)

| User | Question | Language | Start Time | End Time | Duration | Exec Time | Status |
|------|----------|----------|------------|----------|----------|-----------|--------|
| user_5 | Factorial | python | 22:36:11.957 | 22:36:12.668 | 711ms | 21ms | ✅ Pass |
| user_19 | Sum of Squares | python | 22:36:11.957 | 22:36:12.695 | 738ms | 25ms | ✅ Pass |
| user_15 | Square Root | python | 22:36:11.957 | 22:36:12.707 | 750ms | 33ms | ✅ Pass |
| user_11 | Check Palindrome | python | 22:36:11.957 | 22:36:12.786 | 829ms | 98ms | ✅ Pass |
| user_7 | Fibonacci | python | 22:36:11.957 | 22:36:12.866 | 909ms | 92ms | ✅ Pass |
| user_13 | GCD | python | 22:36:11.957 | 22:36:12.930 | 973ms | 113ms | ✅ Pass |
| user_17 | String Length | python | 22:36:11.957 | 22:36:12.942 | 985ms | 125ms | ✅ Pass |
| user_2 | Find Maximum | cpp | 22:36:11.957 | 22:36:16.587 | 4,630ms | 3,932ms | ✅ Pass |
| user_12 | Power of Two | cpp | 22:36:11.957 | 22:36:16.895 | 4,938ms | 4,214ms | ✅ Pass |
| user_16 | Count Primes | cpp | 22:36:11.957 | 22:36:17.172 | 5,216ms | 4,495ms | ✅ Pass |
| user_14 | Count Vowels | cpp | 22:36:11.957 | 22:36:17.293 | 5,336ms | 4,595ms | ✅ Pass |
| user_20 | Check Even | cpp | 22:36:11.957 | 22:36:17.339 | 5,379ms | 4,671ms | ✅ Pass |
| user_4 | Reverse Array | cpp | 22:36:11.957 | 22:36:17.619 | 5,662ms | 4,931ms | ✅ Pass |

## ❌ Failed Requests (7)

| User | Question | Language | Start Time | End Time | Duration | Error |
|------|----------|----------|------------|----------|----------|-------|
| user_9 | Count Odd Numbers | python | 22:36:11.957 | 22:36:12.668 | 711ms | HTTP 400 |
| user_3 | Count Even Numbers | python | 22:36:11.957 | 22:36:12.784 | 827ms | HTTP 400 |
| user_10 | Sum of Digits | cpp | 22:36:11.957 | 22:36:17.681 | 5,724ms | HTTP 400 |
| user_18 | Binary to Decimal | cpp | 22:36:11.957 | 22:36:17.680 | 5,723ms | HTTP 400 |
| user_8 | Find Minimum | cpp | 22:36:11.957 | 22:36:17.684 | 5,727ms | HTTP 400 |
| user_6 | Check Prime | cpp | 22:36:11.957 | 22:36:17.853 | 5,896ms | HTTP 400 |
| user_1 | Sum of Array | cpp | 22:36:11.957 | 22:36:17.867 | 5,910ms | HTTP 400 |

## 📊 Analysis

### Performance Patterns

1. **Python Requests**: 
   - Fast execution (21-125ms)
   - Quick response times (711-985ms)
   - Higher success rate (70%)

2. **C++ Requests**:
   - Slower execution (3,932-4,931ms)
   - Longer response times (4,630-5,662ms)
   - Lower success rate (60%)
   - More failures under concurrent load

### Failure Pattern

- **Python failures**: 3 failures, all occurred early (711-827ms)
- **C++ failures**: 4 failures, all occurred late (5,723-5,910ms)
- **Pattern**: C++ requests that took longer were more likely to fail
- **Possible cause**: Timeout or resource contention under concurrent load

### Capacity Analysis

- **Concurrent capacity**: Successfully handled 13/20 requests (65%)
- **Python capacity**: 7/10 (70%)
- **C++ capacity**: 6/10 (60%)
- **Total time**: 5.91 seconds for 20 parallel requests
- **Throughput**: ~3.4 requests/second

## 🔍 Observations

1. **System handled 13 concurrent requests successfully**
2. **Python code executes much faster than C++**
3. **C++ requests are more prone to failures under high load**
4. **All successful requests passed their test cases (100%)**
5. **HTTP 400 errors suggest server-side validation or resource issues**

## 💡 Recommendations

1. **For production**: System can handle ~13-15 concurrent requests reliably
2. **For C++ heavy loads**: Consider increasing timeout or optimizing C++ compilation
3. **For 200-300 users**: Need ~20-25 replicas (20 × 13 = 260 concurrent capacity)
4. **Investigate HTTP 400 errors**: Check server logs for root cause

## 📅 Test Timestamp

**Start**: 2025-12-04 22:36:11.957  
**End**: 2025-12-04 22:36:17.869  
**Duration**: 5,911ms

