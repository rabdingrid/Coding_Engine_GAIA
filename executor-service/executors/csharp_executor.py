"""C# code executor"""
import subprocess
import os
import time
import threading
import psutil
import shutil
from typing import Dict
from executor_service.config import EXECUTION_TIMEOUT, MAX_MEMORY
from executor_service.security.limits import set_resource_limits
from executor_service.executors.base import create_sandboxed_directory

def execute(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT) -> Dict:
    """Execute C# code"""
    temp_dir = create_sandboxed_directory()
    start_time = time.time()
    cpu_usage = 0.0
    memory_usage = 0
    
    try:
        cs_file = os.path.join(temp_dir, 'Program.cs')
        with open(cs_file, 'w') as f:
            f.write(code)
        
        compile_cmd = None
        run_cmd = None
        
        dotnet_check = subprocess.run(['which', 'dotnet'], capture_output=True)
        if dotnet_check.returncode == 0:
            compile_cmd = ['dotnet', 'new', 'console', '-n', 'Solution', '--force']
            run_cmd = ['dotnet', 'run', '--project', os.path.join(temp_dir, 'Solution')]
            solution_dir = os.path.join(temp_dir, 'Solution')
            if os.path.exists(solution_dir):
                with open(os.path.join(solution_dir, 'Program.cs'), 'w') as f:
                    f.write(code)
        else:
            compile_cmd = ['mcs', '-out:' + os.path.join(temp_dir, 'program.exe'), cs_file]
            run_cmd = ['mono', os.path.join(temp_dir, 'program.exe')]
        
        if compile_cmd:
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir,
                env={'PATH': '/usr/local/bin:/usr/bin:/bin'}
            )
            
            if compile_result.returncode != 0:
                execution_time_ms = int((time.time() - start_time) * 1000)
                return {
                    'stdout': '',
                    'stderr': compile_result.stderr,
                    'code': compile_result.returncode,
                    'execution_time_ms': execution_time_ms,
                    'cpu_usage_percent': 0.0,
                    'memory_usage_bytes': 0
                }
        process = subprocess.Popen(
            run_cmd,
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
        psutil_process_obj = None
        
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
        
        stdout, stderr = process.communicate(input=stdin, timeout=timeout)
        monitoring_active = False
        
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
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Check for TLE/MLE
        error_msg = stderr
        if execution_time_ms >= timeout * 1000:
            error_msg = f"Time Limit Exceeded (TLE): Execution exceeded {timeout} seconds"
        elif memory_usage > MAX_MEMORY:
            error_msg = f"Memory Limit Exceeded (MLE): Used {memory_usage / (1024*1024):.2f}MB (limit: {MAX_MEMORY / (1024*1024):.2f}MB)"
        
        return {
            'stdout': stdout,
            'stderr': error_msg if error_msg else stderr,
            'code': process.returncode,
            'execution_time_ms': execution_time_ms,
            'cpu_usage_percent': cpu_usage,
            'memory_usage_bytes': memory_usage
        }
    except subprocess.TimeoutExpired:
        execution_time_ms = int((time.time() - start_time) * 1000)
        return {
            'stdout': '',
            'stderr': f'Time Limit Exceeded (TLE): Execution exceeded {timeout} seconds',
            'code': 124,
            'execution_time_ms': execution_time_ms,
            'cpu_usage_percent': cpu_usage,
            'memory_usage_bytes': memory_usage
        }
    except Exception as e:
        execution_time_ms = int((time.time() - start_time) * 1000)
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1,
            'execution_time_ms': execution_time_ms,
            'cpu_usage_percent': cpu_usage,
            'memory_usage_bytes': memory_usage
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

