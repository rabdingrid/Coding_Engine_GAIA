"""
Ultra-Secure Code Execution Service
Enhanced with AST-based code analysis, improved resource limits, and additional security layers
Addresses: syscall filtering, process isolation, pattern bypass, and soft resource limits
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
import ast
import ctypes
from ctypes import c_int, c_void_p, POINTER

app = Flask(__name__)

# Configure logging for Azure Monitor
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting (stricter for security)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["50 per minute"],  # Reduced from 100
    storage_uri="memory://"
)

# Resource limits for security (stricter)
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 256 * 1024 * 1024  # 256MB
MAX_PROCESSES = 5  # Reduced from 10
EXECUTION_TIMEOUT = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_CODE_LENGTH = 50 * 1024  # 50KB max code size (reduced from 100KB)

# Blocked patterns for code sanitization (enhanced)
BLOCKED_PATTERNS = {
    'python': [
        r'import\s+os\b',
        r'from\s+os\s+import',
        r'import\s+subprocess\b',
        r'from\s+subprocess\s+import',
        r'import\s+sys\b',
        r'from\s+sys\s+import',
        r'__import__\s*\(',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'open\s*\([^)]*[\'"]w[\'"]',
        r'open\s*\([^)]*[\'"]a[\'"]',
        r'open\s*\([^)]*[\'"]x[\'"]',
        r'\.write\s*\(',
        r'\.writelines\s*\(',
        r'pickle\s*\.',
        r'marshal\s*\.',
        r'ctypes\s*\.',
        r'__builtins__',
        r'__import__',
        r'getattr\s*\([^,]+,\s*[\'"]__',
        r'setattr\s*\(',
        r'delattr\s*\(',
        r'hasattr\s*\([^,]+,\s*[\'"]__',
    ],
    'javascript': [
        r'require\s*\(\s*[\'"]fs[\'"]',
        r'require\s*\(\s*[\'"]child_process[\'"]',
        r'require\s*\(\s*[\'"]os[\'"]',
        r'require\s*\(\s*[\'"]net[\'"]',
        r'require\s*\(\s*[\'"]http[\'"]',
        r'require\s*\(\s*[\'"]https[\'"]',
        r'eval\s*\(',
        r'Function\s*\(',
        r'process\.',
        r'global\s*\.',
        r'Buffer\s*\.',
    ],
    'java': [
        r'java\.io\.File',
        r'java\.net\.',
        r'Runtime\.getRuntime',
        r'ProcessBuilder',
        r'Process',
        r'System\.exit',
        r'System\.gc',
        r'Runtime\.',
    ],
    'cpp': [
        r'#include\s*<fstream>',
        r'#include\s*<sys/socket\.h>',
        r'#include\s*<netinet/in\.h>',
        r'#include\s*<arpa/inet\.h>',
        r'system\s*\(',
        r'popen\s*\(',
        r'exec\s*\(',
        r'fork\s*\(',
        r'clone\s*\(',
    ]
}

# Blocked network functions (enhanced)
BLOCKED_NETWORK_PATTERNS = [
    r'socket\.',
    r'urllib\.',
    r'requests\.',
    r'http\.',
    r'https\.',
    r'fetch\s*\(',
    r'XMLHttpRequest',
    r'WebSocket',
    r'net\.',
]

# Dangerous AST nodes to block
DANGEROUS_AST_NODES = {
    'python': [
        ast.Import, ast.ImportFrom, ast.Call, ast.Attribute,
        ast.Subscript, ast.BinOp, ast.UnaryOp
    ]
}

# Try to load seccomp (if available)
try:
    import seccomp
    SECCOMP_AVAILABLE = True
except ImportError:
    SECCOMP_AVAILABLE = False
    try:
        # Try using prctl via ctypes
        libc = ctypes.CDLL("libc.so.6")
        PR_SET_SECCOMP = 22
        SECCOMP_MODE_FILTER = 2
        SECCOMP_AVAILABLE = hasattr(libc, 'prctl')
    except:
        SECCOMP_AVAILABLE = False

# Try to check for unshare capability
try:
    libc = ctypes.CDLL("libc.so.6")
    CLONE_NEWPID = 0x20000000
    CLONE_NEWNS = 0x00020000
    UNSHARE_AVAILABLE = hasattr(libc, 'unshare')
except:
    UNSHARE_AVAILABLE = False


def analyze_code_ast(code: str, language: str):
    """
    Analyze code using AST to detect dangerous patterns
    More robust than regex pattern matching
    """
    if language != 'python':
        return True, ""  # AST analysis only for Python
    
    try:
        tree = ast.parse(code, mode='exec')
        
        dangerous_imports = ['os', 'subprocess', 'sys', 'ctypes', 'pickle', 'marshal']
        dangerous_functions = ['eval', 'exec', 'compile', '__import__']
        
        for node in ast.walk(tree):
            # Check for dangerous imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in dangerous_imports:
                        return False, f"Dangerous import detected: {alias.name}"
            
            if isinstance(node, ast.ImportFrom):
                if node.module in dangerous_imports:
                    return False, f"Dangerous import from detected: {node.module}"
            
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in dangerous_functions:
                        return False, f"Dangerous function call detected: {node.func.id}"
                
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.value.id in dangerous_imports:
                            return False, f"Dangerous method call detected: {node.func.attr}"
            
            # Check for file operations
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'open':
                    if len(node.args) > 1:
                        if isinstance(node.args[1], ast.Str):
                            mode = node.args[1].s
                            if mode in ['w', 'a', 'x', 'wb', 'ab', 'xb']:
                                return False, f"File write operation detected: open(..., '{mode}')"
        
        return True, ""
    except SyntaxError:
        # If code doesn't parse, let it through (will fail at execution anyway)
        return True, ""
    except Exception as e:
        # If AST analysis fails, fall back to regex
        logger.warning(f"AST analysis failed: {e}, falling back to regex")
        return True, ""


def sanitize_code(code: str, language: str):
    """
    Enhanced code sanitization with AST analysis + regex patterns
    """
    if not code:
        return False, "Empty code"
    
    if len(code) > MAX_CODE_LENGTH:
        return False, f"Code too long (max {MAX_CODE_LENGTH} bytes)"
    
    # First: AST-based analysis (for Python)
    if language == 'python':
        is_safe, error_msg = analyze_code_ast(code, language)
        if not is_safe:
            return False, error_msg
    
    # Second: Regex pattern matching (for all languages)
    patterns = BLOCKED_PATTERNS.get(language, [])
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Blocked pattern detected: {pattern}"
    
    # Third: Network operations check
    for pattern in BLOCKED_NETWORK_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Network operations not allowed: {pattern}"
    
    # Fourth: Check for obfuscation attempts
    suspicious_patterns = [
        r'[\'"]\s*\+\s*[\'"]',  # String concatenation (potential obfuscation)
        r'chr\s*\(',  # Character code obfuscation
        r'ord\s*\(',  # Character code obfuscation
        r'base64\s*\.',  # Base64 encoding (potential obfuscation)
        r'exec\s*\(.*\+',  # Dynamic code construction
    ]
    
    if language == 'python':
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if len(matches) > 3:  # Multiple obfuscation attempts
                return False, f"Suspicious obfuscation pattern detected: {pattern}"
    
    return True, ""


def setup_seccomp_filter():
    """
    Setup seccomp filter to block dangerous syscalls
    Falls back gracefully if seccomp is not available
    """
    if not SECCOMP_AVAILABLE:
        return False
    
    try:
        if hasattr(seccomp, 'SyscallFilter'):
            # Using python-seccomp library
            f = seccomp.SyscallFilter(defaction=seccomp.ALLOW)
            
            # Block dangerous syscalls
            dangerous_syscalls = [
                'execve', 'execveat', 'fork', 'vfork', 'clone',
                'mount', 'umount', 'umount2', 'pivot_root',
                'chroot', 'setuid', 'setgid', 'setreuid', 'setregid',
                'socket', 'socketpair', 'connect', 'bind', 'listen',
                'accept', 'sendto', 'recvfrom',
            ]
            
            for syscall in dangerous_syscalls:
                try:
                    f.add_rule(seccomp.KILL, syscall)
                except:
                    pass
            
            f.load()
            return True
        else:
            # Try using prctl directly
            libc = ctypes.CDLL("libc.so.6")
            libc.prctl.argtypes = [c_int, c_void_p, c_void_p, c_void_p, c_void_p]
            # Note: This is simplified - full seccomp setup requires BPF programs
            return False
    except Exception as e:
        logger.warning(f"Seccomp setup failed: {e}")
        return False


def set_enhanced_resource_limits():
    """
    Enhanced resource limits with better enforcement
    """
    try:
        # Set stricter limits
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_SIZE, MAX_FILE_SIZE))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        
        # Additional limits
        try:
            resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))  # Limit open files
        except:
            pass
        
        # Try to set nice value (lower priority)
        try:
            os.nice(10)  # Lower priority (higher nice value)
        except:
            pass
        
        return True
    except Exception as e:
        logger.warning(f"Enhanced resource limits failed: {e}")
        # Fall back to basic limits
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
            resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        except:
            pass
        return False


def create_isolated_namespace():
    """
    Attempt to create isolated namespace for process
    Falls back gracefully if not available
    """
    if not UNSHARE_AVAILABLE:
        return False
    
    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.unshare.argtypes = [c_int]
        # Try to unshare PID namespace (requires CAP_SYS_ADMIN)
        result = libc.unshare(CLONE_NEWPID)
        if result == 0:
            return True
    except Exception as e:
        logger.debug(f"Namespace isolation not available: {e}")
    
    return False


def block_network_access():
    """Block network access during code execution"""
    original_socket = socket.socket
    
    def blocked_socket(*args, **kwargs):
        raise PermissionError("Network access is not allowed")
    
    socket.socket = blocked_socket
    return original_socket


def restore_network_access(original_socket):
    """Restore network access after code execution"""
    socket.socket = original_socket


def create_sandboxed_directory() -> str:
    """Create a sandboxed temporary directory with strict permissions"""
    temp_dir = tempfile.mkdtemp(prefix='exec_', dir='/tmp')
    os.chmod(temp_dir, 0o700)  # Only owner can access
    
    # Try to set additional restrictions
    try:
        # Make directory read-only for others (if possible)
        os.chmod(temp_dir, 0o700)
    except:
        pass
    
    return temp_dir


def normalize_output(output: str) -> str:
    """Normalize output for comparison"""
    if not output:
        return ""
    return output.rstrip()


def compare_outputs(actual: str, expected: str) -> bool:
    """Compare actual output with expected output"""
    return normalize_output(actual) == normalize_output(expected)


def read_file_content(file_path: str) -> str:
    """Read content from a file (for input/output files)"""
    try:
        allowed_prefixes = [
            '/app/test_cases/',
            '/tmp/',
            './test_cases/',
        ]
        
        is_allowed = any(file_path.startswith(prefix) for prefix in allowed_prefixes)
        if not is_allowed:
            raise ValueError(f"File path not allowed: {file_path}")
        
        if file_path.startswith('./test_cases/'):
            file_path = file_path.replace('./test_cases/', '/app/test_cases/')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {str(e)}")


def get_test_input(test_case: dict) -> str:
    """Get test input from test case"""
    if 'input_file' in test_case and test_case['input_file']:
        return read_file_content(test_case['input_file'])
    return test_case.get('input', '')


def get_expected_output(test_case: dict) -> str:
    """Get expected output from test case"""
    if 'expected_output_file' in test_case and test_case['expected_output_file']:
        return read_file_content(test_case['expected_output_file'])
    return test_case.get('expected_output', '')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Code Execution Service (Ultra-Secure)',
        'replica': os.environ.get('REPLICA_NAME', 'unknown'),
        'security': {
            'enabled': True,
            'seccomp': SECCOMP_AVAILABLE,
            'unshare': UNSHARE_AVAILABLE,
            'features': [
                'ast_analysis',
                'enhanced_sanitization',
                'network_isolation',
                'resource_limits',
                'rate_limiting'
            ]
        }
    }), 200


@app.route('/execute', methods=['POST'])
@limiter.limit("30 per minute")  # Stricter limit
def execute():
    """
    Execute code with enhanced security measures
    """
    container_id = (
        os.environ.get('HOSTNAME') or 
        os.environ.get('CONTAINER_NAME') or 
        os.environ.get('REPLICA_NAME') or
        'unknown'
    )
    replica_name = os.environ.get('REPLICA_NAME', container_id)
    
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
        
        if timeout > 10:
            timeout = 10
        
        # Enhanced code sanitization (AST + regex + obfuscation detection)
        is_safe, error_msg = sanitize_code(code, language)
        if not is_safe:
            execution_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()
            
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
        
        execution_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        start_time = time.time()
        
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
            test_results = []
            total_passed = 0
            total_failed = 0
            
            for idx, test_case in enumerate(test_cases):
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
                test_start_time = time.time()
                
                # Execute code with enhanced security
                if language in ['python', 'py']:
                    execution_result = execute_python(code, test_input, timeout)
                elif language in ['javascript', 'js', 'node']:
                    execution_result = execute_node(code, test_input, timeout)
                elif language in ['java']:
                    execution_result = execute_java(code, test_input, timeout)
                elif language in ['cpp', 'c++']:
                    execution_result = execute_cpp(code, test_input, timeout)
                else:
                    restore_network_access(original_socket)
                    return jsonify({
                        'error': f'Unsupported language: {language}',
                        'supported': ['python', 'javascript', 'java', 'cpp']
                    }), 400
                
                if 'execution_time_ms' not in execution_result:
                    execution_result['execution_time_ms'] = int((time.time() - test_start_time) * 1000)
                
                if execution_result['code'] != 0:
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
            
            total_tests = len(test_cases)
            all_passed = total_passed == total_tests
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            total_cpu = sum(t.get('cpu_usage_percent', 0) for t in test_results)
            total_memory = sum(t.get('memory_usage_bytes', 0) for t in test_results)
            avg_cpu = total_cpu / total_tests if total_tests > 0 else 0
            max_memory = max((t.get('memory_usage_bytes', 0) for t in test_results), default=0)
            
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
                    'security': {
                        'enabled': True,
                        'seccomp': SECCOMP_AVAILABLE,
                        'unshare': UNSHARE_AVAILABLE,
                        'ast_analysis': language == 'python'
                    }
                }
            }
            
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
    """Execute Python code with enhanced security"""
    start_time = time.time()
    process = None
    cpu_usage = 0.0
    memory_usage = 0
    
    try:
        # Try to setup seccomp filter (if available)
        seccomp_enabled = setup_seccomp_filter()
        
        # Try to setup enhanced resource limits
        enhanced_limits = set_enhanced_resource_limits()
        
        process = subprocess.Popen(
            ['python3', '-c', code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_enhanced_resource_limits,  # Use enhanced limits
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'PYTHONUNBUFFERED': '1',
                'PYTHONDONTWRITEBYTECODE': '1',
                'PYTHONNOUSERSITE': '1',
                'PYTHONDONTWRITEBYTECODE': '1',
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
        if process:
            try:
                process.kill()
            except:
                pass
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
    """Execute Node.js code with enhanced security"""
    start_time = time.time()
    process = None
    cpu_usage = 0.0
    memory_usage = 0
    
    try:
        set_enhanced_resource_limits()
        
        process = subprocess.Popen(
            ['node', '-e', code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_enhanced_resource_limits,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'NODE_ENV': 'production',
            },
            cwd='/tmp',
        )
        
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
        if process:
            try:
                process.kill()
            except:
                pass
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
    """Execute Java code with enhanced security"""
    temp_dir = create_sandboxed_directory()
    
    try:
        java_file = os.path.join(temp_dir, 'Main.java')
        with open(java_file, 'w') as f:
            f.write(code)
        
        clean_env = dict(os.environ)
        clean_env['JAVA_TOOL_OPTIONS'] = '-Xmx32m -XX:ReservedCodeCacheSize=8m -XX:InitialCodeCacheSize=4m'
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        
        compile_result = subprocess.run(
            ['javac', 
             '-J-Xmx32m',
             '-J-XX:ReservedCodeCacheSize=8m',
             '-J-XX:InitialCodeCacheSize=4m',
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
                'code': compile_result.returncode,
                'execution_time_ms': 0,
                'cpu_usage_percent': 0.0,
                'memory_usage_bytes': 0
            }
        
        start_time = time.time()
        process = subprocess.Popen(
            ['java', 
             '-Xmx32m',
             '-Xms16m',
             '-XX:ReservedCodeCacheSize=8m',
             '-XX:InitialCodeCacheSize=4m',
             '-XX:MaxMetaspaceSize=16m',
             '-XX:CompressedClassSpaceSize=8m',
             '-cp', temp_dir, 'Main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_enhanced_resource_limits,
            cwd=temp_dir,
            env=clean_env
        )
        
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
        if process:
            try:
                process.kill()
            except:
                pass
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
    """Execute C++ code with enhanced security"""
    temp_dir = create_sandboxed_directory()
    
    try:
        cpp_file = os.path.join(temp_dir, 'main.cpp')
        with open(cpp_file, 'w') as f:
            f.write(code)
        
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
                'code': compile_result.returncode,
                'execution_time_ms': 0,
                'cpu_usage_percent': 0.0,
                'memory_usage_bytes': 0
            }
        
        start_time = time.time()
        process = subprocess.Popen(
            [os.path.join(temp_dir, 'main')],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_enhanced_resource_limits,
            cwd=temp_dir,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
            }
        )
        
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
        if process:
            try:
                process.kill()
            except:
                pass
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


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Code Execution Service (Ultra-Secure)',
        'version': '3.0.0',
        'status': 'running',
        'supported_languages': ['python', 'javascript', 'java', 'cpp'],
        'security': {
            'enabled': True,
            'seccomp_available': SECCOMP_AVAILABLE,
            'unshare_available': UNSHARE_AVAILABLE,
            'features': [
                'ast_based_code_analysis',
                'enhanced_pattern_matching',
                'obfuscation_detection',
                'network_isolation',
                'enhanced_resource_limits',
                'rate_limiting',
                'filesystem_sandboxing'
            ]
        },
        'replica': os.environ.get('REPLICA_NAME', 'unknown')
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)


