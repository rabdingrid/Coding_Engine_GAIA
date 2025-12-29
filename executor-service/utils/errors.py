"""Error detection and classification"""
from typing import Dict
from executor_service.config import MAX_MEMORY

def detect_error_type(execution_result: Dict, timeout: int) -> str:
    """
    Detect error type: 'tle', 'mle', 'syntax_error', 'runtime_error', 'error'
    """
    stderr = execution_result.get('stderr', '')
    code = execution_result.get('code', 0)
    execution_time_ms = execution_result.get('execution_time_ms', 0)
    memory_usage_bytes = execution_result.get('memory_usage_bytes', 0)
    
    # Check for TLE
    if code == 124 or execution_time_ms >= timeout * 1000:
        return 'tle'
    
    # Check for MLE
    if memory_usage_bytes > MAX_MEMORY * 0.9:  # 90% of limit
        return 'mle'
    
    # Check for syntax/compilation errors
    syntax_keywords = [
        'syntax error', 'SyntaxError', 'compile error', 'CompilationError',
        'error:', 'Error:', 'Exception:', 'Traceback'
    ]
    if any(keyword.lower() in stderr.lower() for keyword in syntax_keywords):
        if 'syntax' in stderr.lower() or 'compile' in stderr.lower():
            return 'syntax_error'
        return 'runtime_error'
    
    # Default error
    if code != 0:
        return 'error'
    
    return 'passed'

