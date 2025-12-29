"""
Optimized C++ batch execution - Compile once, run multiple times
This reduces execution time from 24s to ~5s for 17 test cases
"""

import subprocess
import tempfile
import shutil
import os
import time
import psutil
import threading
import hashlib

def set_resource_limits():
    """Set resource limits for subprocess"""
    import resource
    # Set memory limit (64MB)
    resource.setrlimit(resource.RLIMIT_AS, (64 * 1024 * 1024, 64 * 1024 * 1024))
    # Set CPU time limit
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))

def execute_cpp_batch(code: str, test_inputs: list, timeout: int = 5):
    """
    Execute C++ code with multiple test cases - COMPILE ONCE, RUN MULTIPLE TIMES
    
    This is the optimized version that reduces 24s to ~5s for 17 test cases.
    
    Args:
        code: C++ source code
        test_inputs: List of test input strings
        timeout: Timeout in seconds
    
    Returns:
        List of execution results, one per test input
    """
    temp_dir = tempfile.mkdtemp(prefix='cpp_batch_')
    start_time = time.time()
    results = []
    
    try:
        # Write code to file
        cpp_file = os.path.join(temp_dir, 'main.cpp')
        with open(cpp_file, 'w') as f:
            f.write(code)
        
        # ============================================
        # STEP 1: COMPILE ONCE (takes ~1.2s)
        # ============================================
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
        
        # ============================================
        # STEP 2: RUN MULTIPLE TIMES (fast, ~0.2s each)
        # ============================================
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
                
                # Monitor CPU and memory
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
                
                # Execute with input
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
        # Return error for all test cases
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
        # Cleanup
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass


# Example usage and performance comparison
if __name__ == "__main__":
    # Test code
    test_code = """#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}"""
    
    # Test inputs
    test_inputs = [
        "5\n3",
        "10\n20",
        "1\n1",
        "0\n0",
        "-5\n5"
    ]
    
    print("Testing optimized batch execution...")
    start = time.time()
    results = execute_cpp_batch(test_code, test_inputs, timeout=5)
    total_time = time.time() - start
    
    print(f"\n✅ Batch execution completed in {total_time:.2f}s")
    print(f"   Average per test: {total_time/len(test_inputs)*1000:.1f}ms")
    print(f"\nResults:")
    for i, result in enumerate(results):
        print(f"  Test {i+1}: {result['stdout'].strip()} (executed in {result['execution_time_ms']}ms)")


