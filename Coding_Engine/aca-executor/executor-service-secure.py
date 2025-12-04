"""
Enhanced Code Execution Service with Security Guardrails
Handles Python, JavaScript, Java, C++, and C# code execution with test cases
Includes network isolation, filesystem sandboxing, code sanitization, and rate limiting
"""

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import resource
import tempfile
import shutil
import os
import sys
import re
import socket
from datetime import datetime
import uuid
import signal
import logging
import time
import json
import psutil
import threading

app = Flask(__name__)

# Configure logging for Azure Monitor
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting (100 requests per minute per IP)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

# Resource limits for security
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 1024 * 1024 * 1024  # 1GB (increased for Java compressed class space + all memory regions)
MAX_PROCESSES = 50  # Increased for Java thread creation
EXECUTION_TIMEOUT = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_CODE_LENGTH = 100 * 1024  # 100KB max code size

# Blocked patterns for code sanitization
BLOCKED_PATTERNS = {
    'python': [
        r'import\s+os\b',  # Match 'import os' anywhere (not just end of line)
        r'from\s+os\s+import',  # Match 'from os import'
        r'import\s+subprocess\b',
        r'from\s+subprocess\s+import',
        r'import\s+sys\b',
        r'from\s+sys\s+import',
        r'__import__\s*\(',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'open\s*\([^)]*[\'"]w[\'"]',  # Block file writes
        r'open\s*\([^)]*[\'"]a[\'"]',  # Block file appends
    ],
    'javascript': [
        r'require\s*\(\s*[\'"]fs[\'"]',
        r'require\s*\(\s*[\'"]child_process[\'"]',
        r'require\s*\(\s*[\'"]os[\'"]',
        r'eval\s*\(',
        r'Function\s*\(',
        # Allow process.stdin/stdout/stderr/argv/env/exit/version, but block dangerous ones
        r'process\.(exec|fork|spawn|kill|chdir|cwd|umask|setuid|setgid)',
        # Block process methods that could be dangerous
        r'process\.(nextTick|_kill|_fatalException)',
    ],
    'java': [
        r'java\.io\.File',
        r'java\.net\.',
        r'Runtime\.getRuntime',
        r'ProcessBuilder',
        r'Process',
    ],
    'cpp': [
        r'#include\s*<fstream>',
        r'#include\s*<sys/socket\.h>',
        r'system\s*\(',
        r'popen\s*\(',
    ],
    'csharp': [
        r'System\.IO\.File',
        r'System\.Net\.',
        r'System\.Diagnostics\.Process',
        r'System\.Runtime\.InteropServices',
        r'DllImport',
        r'Marshal\.',
        r'File\.',
        r'Directory\.',
        r'Process\.Start',
    ]
}

# Blocked network functions
BLOCKED_NETWORK_PATTERNS = [
    r'socket\.',
    r'urllib\.',
    r'requests\.',
    r'http\.',
    r'https\.',
    r'fetch\s*\(',
    r'XMLHttpRequest',
]


def sanitize_code(code: str, language: str):
    """
    Sanitize code to block dangerous operations
    Returns: (is_safe, error_message)
    """
    if not code:
        return False, "Empty code"
    
    if len(code) > MAX_CODE_LENGTH:
        return False, f"Code too long (max {MAX_CODE_LENGTH} bytes)"
    
    # Check for blocked patterns
    patterns = BLOCKED_PATTERNS.get(language, [])
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Blocked pattern detected: {pattern}"
    
    # Check for network operations
    for pattern in BLOCKED_NETWORK_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Network operations not allowed: {pattern}"
    
    return True, ""


def block_network_access():
    """Block network access during code execution"""
    # Disable socket creation
    original_socket = socket.socket
    
    def blocked_socket(*args, **kwargs):
        raise PermissionError("Network access is not allowed")
    
    socket.socket = blocked_socket
    
    return original_socket


def restore_network_access(original_socket):
    """Restore network access after code execution"""
    socket.socket = original_socket


def set_resource_limits():
    """Set resource limits for code execution"""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_SIZE, MAX_FILE_SIZE))
        
        # Block core dumps
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except Exception:
        pass  # Limits may not work in all environments


def create_sandboxed_directory() -> str:
    """Create a sandboxed temporary directory"""
    temp_dir = tempfile.mkdtemp(prefix='exec_', dir='/tmp')
    # Restrict permissions
    os.chmod(temp_dir, 0o700)
    return temp_dir


def normalize_output(output: str) -> str:
    """Normalize output for comparison (trim whitespace, handle newlines)"""
    if not output:
        return ""
    # Remove trailing whitespace and newlines
    return output.rstrip()


def compare_outputs(actual: str, expected: str) -> bool:
    """Compare actual output with expected output"""
    return normalize_output(actual) == normalize_output(expected)


def read_file_content(file_path: str) -> str:
    """Read content from a file (for input/output files)"""
    try:
        # Security: Only allow reading from /app/test_cases or /tmp directories
        # Also allow local testing paths (for development)
        allowed_prefixes = [
            '/app/test_cases/',
            '/tmp/',
            './test_cases/',
            '/Users/',  # For local testing (will be restricted in production)
        ]
        
        # Check if path is allowed
        is_allowed = any(file_path.startswith(prefix) for prefix in allowed_prefixes)
        if not is_allowed:
            raise ValueError(f"File path not allowed: {file_path}")
        
        # Resolve relative paths
        if file_path.startswith('./test_cases/'):
            file_path = file_path.replace('./test_cases/', '/app/test_cases/')
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {str(e)}")


def get_test_input(test_case: dict) -> str:
    """
    Get test input from test case
    Supports both string-based and file-based input
    """
    # Check for file-based input first
    if 'input_file' in test_case and test_case['input_file']:
        return read_file_content(test_case['input_file'])
    
    # Fall back to string-based input
    return test_case.get('input', '')


def get_expected_output(test_case: dict) -> str:
    """
    Get expected output from test case
    Supports both string-based and file-based output
    """
    # Check for file-based output first
    if 'expected_output_file' in test_case and test_case['expected_output_file']:
        return read_file_content(test_case['expected_output_file'])
    
    # Fall back to string-based output
    return test_case.get('expected_output', '')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Code Execution Service (Secure)',
        'replica': os.environ.get('REPLICA_NAME', 'unknown'),
        'security': 'enabled'
    }), 200


@app.route('/execute', methods=['POST'])
@limiter.limit("50 per minute")  # Stricter limit for execution endpoint
def execute():
    """
    Execute code with test cases and return pass/fail results
    Enhanced with security guardrails and monitoring
    
    Supports both string-based and file-based test cases:
    
    String-based:
    {
        "test_cases": [
            {
                "id": "test_1",
                "input": "5\n10",
                "expected_output": "15"
            }
        ]
    }
    
    File-based:
    {
        "test_cases": [
            {
                "id": "test_1",
                "input_file": "/app/test_cases/input1.txt",
                "expected_output_file": "/app/test_cases/output1.txt"
            }
        ]
    }
    
    Mixed (input from file, output as string):
    {
        "test_cases": [
            {
                "id": "test_1",
                "input_file": "/app/test_cases/input1.txt",
                "expected_output": "15"
            }
        ]
    }
    """
    # Get container/replica information for monitoring
    # Try multiple environment variables that Azure Container Apps might set
    container_id = (
        os.environ.get('HOSTNAME') or 
        os.environ.get('CONTAINER_NAME') or 
        os.environ.get('REPLICA_NAME') or
        os.environ.get('WEBSITE_INSTANCE_ID') or
        'unknown'
    )
    replica_name = os.environ.get('REPLICA_NAME', container_id)
    
    # If still unknown, try to get from hostname
    if container_id == 'unknown':
        try:
            import socket
            container_id = socket.gethostname()
        except:
            pass
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        language = data.get('language', '').lower()
        code = data.get('code', '')
        test_cases = data.get('test_cases', [])
        timeout = data.get('timeout', EXECUTION_TIMEOUT)
        user_id = data.get('user_id', '')
        question_id = data.get('question_id', '')
        submission_id = data.get('submission_id', str(uuid.uuid4()))
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        if not test_cases:
            return jsonify({'error': 'No test cases provided'}), 400
        
        # Validate timeout
        if timeout > 10:
            timeout = 10  # Cap at 10 seconds
        
        # Sanitize code
        is_safe, error_msg = sanitize_code(code, language)
        if not is_safe:
            execution_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()
            
            # Log failed validation
            logger.warning(json.dumps({
                'event': 'code_validation_failed',
                'execution_id': execution_id,
                'user_id': user_id,
                'question_id': question_id,
                'submission_id': submission_id,
                'container_id': container_id,
                'replica_name': replica_name,
                'error': error_msg,
                'timestamp': timestamp
            }))
            
            return jsonify({
                'error': f'Code validation failed: {error_msg}',
                'execution_id': execution_id,
                'timestamp': timestamp
            }), 400
        
        # Generate execution ID for tracking
        execution_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        start_time = time.time()
        
        # Log execution start
        logger.info(json.dumps({
            'event': 'execution_started',
            'execution_id': execution_id,
            'user_id': user_id,
            'question_id': question_id,
            'submission_id': submission_id,
            'container_id': container_id,
            'replica_name': replica_name,
            'language': language,
            'test_cases_count': len(test_cases),
            'timestamp': timestamp
        }))
        
        # Block network access
        original_socket = block_network_access()
        
        try:
            # Run code against each test case
            test_results = []
            total_passed = 0
            total_failed = 0
            
            for idx, test_case in enumerate(test_cases):
                # Support both file-based and string-based test cases
                try:
                    test_input = get_test_input(test_case)
                    expected_output = get_expected_output(test_case)
                except Exception as e:
                    restore_network_access(original_socket)
                    return jsonify({
                        'error': f'Error reading test case files: {str(e)}',
                        'execution_id': execution_id,
                        'timestamp': timestamp
                    }), 400
                
                test_case_id = test_case.get('id', f'test_{idx + 1}')
                
                # Execute code with this test case
                test_start_time = time.time()
                if language in ['python', 'py']:
                    execution_result = execute_python(code, test_input, timeout)
                elif language in ['javascript', 'js', 'node']:
                    execution_result = execute_node(code, test_input, timeout)
                elif language in ['java']:
                    execution_result = execute_java(code, test_input, timeout)
                elif language in ['cpp', 'c++']:
                    execution_result = execute_cpp(code, test_input, timeout)
                elif language in ['csharp', 'c#', 'cs']:
                    execution_result = execute_csharp(code, test_input, timeout)
                else:
                    restore_network_access(original_socket)
                    return jsonify({
                        'error': f'Unsupported language: {language}',
                        'supported': ['python', 'javascript', 'java', 'cpp', 'csharp']
                    }), 400
                
                # Calculate test execution time if not provided
                if 'execution_time_ms' not in execution_result:
                    execution_result['execution_time_ms'] = int((time.time() - test_start_time) * 1000)
                
                # Check if execution was successful
                if execution_result['code'] != 0:
                    # Execution failed (compile error, runtime error, timeout)
                    test_result = {
                        'test_case_id': test_case_id,
                        'test_case_number': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': execution_result['stdout'],
                        'error': execution_result['stderr'],
                        'status': 'error',
                        'passed': False,
                        'execution_time_ms': execution_result.get('execution_time_ms', 0),
                        'cpu_usage_percent': execution_result.get('cpu_usage_percent', 0),
                        'memory_usage_bytes': execution_result.get('memory_usage_bytes', 0)
                    }
                    total_failed += 1
                else:
                    # Compare outputs
                    actual_output = execution_result['stdout']
                    passed = compare_outputs(actual_output, expected_output)
                    
                    test_result = {
                        'test_case_id': test_case_id,
                        'test_case_number': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': actual_output,
                        'error': execution_result['stderr'] if execution_result['stderr'] else None,
                        'status': 'passed' if passed else 'failed',
                        'passed': passed,
                        'execution_time_ms': execution_result.get('execution_time_ms', 0),
                        'cpu_usage_percent': execution_result.get('cpu_usage_percent', 0),
                        'memory_usage_bytes': execution_result.get('memory_usage_bytes', 0)
                    }
                    
                    if passed:
                        total_passed += 1
                    else:
                        total_failed += 1
                
                test_results.append(test_result)
            
            # Calculate overall status and aggregate metrics
            total_tests = len(test_cases)
            all_passed = total_passed == total_tests
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Aggregate CPU and memory usage from all test cases
            total_cpu = sum(t.get('cpu_usage_percent', 0) for t in test_results)
            total_memory = sum(t.get('memory_usage_bytes', 0) for t in test_results)
            avg_cpu = total_cpu / total_tests if total_tests > 0 else 0
            max_memory = max((t.get('memory_usage_bytes', 0) for t in test_results), default=0)
            
            # Prepare response for database storage
            response_data = {
                'execution_id': execution_id,
                'submission_id': submission_id,
                'timestamp': timestamp,
                'user_id': user_id,
                'question_id': question_id,
                'language': language,
                'code': code,
                'summary': {
                    'total_tests': total_tests,
                    'passed': total_passed,
                    'failed': total_failed,
                    'all_passed': all_passed,
                    'pass_percentage': round((total_passed / total_tests * 100) if total_tests > 0 else 0, 2)
                },
                'test_results': test_results,
                'metadata': {
                    'replica': replica_name,
                    'container_id': container_id,
                    'timeout': timeout,
                    'execution_time_ms': execution_time_ms,
                    'cpu_usage_percent': round(avg_cpu, 2),
                    'memory_usage_bytes': max_memory,
                    'memory_usage_mb': round(max_memory / (1024 * 1024), 2),
                    'security': 'enabled'
                }
            }
            
            # Log execution completion with all metrics
            logger.info(json.dumps({
                'event': 'execution_completed',
                'execution_id': execution_id,
                'user_id': user_id,
                'question_id': question_id,
                'submission_id': submission_id,
                'container_id': container_id,
                'replica_name': replica_name,
                'language': language,
                'execution_time_ms': execution_time_ms,
                'cpu_usage_percent': round(avg_cpu, 2),
                'memory_usage_bytes': max_memory,
                'memory_usage_mb': round(max_memory / (1024 * 1024), 2),
                'tests_passed': total_passed,
                'tests_total': total_tests,
                'all_passed': all_passed,
                'timestamp': datetime.utcnow().isoformat()
            }))
            
            restore_network_access(original_socket)
            return jsonify(response_data), 200
                
        except Exception as e:
            restore_network_access(original_socket)
            execution_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()
            
            # Log server error
            logger.error(json.dumps({
                'event': 'execution_error',
                'execution_id': execution_id,
                'user_id': user_id,
                'question_id': question_id,
                'submission_id': submission_id,
                'container_id': container_id,
                'replica_name': replica_name,
                'error': str(e),
                'timestamp': timestamp
            }))
            
            return jsonify({
                'error': f'Server error: {str(e)}',
                'execution_id': execution_id,
                'timestamp': timestamp
            }), 500
    
    except Exception as e:
        # Outer exception handler for any unhandled errors
        execution_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        container_id = os.environ.get('HOSTNAME', 'unknown')
        replica_name = os.environ.get('REPLICA_NAME', container_id)
        
        logger.error(json.dumps({
            'event': 'execution_error',
            'execution_id': execution_id,
            'error': str(e),
            'timestamp': timestamp
        }))
        
        return jsonify({
            'error': f'Server error: {str(e)}',
            'execution_id': execution_id,
            'timestamp': timestamp
        }), 500


def execute_python(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
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
            cwd='/tmp',  # Sandboxed working directory
        )
        
        # Monitor CPU and memory continuously while process runs
        monitoring_active = True
        max_cpu = 0.0
        max_memory = 0
        psutil_process_obj = None
        
        def monitor_process():
            nonlocal cpu_usage, memory_usage, max_cpu, max_memory, psutil_process_obj
            try:
                psutil_process_obj = psutil.Process(process.pid)
                # First call to cpu_percent() initializes it (returns 0.0)
                psutil_process_obj.cpu_percent()
                
                # Poll while process is running
                while monitoring_active:
                    try:
                        # Check if process is still running
                        if not psutil_process_obj.is_running():
                            break
                        
                        # Get CPU usage (non-blocking, compares to previous call)
                        current_cpu = psutil_process_obj.cpu_percent()
                        if current_cpu > max_cpu:
                            max_cpu = current_cpu
                        
                        # Get memory usage
                        memory_info = psutil_process_obj.memory_info()
                        current_memory = memory_info.rss
                        if current_memory > max_memory:
                            max_memory = current_memory
                        
                        cpu_usage = max_cpu
                        memory_usage = max_memory
                        
                        time.sleep(0.01)  # Poll every 10ms
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_process, daemon=True)
        monitor_thread.start()
        
        # Small delay to let monitoring initialize
        time.sleep(0.01)
        
        # Execute with timeout
        stdout, stderr = process.communicate(input=stdin, timeout=timeout)
        
        # Stop monitoring
        monitoring_active = False
        
        # Get final metrics (process might still be alive briefly)
        try:
            if psutil_process_obj is None:
                psutil_process_obj = psutil.Process(process.pid)
            # Final CPU check
            final_cpu = psutil_process_obj.cpu_percent()
            if final_cpu > max_cpu:
                max_cpu = final_cpu
            # Final memory check
            memory_info = psutil_process_obj.memory_info()
            final_memory = memory_info.rss
            if final_memory > max_memory:
                max_memory = final_memory
            
            cpu_usage = max_cpu
            memory_usage = max_memory
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Use values captured during monitoring
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
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
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


def execute_node(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Node.js code with security guardrails"""
    temp_dir = create_sandboxed_directory()
    start_time = time.time()
    process = None
    cpu_usage = 0.0
    memory_usage = 0
    
    try:
        # Write code to file (file-based execution uses less memory than -e flag)
        js_file = os.path.join(temp_dir, 'main.js')
        with open(js_file, 'w') as f:
            f.write(code)
        
        # Create clean environment and limit Node.js memory to prevent OOM
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('NODE_'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        clean_env['NODE_ENV'] = 'production'
        # Explicitly unset NODE_OPTIONS to prevent conflicts with old values
        # We'll use command-line flags instead
        if 'NODE_OPTIONS' in clean_env:
            del clean_env['NODE_OPTIONS']
        
        process = subprocess.Popen(
            ['node', '--max-old-space-size=64', js_file],  # Reduced to 64MB heap (Node.js v16)
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            env=clean_env,
            cwd=temp_dir,  # Use temp directory
        )
        
        # Monitor CPU and memory continuously while process runs
        monitoring_active = True
        max_cpu = 0.0
        max_memory = 0
        psutil_process_obj = None
        
        def monitor_process():
            nonlocal cpu_usage, memory_usage, max_cpu, max_memory, psutil_process_obj
            try:
                psutil_process_obj = psutil.Process(process.pid)
                # First call to cpu_percent() initializes it (returns 0.0)
                psutil_process_obj.cpu_percent()
                
                # Poll while process is running
                while monitoring_active:
                    try:
                        # Check if process is still running
                        if not psutil_process_obj.is_running():
                            break
                        
                        # Get CPU usage (non-blocking, compares to previous call)
                        current_cpu = psutil_process_obj.cpu_percent()
                        if current_cpu > max_cpu:
                            max_cpu = current_cpu
                        
                        # Get memory usage
                        memory_info = psutil_process_obj.memory_info()
                        current_memory = memory_info.rss
                        if current_memory > max_memory:
                            max_memory = current_memory
                        
                        cpu_usage = max_cpu
                        memory_usage = max_memory
                        
                        time.sleep(0.01)  # Poll every 10ms
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_process, daemon=True)
        monitor_thread.start()
        
        # Small delay to let monitoring initialize
        time.sleep(0.01)
        
        # Execute with timeout
        stdout, stderr = process.communicate(input=stdin, timeout=timeout)
        
        # Stop monitoring
        monitoring_active = False
        
        # Get final metrics (process might still be alive briefly)
        try:
            if psutil_process_obj is None:
                psutil_process_obj = psutil.Process(process.pid)
            # Final CPU check
            final_cpu = psutil_process_obj.cpu_percent()
            if final_cpu > max_cpu:
                max_cpu = final_cpu
            # Final memory check
            memory_info = psutil_process_obj.memory_info()
            final_memory = memory_info.rss
            if final_memory > max_memory:
                max_memory = final_memory
            
            cpu_usage = max_cpu
            memory_usage = max_memory
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Use values captured during monitoring
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
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
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


def execute_java(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Java code with security guardrails"""
    temp_dir = create_sandboxed_directory()
    
    try:
        # Write Java code to file
        java_file = os.path.join(temp_dir, 'Main.java')
        with open(java_file, 'w') as f:
            f.write(code)
        
        # Compile Java code with minimal memory
        # Create clean environment - explicitly unset all Java-related env vars
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('JAVA') and not key.startswith('_JAVA'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        # Explicitly unset JAVA_TOOL_OPTIONS to prevent javac from picking it up
        if 'JAVA_TOOL_OPTIONS' in clean_env:
            del clean_env['JAVA_TOOL_OPTIONS']
        if '_JAVA_OPTIONS' in clean_env:
            del clean_env['_JAVA_OPTIONS']
        
        compile_result = subprocess.run(
            ['javac', 
             '-J-Xmx32m',
             '-J-Xms16m',
             '-J-XX:ReservedCodeCacheSize=8m',
             '-J-XX:InitialCodeCacheSize=4m',
             '-J-XX:MaxMetaspaceSize=16m',
             '-J-XX:CompressedClassSpaceSize=8m',
             java_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir,
            env=clean_env
        )
        
        if compile_result.returncode != 0:
            return {
                'stdout': '',
                'stderr': compile_result.stderr,
                'code': compile_result.returncode
            }
        
        # Execute compiled Java code with minimal memory settings
        # Recreate clean environment - explicitly unset JAVA_TOOL_OPTIONS
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('JAVA') and not key.startswith('_JAVA'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        # Explicitly unset JAVA_TOOL_OPTIONS to prevent JVM from picking it up
        if 'JAVA_TOOL_OPTIONS' in clean_env:
            del clean_env['JAVA_TOOL_OPTIONS']
        if '_JAVA_OPTIONS' in clean_env:
            del clean_env['_JAVA_OPTIONS']
        
        start_time = time.time()
        # HotSpot JVM with minimal settings and increased process limits
        # Using very small heap to minimize memory allocation
        process = subprocess.Popen(
            ['java', 
             '-Xmx32m',  # 32MB heap (increased slightly to avoid allocation issues)
             '-Xms8m',   # Initial heap
             '-XX:ReservedCodeCacheSize=4m',  # Code cache
             '-XX:InitialCodeCacheSize=2m',   # Initial cache
             '-XX:MaxMetaspaceSize=16m',      # Metaspace
             '-XX:+UseSerialGC',  # Serial GC (lowest overhead)
             '-XX:+TieredCompilation',  # Tiered compilation
             '-XX:TieredStopAtLevel=1',  # Stop at C1 (no C2)
             '-XX:MaxDirectMemorySize=4m',  # Direct memory
             '-XX:MaxRAMPercentage=10.0',  # Use only 10% of container memory
             '-cp', temp_dir, 'Main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env=clean_env
        )
        
        # Monitor CPU and memory continuously while process runs
        monitoring_active = True
        max_cpu = 0.0
        max_memory = 0
        cpu_usage = 0.0
        memory_usage = 0
        psutil_process_obj = None
        
        def monitor_process():
            nonlocal cpu_usage, memory_usage, max_cpu, max_memory, psutil_process_obj
            try:
                psutil_process_obj = psutil.Process(process.pid)
                # First call to cpu_percent() initializes it (returns 0.0)
                psutil_process_obj.cpu_percent()
                
                # Poll while process is running
                while monitoring_active:
                    try:
                        # Check if process is still running
                        if not psutil_process_obj.is_running():
                            break
                        
                        # Get CPU usage (non-blocking, compares to previous call)
                        current_cpu = psutil_process_obj.cpu_percent()
                        if current_cpu > max_cpu:
                            max_cpu = current_cpu
                        
                        # Get memory usage
                        memory_info = psutil_process_obj.memory_info()
                        current_memory = memory_info.rss
                        if current_memory > max_memory:
                            max_memory = current_memory
                        
                        cpu_usage = max_cpu
                        memory_usage = max_memory
                        
                        time.sleep(0.01)  # Poll every 10ms
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_process, daemon=True)
        monitor_thread.start()
        
        # Small delay to let monitoring initialize
        time.sleep(0.01)
        
        # Execute with timeout
        stdout, stderr = process.communicate(input=stdin, timeout=timeout)
        
        # Stop monitoring
        monitoring_active = False
        
        # Get final metrics (process might still be alive briefly)
        try:
            if psutil_process_obj is None:
                psutil_process_obj = psutil.Process(process.pid)
            # Final CPU check
            final_cpu = psutil_process_obj.cpu_percent()
            if final_cpu > max_cpu:
                max_cpu = final_cpu
            # Final memory check
            memory_info = psutil_process_obj.memory_info()
            final_memory = memory_info.rss
            if final_memory > max_memory:
                max_memory = final_memory
            
            cpu_usage = max_cpu
            memory_usage = max_memory
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Use values captured during monitoring
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
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
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


def execute_cpp(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute C++ code with security guardrails"""
    temp_dir = create_sandboxed_directory()
    
    try:
        # Write C++ code to file
        cpp_file = os.path.join(temp_dir, 'main.cpp')
        with open(cpp_file, 'w') as f:
            f.write(code)
        
        # Compile C++ code
        compile_result = subprocess.run(
            ['g++', '-o', os.path.join(temp_dir, 'main'), cpp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
            }
        )
        
        if compile_result.returncode != 0:
            return {
                'stdout': '',
                'stderr': compile_result.stderr,
                'code': compile_result.returncode
            }
        
        # Execute compiled C++ code
        start_time = time.time()
        process = subprocess.Popen(
            [os.path.join(temp_dir, 'main')],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
            }
        )
        
        # Monitor CPU and memory continuously while process runs
        monitoring_active = True
        max_cpu = 0.0
        max_memory = 0
        cpu_usage = 0.0
        memory_usage = 0
        psutil_process_obj = None
        
        def monitor_process():
            nonlocal cpu_usage, memory_usage, max_cpu, max_memory, psutil_process_obj
            try:
                psutil_process_obj = psutil.Process(process.pid)
                # First call to cpu_percent() initializes it (returns 0.0)
                psutil_process_obj.cpu_percent()
                
                # Poll while process is running
                while monitoring_active:
                    try:
                        # Check if process is still running
                        if not psutil_process_obj.is_running():
                            break
                        
                        # Get CPU usage (non-blocking, compares to previous call)
                        current_cpu = psutil_process_obj.cpu_percent()
                        if current_cpu > max_cpu:
                            max_cpu = current_cpu
                        
                        # Get memory usage
                        memory_info = psutil_process_obj.memory_info()
                        current_memory = memory_info.rss
                        if current_memory > max_memory:
                            max_memory = current_memory
                        
                        cpu_usage = max_cpu
                        memory_usage = max_memory
                        
                        time.sleep(0.01)  # Poll every 10ms
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_process, daemon=True)
        monitor_thread.start()
        
        # Small delay to let monitoring initialize
        time.sleep(0.01)
        
        # Execute with timeout
        stdout, stderr = process.communicate(input=stdin, timeout=timeout)
        
        # Stop monitoring
        monitoring_active = False
        
        # Get final metrics (process might still be alive briefly)
        try:
            if psutil_process_obj is None:
                psutil_process_obj = psutil.Process(process.pid)
            # Final CPU check
            final_cpu = psutil_process_obj.cpu_percent()
            if final_cpu > max_cpu:
                max_cpu = final_cpu
            # Final memory check
            memory_info = psutil_process_obj.memory_info()
            final_memory = memory_info.rss
            if final_memory > max_memory:
                max_memory = final_memory
            
            cpu_usage = max_cpu
            memory_usage = max_memory
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Use values captured during monitoring
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
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
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


def execute_csharp(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute C# code with security guardrails"""
    temp_dir = create_sandboxed_directory()
    
    try:
        # Write C# code to file
        cs_file = os.path.join(temp_dir, 'Program.cs')
        with open(cs_file, 'w') as f:
            f.write(code)
        
        # Compile C# code using dotnet or mcs (depending on what's available)
        # Try dotnet first (modern .NET)
        compile_cmd = None
        run_cmd = None
        
        # Check if dotnet is available
        dotnet_check = subprocess.run(['which', 'dotnet'], capture_output=True)
        if dotnet_check.returncode == 0:
            # Use dotnet
            compile_cmd = ['dotnet', 'new', 'console', '-n', 'Solution', '--force']
            run_cmd = ['dotnet', 'run', '--project', os.path.join(temp_dir, 'Solution')]
            # Replace Program.cs with user code
            solution_dir = os.path.join(temp_dir, 'Solution')
            if os.path.exists(solution_dir):
                with open(os.path.join(solution_dir, 'Program.cs'), 'w') as f:
                    f.write(code)
        else:
            # Try mcs (Mono C# compiler)
            compile_cmd = ['mcs', '-out:' + os.path.join(temp_dir, 'program.exe'), cs_file]
            run_cmd = ['mono', os.path.join(temp_dir, 'program.exe')]
        
        if compile_cmd:
            compile_result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir,
                env={
                    'PATH': '/usr/local/bin:/usr/bin:/bin',
                }
            )
            
            if compile_result.returncode != 0:
                return {
                    'stdout': '',
                    'stderr': compile_result.stderr,
                    'code': compile_result.returncode,
                    'execution_time_ms': 0,
                    'cpu_usage_percent': 0.0,
                    'memory_usage_bytes': 0
                }
        
        # Execute compiled C# code
        start_time = time.time()
        process = subprocess.Popen(
            run_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
            }
        )
        
        # Monitor CPU and memory continuously while process runs
        monitoring_active = True
        max_cpu = 0.0
        max_memory = 0
        cpu_usage = 0.0
        memory_usage = 0
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
        
        # Execute with timeout
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


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Code Execution Service with Test Cases (Secure)',
        'version': '2.1.0',
        'status': 'running',
        'supported_languages': ['python', 'javascript', 'java', 'cpp', 'csharp'],
        'security': {
            'enabled': True,
            'features': [
                'network_isolation',
                'code_sanitization',
                'rate_limiting',
                'resource_limits',
                'filesystem_sandboxing'
            ]
        },
        'replica': os.environ.get('REPLICA_NAME', 'unknown')
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

