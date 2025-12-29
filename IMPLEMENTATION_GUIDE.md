# 🚀 Implementation Guide: Reduce C++ Execution from 24s to ~5s

## Problem

**Current:** 17 test cases × 1.4s = **24 seconds**  
**Target:** Compile once + run 17 times = **~5 seconds**  
**Improvement:** **80% faster!**

## Root Cause

The `/runall` endpoint calls `execute_code()` for each test case, which compiles C++ code 17 times. Each compilation takes ~1.2s.

## Solution

**Compile once, run multiple times** - Add batch execution for compiled languages.

---

## Step-by-Step Implementation

### Step 1: Add Batch Execution Function

Add this function to `executor-service-fastapi.py` (after `execute_cpp` function, around line 850):

```python
def execute_cpp_batch(code: str, test_inputs: list, timeout: int = EXECUTION_TIMEOUT):
    """
    Execute C++ code with multiple test cases - COMPILE ONCE, RUN MULTIPLE TIMES
    Optimized version that reduces execution time by ~80% for multiple test cases.
    """
    temp_dir = create_sandboxed_directory()
    start_time = time.time()
    results = []
    
    try:
        # Write code to file
        cpp_file = os.path.join(temp_dir, 'main.cpp')
        with open(cpp_file, 'w') as f:
            f.write(code)
        
        # COMPILE ONCE (takes ~1.2s)
        compile_start = time.time()
        binary_path = os.path.join(temp_dir, 'main')
        
        compile_result = subprocess.run(
            ['g++', '-O2', '-std=c++17', '-pipe', '-o', binary_path, cpp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir,
            env={'PATH': '/usr/local/bin:/usr/bin:/bin'}
        )
        compile_time_ms = int((time.time() - compile_start) * 1000)
        
        # If compilation fails, return error for all test cases
        if compile_result.returncode != 0:
            error_result = {
                'stdout': '',
                'stderr': compile_result.stderr,
                'code': compile_result.returncode,
                'execution_time_ms': compile_time_ms,
                'cpu_usage_percent': 0.0,
                'memory_usage_bytes': 0
            }
            return [error_result] * len(test_inputs)
        
        # RUN MULTIPLE TIMES (fast, ~0.2s each)
        for test_input in test_inputs:
            exec_start = time.time()
            cpu_usage = 0.0
            memory_usage = 0
            psutil_process_obj = None
            
            try:
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
                
                # Monitor CPU and memory (same as execute_cpp)
                monitoring_active = True
                max_cpu = 0.0
                max_memory = 0
                
                def monitor_process():
                    nonlocal cpu_usage, memory_usage, max_cpu, max_memory, psutil_process_obj
                    try:
                        psutil_process_obj = psutil.Process(process.pid)
                        psutil_process_obj.cpu_percent()
                        
                        while monitoring_active:
                            try:
                                if not psutil_process_obj.is_running():
                                    break
                                current_cpu = psutil_process_obj.cpu_percent()
                                if current_cpu > max_cpu:
                                    max_cpu = current_cpu
                                memory_info = psutil_process_obj.memory_info()
                                current_memory = memory_info.rss
                                if current_memory > max_memory:
                                    max_memory = current_memory
                                cpu_usage = max_cpu
                                memory_usage = max_memory
                                time.sleep(0.01)
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                monitor_thread = threading.Thread(target=monitor_process, daemon=True)
                monitor_thread.start()
                time.sleep(0.01)
                
                stdout, stderr = process.communicate(input=test_input, timeout=timeout)
                monitoring_active = False
                
                # Final CPU/memory reading
                try:
                    if psutil_process_obj is None:
                        psutil_process_obj = psutil.Process(process.pid)
                    final_cpu = psutil_process_obj.cpu_percent()
                    if final_cpu > max_cpu:
                        max_cpu = final_cpu
                    memory_info = psutil_process_obj.memory_info()
                    final_memory = memory_info.rss
                    if final_memory > max_memory:
                        max_memory = final_memory
                    cpu_usage = max_cpu
                    memory_usage = max_memory
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                
                exec_time_ms = int((time.time() - exec_start) * 1000)
                
                results.append({
                    'stdout': stdout,
                    'stderr': stderr,
                    'code': process.returncode,
                    'execution_time_ms': exec_time_ms,
                    'cpu_usage_percent': cpu_usage,
                    'memory_usage_bytes': memory_usage
                })
                
            except subprocess.TimeoutExpired:
                exec_time_ms = int((time.time() - exec_start) * 1000)
                results.append({
                    'stdout': '',
                    'stderr': f'Time Limit Exceeded (TLE): Execution exceeded {timeout} seconds',
                    'code': 124,
                    'execution_time_ms': exec_time_ms,
                    'cpu_usage_percent': cpu_usage,
                    'memory_usage_bytes': memory_usage
                })
            except Exception as e:
                exec_time_ms = int((time.time() - exec_start) * 1000)
                results.append({
                    'stdout': '',
                    'stderr': f'Execution error: {str(e)}',
                    'code': 1,
                    'execution_time_ms': exec_time_ms,
                    'cpu_usage_percent': 0.0,
                    'memory_usage_bytes': 0
                })
        
        return results
        
    except Exception as e:
        error_result = {
            'stdout': '',
            'stderr': f'Batch execution error: {str(e)}',
            'code': 1,
            'execution_time_ms': int((time.time() - start_time) * 1000),
            'cpu_usage_percent': 0.0,
            'memory_usage_bytes': 0
        }
        return [error_result] * len(test_inputs)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
```

### Step 2: Modify `/runall` Endpoint

Modify the `/runall` endpoint (around line 1257) to use batch execution for C++:

**Find this code:**
```python
for idx, test_case in enumerate(test_cases):
    test_input = test_case.input
    expected_output = test_case.expected_output
    test_case_id = test_case.id or f'test_{idx + 1}'
    
    # Execute code
    test_start_time = time.time()
    try:
        execution_result = execute_code(language, code, test_input, timeout)
    except Exception as e:
        # ... error handling ...
```

**Replace with:**
```python
# OPTIMIZATION: For compiled languages with multiple test cases, use batch execution
if language in ['cpp', 'c++'] and len(test_cases) > 1:
    # Extract all test inputs
    test_inputs = [tc.input for tc in test_cases]
    
    # Execute batch (compile once, run multiple times)
    try:
        execution_results = execute_cpp_batch(code, test_inputs, timeout)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error in execute_cpp_batch: {e}\n{error_trace}")
        restore_network_access(original_socket)
        raise HTTPException(status_code=400, detail=f"Batch execution failed: {str(e)}")
    
    # Process results
    for idx, (test_case, execution_result) in enumerate(zip(test_cases, execution_results)):
        test_input = test_case.input
        expected_output = test_case.expected_output
        test_case_id = test_case.id or f'test_{idx + 1}'
        
        # Process result (same as before)
        error_type = detect_error_type(execution_result, timeout)
        actual_output = execution_result.get('stdout', '')
        stderr = execution_result.get('stderr', '')
        
        # Determine status and passed
        if error_type in ['tle', 'mle', 'syntax_error', 'runtime_error', 'error']:
            status = error_type
            passed = False
        else:
            passed = compare_outputs(actual_output, expected_output)
            status = 'passed' if passed else 'failed'
        
        if passed:
            total_passed += 1
        else:
            total_failed += 1
        
        test_results.append({
            'test_case_id': test_case_id,
            'test_case_number': idx + 1,
            'input': test_input,
            'expected_output': expected_output,
            'actual_output': actual_output,
            'error': stderr if stderr else None,
            'status': status,
            'passed': passed,
            'execution_time_ms': execution_result.get('execution_time_ms', 0),
            'cpu_usage_percent': execution_result.get('cpu_usage_percent', 0.0),
            'memory_usage_bytes': execution_result.get('memory_usage_bytes', 0)
        })
else:
    # Original sequential execution for interpreted languages or single test case
    for idx, test_case in enumerate(test_cases):
        test_input = test_case.input
        expected_output = test_case.expected_output
        test_case_id = test_case.id or f'test_{idx + 1}'
        
        # Execute code
        test_start_time = time.time()
        try:
            execution_result = execute_code(language, code, test_input, timeout)
        except Exception as e:
            # ... existing error handling ...
```

---

## Expected Performance

| Scenario | Before | After | Improvement |
|----------|--------|-------|-------------|
| **17 C++ test cases** | 24s | ~5s | **80% faster** |
| **5 C++ test cases** | 7s | ~2s | **71% faster** |
| **1 C++ test case** | 1.4s | 1.4s | No change |
| **Python/JS** | Same | Same | No change |

---

## Testing

After implementation, test with:

```bash
# Test with 17 test cases (should take ~5s instead of 24s)
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall" \
  -H "Content-Type: application/json" \
  -d @your_test_payload.json \
  -w "\n⏱️ Total Time: %{time_total}s\n"
```

---

## Notes

- ✅ Backward compatible - same API
- ✅ Only optimizes `/runall` endpoint
- ✅ Only applies to C++ with multiple test cases
- ✅ Single test cases use original path (no regression)
- ✅ Python/JavaScript unchanged (already fast)

---

## Future Enhancements

1. **Add Java batch execution** (similar optimization)
2. **Add C# batch execution** (similar optimization)
3. **Code caching** (cache compiled binaries by code hash)
4. **Parallel test execution** (run multiple tests in parallel after compilation)


