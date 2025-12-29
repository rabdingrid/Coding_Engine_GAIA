# 🚀 Optimize C++ Compilation - Reduce 24s to ~10s

## Problem Analysis

**Current Performance:**
- 17 test cases × 1.4s compilation = **23.6s**
- Each test case compiles C++ code separately
- Compilation overhead: ~1.0-1.2s per test
- Execution time: ~0.1-0.3s per test

**Target Performance:**
- Compile once: ~1.2s
- Execute 17 times: ~0.2s × 17 = ~3.4s
- **Total: ~4.6s** (80% improvement!)

---

## Solution: Compile Once, Run Multiple Times

### Strategy 1: Compile Before Loop (Recommended)

Modify `/runall` endpoint to compile once before executing all test cases.

**Current Code Flow:**
```
for each test_case:
    execute_code() → compile C++ → run → cleanup
```

**Optimized Code Flow:**
```
compile C++ once → for each test_case: run binary → cleanup
```

### Strategy 2: Code Caching

Cache compiled binaries based on code hash (more complex, but better for repeated submissions).

---

## Implementation Plan

### Option A: Quick Fix (Modify `/runall` endpoint)

Add compilation optimization for compiled languages (C++, Java, C#) in the `/runall` endpoint.

**Changes Needed:**
1. Detect compiled languages
2. Compile once before the loop
3. Reuse binary for all test cases
4. Handle compilation errors early

### Option B: New Function (Better Architecture)

Create `execute_code_batch()` function that:
- Compiles once
- Runs multiple test cases
- Returns results for all tests

---

## Expected Performance Improvement

| Metric | Current | Optimized | Improvement |
|--------|---------|-----------|------------|
| **Compilation Time** | 17 × 1.2s = 20.4s | 1 × 1.2s = 1.2s | **-94%** |
| **Execution Time** | 17 × 0.2s = 3.4s | 17 × 0.2s = 3.4s | Same |
| **Total Time** | **23.8s** | **~4.6s** | **-81%** |

**Result: 24s → ~5s** ✅

---

## Code Changes Required

### 1. Add Batch Execution Function

```python
def execute_cpp_batch(code: str, test_inputs: List[str], timeout: int = EXECUTION_TIMEOUT):
    """
    Execute C++ code with multiple test cases - compile once, run multiple times
    """
    temp_dir = create_sandboxed_directory()
    start_time = time.time()
    
    try:
        # Write code to file
        cpp_file = os.path.join(temp_dir, 'main.cpp')
        with open(cpp_file, 'w') as f:
            f.write(code)
        
        # COMPILE ONCE
        compile_start = time.time()
        compile_result = subprocess.run(
            ['g++', '-O2', '-std=c++17', '-o', os.path.join(temp_dir, 'main'), cpp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir,
            env={'PATH': '/usr/local/bin:/usr/bin:/bin'}
        )
        compile_time = (time.time() - compile_start) * 1000
        
        if compile_result.returncode != 0:
            return [{
                'stdout': '',
                'stderr': compile_result.stderr,
                'code': compile_result.returncode,
                'execution_time_ms': int(compile_time),
                'cpu_usage_percent': 0.0,
                'memory_usage_bytes': 0
            }] * len(test_inputs)
        
        # RUN MULTIPLE TIMES
        results = []
        binary_path = os.path.join(temp_dir, 'main')
        
        for test_input in test_inputs:
            exec_start = time.time()
            process = subprocess.Popen(
                [binary_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=set_resource_limits,
                cwd=temp_dir,
                env={'PATH': '/usr/local/bin:/usr/bin:/bin'}
            )
            
            stdout, stderr = process.communicate(input=test_input, timeout=timeout)
            exec_time = (time.time() - exec_start) * 1000
            
            results.append({
                'stdout': stdout,
                'stderr': stderr,
                'code': process.returncode,
                'execution_time_ms': int(exec_time),
                'cpu_usage_percent': 0.0,
                'memory_usage_bytes': 0
            })
        
        return results
        
    except Exception as e:
        return [{
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1,
            'execution_time_ms': int((time.time() - start_time) * 1000),
            'cpu_usage_percent': 0.0,
            'memory_usage_bytes': 0
        }] * len(test_inputs)
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
```

### 2. Modify `/runall` Endpoint

```python
@app.post('/runall', response_model=ExecutionResponse)
async def runall(request: Request, runall_req: RunAllRequest):
    # ... existing validation code ...
    
    language = runall_req.language.lower()
    code = runall_req.code
    test_cases = runall_req.test_cases
    
    # OPTIMIZATION: For compiled languages, compile once
    if language in ['cpp', 'java', 'csharp'] and len(test_cases) > 1:
        # Extract all test inputs
        test_inputs = [tc.input for tc in test_cases]
        
        # Execute batch (compile once)
        if language == 'cpp':
            execution_results = execute_cpp_batch(code, test_inputs, timeout)
        elif language == 'java':
            execution_results = execute_java_batch(code, test_inputs, timeout)
        elif language == 'csharp':
            execution_results = execute_csharp_batch(code, test_inputs, timeout)
        
        # Process results
        for idx, (test_case, execution_result) in enumerate(zip(test_cases, execution_results)):
            # ... process each result ...
    else:
        # Original sequential execution for interpreted languages
        for test_case in test_cases:
            execution_result = execute_code(language, code, test_case.input, timeout)
            # ... process result ...
```

---

## Additional Optimizations

### 1. Faster Compilation Flags

```bash
# Current
g++ -o main main.cpp

# Optimized (faster compilation, still fast execution)
g++ -O2 -std=c++17 -pipe -o main main.cpp
```

**Benefits:**
- `-O2`: Good optimization, faster than `-O3` compilation
- `-pipe`: Use pipes instead of temp files (faster)
- `-std=c++17`: Modern standard, better optimizations

### 2. Pre-compiled Headers (Advanced)

For frequently used headers like `<bits/stdc++.h>`, pre-compile them.

### 3. Parallel Compilation (Future)

Use `-j` flag for multi-file projects (not applicable here, but good to know).

---

## Testing Plan

1. **Test with 17 test cases:**
   - Current: ~24s
   - Expected: ~5s
   - Target: <10s ✅

2. **Test edge cases:**
   - Compilation errors (should fail fast)
   - Single test case (should still work)
   - Large code (should still compile)

3. **Verify correctness:**
   - All test results should match current implementation
   - No regressions

---

## Implementation Steps

1. ✅ Create `execute_cpp_batch()` function
2. ✅ Modify `/runall` endpoint to use batch execution
3. ✅ Add similar functions for Java and C#
4. ✅ Test with existing test cases
5. ✅ Measure performance improvement
6. ✅ Deploy and monitor

---

## Expected Results

**Before:**
```
17 test cases × 1.4s = 23.8s
```

**After:**
```
1 compilation × 1.2s = 1.2s
17 executions × 0.2s = 3.4s
Total: ~4.6s
```

**Improvement: 81% faster!** 🚀

---

## Notes

- This optimization only applies to `/runall` endpoint (multiple test cases)
- `/run` endpoint (single test case) remains unchanged
- No changes needed for interpreted languages (Python, JavaScript)
- Backward compatible - same API, faster performance


