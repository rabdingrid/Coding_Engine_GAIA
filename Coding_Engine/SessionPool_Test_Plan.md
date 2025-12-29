# Session Pool Code Execution Test Plan

## 🎯 Objective
Verify that the session pool can properly execute code through the complete flow:
**Backend API → Azure Session Pool → Code Execution → Response**

## 📋 Test Scenarios

### 1. Basic Code Execution Tests
- **Test 1.1**: Simple print statement
  - Code: `print("Hello, World!")`
  - Expected: stdout contains "Hello, World!"
  - Exit code: 0

- **Test 1.2**: Arithmetic operations
  - Code: `print(2 + 2)`
  - Expected: stdout contains "4"
  - Exit code: 0

- **Test 1.3**: Variable assignment and output
  - Code: `x = 10; print(x * 2)`
  - Expected: stdout contains "20"
  - Exit code: 0

### 2. Input/Output Tests
- **Test 2.1**: Reading from stdin
  - Code: `name = input(); print(f"Hello, {name}")`
  - Input: "Alice"
  - Expected: stdout contains "Hello, Alice"
  - Exit code: 0

- **Test 2.2**: Multiple input lines
  - Code: `a = int(input()); b = int(input()); print(a + b)`
  - Input: "5\n3"
  - Expected: stdout contains "8"
  - Exit code: 0

- **Test 2.3**: Test case format (from test_cases/)
  - Code: Reads number N, prints "Hello" N times
  - Input: "5"
  - Expected: 5 lines of "Hello"
  - Exit code: 0

### 3. Error Handling Tests
- **Test 3.1**: Syntax error
  - Code: `print("unclosed string`
  - Expected: stderr contains syntax error
  - Exit code: non-zero

- **Test 3.2**: Runtime error
  - Code: `x = 1 / 0`
  - Expected: stderr contains ZeroDivisionError
  - Exit code: non-zero

- **Test 3.3**: Import error
  - Code: `import nonexistent_module`
  - Expected: stderr contains ModuleNotFoundError
  - Exit code: non-zero

### 4. Concurrency Tests
- **Test 4.1**: Sequential requests (5 requests)
  - Purpose: Verify session pool handles sequential requests
  - Expected: All succeed, reasonable latency

- **Test 4.2**: Concurrent requests (10 simultaneous)
  - Purpose: Verify session pool handles concurrent executions
  - Expected: All succeed, no race conditions

- **Test 4.3**: Session reuse
  - Purpose: Verify sessions are reused within cooldown period
  - Expected: Second request faster (if within cooldown)

### 5. Integration Tests
- **Test 5.1**: Full flow through backend API
  - Use backend's `/api/v2/execute` endpoint
  - Verify response format matches expected structure
  - Check all fields present (stdout, stderr, code, language, version)

- **Test 5.2**: Test case validation
  - Run all test cases from `test_cases/` directory
  - Compare outputs with expected outputs
  - Verify 100% match

## 🔧 Test Implementation Strategy

### Phase 1: Local Testing (Fallback Mode)
1. Test with `USE_LOCAL_EXECUTOR=true`
2. Verify test infrastructure works
3. Validate test cases pass locally

### Phase 2: Session Pool Testing (When Deployed)
1. Deploy session pool (cost-optimized: `ready-sessions: 0`)
2. Test with actual Azure session pool
3. Verify authentication works
4. Test all scenarios above

### Phase 3: Performance Testing
1. Measure cold start time (first request)
2. Measure warm execution time (subsequent requests)
3. Measure concurrent execution throughput
4. Document performance metrics

## 📊 Success Criteria

### Functional Requirements
- ✅ All basic execution tests pass
- ✅ All input/output tests pass
- ✅ Error handling works correctly
- ✅ Concurrent executions work without issues
- ✅ Test cases match expected outputs

### Performance Requirements
- ✅ Cold start: < 5 seconds (acceptable)
- ✅ Warm execution: < 1 second
- ✅ Concurrent requests: All handled correctly
- ✅ No memory leaks or resource exhaustion

### Reliability Requirements
- ✅ No crashes or unhandled exceptions
- ✅ Proper error messages for failures
- ✅ Graceful degradation (fallback to local if needed)

## 🚀 Test Execution

### Prerequisites
1. Backend service running (local or deployed)
2. Session pool deployed (for Phase 2)
3. Test script dependencies installed

### Running Tests
```bash
# Phase 1: Local testing
USE_LOCAL_EXECUTOR=true python test_session_pool.py

# Phase 2: Session pool testing (when deployed)
python test_session_pool.py --endpoint <BACKEND_URL>

# Phase 3: Full test suite
python test_session_pool.py --full
```

## 📝 Test Results Documentation

After running tests, document:
1. Test execution summary (passed/failed)
2. Performance metrics
3. Any issues or edge cases discovered
4. Recommendations for improvements

---

**Created**: December 2024  
**Status**: Ready for Implementation


