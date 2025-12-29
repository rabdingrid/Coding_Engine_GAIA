"""Python code executor"""
import subprocess
import time
import threading
import psutil
from typing import Dict
from executor_service.config import EXECUTION_TIMEOUT
from executor_service.security.limits import set_resource_limits

def execute(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT) -> Dict:
    """Execute Python code with security guardrails"""
    start_time = time.time()
    process = None
    cpu_usage = 0.0
    memory_usage = 0
    
    try:
        process = subprocess.Popen(
            ['python3', '-c', code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'PYTHONUNBUFFERED': '1',
                'PYTHONDONTWRITEBYTECODE': '1',
                'PYTHONNOUSERSITE': '1',
            },
            cwd='/tmp',
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
        
        return {
            'stdout': stdout,
            'stderr': stderr,
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

