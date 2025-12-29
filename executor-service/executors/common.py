"""Common utilities for executors"""
import time
import threading
import psutil
from typing import Dict, Callable

def monitor_process_execution(process, timeout: float) -> Dict[str, float]:
    """
    Monitor process CPU and memory usage
    
    Returns:
        Dict with 'cpu_usage_percent' and 'memory_usage_bytes'
    """
    monitoring_active = True
    max_cpu = 0.0
    max_memory = 0
    psutil_process_obj = None
    
    def monitor_process():
        nonlocal max_cpu, max_memory, psutil_process_obj
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
                    time.sleep(0.01)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    monitor_thread = threading.Thread(target=monitor_process, daemon=True)
    monitor_thread.start()
    time.sleep(0.01)
    
    # Return function to stop monitoring and get final stats
    def stop_and_get_stats():
        nonlocal monitoring_active, max_cpu, max_memory, psutil_process_obj
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
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return {'cpu_usage_percent': max_cpu, 'memory_usage_bytes': max_memory}
    
    return stop_and_get_stats

