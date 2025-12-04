"""
FastAPI Code Execution Service with Enhanced Endpoints
Handles Python, JavaScript, Java, C++, and C# code execution with test cases
Includes /run, /runall, and /submit endpoints with database integration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
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
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncpg
from contextlib import asynccontextmanager

# Database connection pool (will be initialized on startup)
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    global db_pool
    # Startup
    try:
        # Initialize database connection pool
        db_url = os.environ.get('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')
        db_pool = await asyncpg.create_pool(
            db_url,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        logger.info("✅ Database connection pool created")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        db_pool = None
    
    yield
    
    # Shutdown
    if db_pool:
        await db_pool.close()
        logger.info("✅ Database connection pool closed")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Code Execution Service",
    description="FastAPI-based code execution service with enhanced endpoints",
    version="3.0.0",
    lifespan=lifespan
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Resource limits for security
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 1024 * 1024 * 1024  # 1GB
MAX_PROCESSES = 50
EXECUTION_TIMEOUT = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_CODE_LENGTH = 100 * 1024  # 100KB max code size

# Blocked patterns for code sanitization (same as Flask version)
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
    ],
    'javascript': [
        r'require\s*\(\s*[\'"]fs[\'"]',
        r'require\s*\(\s*[\'"]child_process[\'"]',
        r'require\s*\(\s*[\'"]os[\'"]',
        r'eval\s*\(',
        r'Function\s*\(',
        r'process\.(exec|fork|spawn|kill|chdir|cwd|umask|setuid|setgid)',
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

BLOCKED_NETWORK_PATTERNS = [
    r'socket\.',
    r'urllib\.',
    r'requests\.',
    r'http\.',
    r'https\.',
    r'fetch\s*\(',
    r'XMLHttpRequest',
]

# Pydantic models for request/response
class TestCase(BaseModel):
    id: str
    input: str
    expected_output: str

class RunRequest(BaseModel):
    """Request for /run endpoint - code + boilerplate + sample test cases"""
    language: str = Field(..., description="Programming language: python, java, cpp, javascript, csharp")
    code: str = Field(..., description="Complete code (user code + boilerplate merged)")
    sample_test_cases: List[TestCase] = Field(..., description="Sample test cases to run")
    user_id: Optional[str] = None
    question_id: Optional[str] = None
    timeout: Optional[int] = EXECUTION_TIMEOUT

class RunAllRequest(BaseModel):
    """Request for /runall endpoint - code + boilerplate + all test cases (except sample)"""
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Complete code (user code + boilerplate merged)")
    test_cases: List[TestCase] = Field(..., description="All test cases (excluding sample)")
    sample_test_cases: List[TestCase] = Field(default=[], description="Sample test cases (for reference, not executed)")
    user_id: Optional[str] = None
    question_id: Optional[str] = None
    timeout: Optional[int] = EXECUTION_TIMEOUT

class SubmitRequest(BaseModel):
    """Request for /submit endpoint - code + boilerplate + all test cases, saves to DB"""
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Complete code (user code + boilerplate merged)")
    test_cases: List[TestCase] = Field(..., description="All test cases")
    sample_test_cases: List[TestCase] = Field(default=[], description="Sample test cases (for reference)")
    user_id: str = Field(..., description="User/Candidate ID (required for submission)")
    question_id: str = Field(..., description="Question ID (required for submission)")
    candidate_id: Optional[str] = None
    timeout: Optional[int] = EXECUTION_TIMEOUT

class TestResult(BaseModel):
    test_case_id: str
    test_case_number: int
    input: str
    expected_output: str
    actual_output: str
    error: Optional[str] = None
    status: str  # 'passed', 'failed', 'error', 'tle', 'mle', 'syntax_error'
    passed: bool
    execution_time_ms: int
    cpu_usage_percent: float
    memory_usage_bytes: int

class ExecutionResponse(BaseModel):
    execution_id: str
    summary: Dict[str, Any]
    test_results: List[TestResult]
    metadata: Dict[str, Any]
    timestamp: str

# Helper functions (same as Flask version)
def sanitize_code(code: str, language: str):
    """Sanitize code to block dangerous operations"""
    if not code:
        return False, "Empty code"
    
    if len(code) > MAX_CODE_LENGTH:
        return False, f"Code too long (max {MAX_CODE_LENGTH} bytes)"
    
    patterns = BLOCKED_PATTERNS.get(language, [])
    for pattern in patterns:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Blocked pattern detected: {pattern}"
    
    for pattern in BLOCKED_NETWORK_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE | re.MULTILINE):
            return False, f"Network operations not allowed: {pattern}"
    
    return True, ""

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

def set_resource_limits():
    """Set resource limits for code execution"""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_SIZE, MAX_FILE_SIZE))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except Exception:
        pass

def create_sandboxed_directory() -> str:
    """Create a sandboxed temporary directory"""
    temp_dir = tempfile.mkdtemp(prefix='exec_', dir='/tmp')
    os.chmod(temp_dir, 0o700)
    return temp_dir

def normalize_output(output: str) -> str:
    """Normalize output for comparison"""
    if not output:
        return ""
    return output.rstrip()

def compare_outputs(actual: str, expected: str) -> bool:
    """Compare actual output with expected output"""
    return normalize_output(actual) == normalize_output(expected)

def detect_error_type(execution_result: dict, timeout: int) -> str:
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

# Execution functions (same as Flask version - will copy the full implementations)
# For brevity, I'll include the key parts and reference the original functions

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
            cwd='/tmp',
        )
        
        # Monitor CPU and memory (same as Flask version)
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

# Similar implementations for execute_node, execute_java, execute_cpp, execute_csharp
# (Copying from executor-service-secure.py - will include full implementations)

def execute_node(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Node.js code - same as Flask version"""
    temp_dir = create_sandboxed_directory()
    start_time = time.time()
    process = None
    cpu_usage = 0.0
    memory_usage = 0
    
    try:
        js_file = os.path.join(temp_dir, 'main.js')
        with open(js_file, 'w') as f:
            f.write(code)
        
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('NODE_'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        clean_env['NODE_ENV'] = 'production'
        if 'NODE_OPTIONS' in clean_env:
            del clean_env['NODE_OPTIONS']
        
        process = subprocess.Popen(
            ['node', '--max-old-space-size=64', js_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            env=clean_env,
            cwd=temp_dir,
        )
        
        # Monitor CPU and memory (same pattern as Python)
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
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def execute_java(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Java code - same as Flask version"""
    temp_dir = create_sandboxed_directory()
    
    try:
        java_file = os.path.join(temp_dir, 'Main.java')
        with open(java_file, 'w') as f:
            f.write(code)
        
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('JAVA') and not key.startswith('_JAVA'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        if 'JAVA_TOOL_OPTIONS' in clean_env:
            del clean_env['JAVA_TOOL_OPTIONS']
        if '_JAVA_OPTIONS' in clean_env:
            del clean_env['_JAVA_OPTIONS']
        
        compile_result = subprocess.run(
            ['javac', 
             '-J-Xmx32m', '-J-Xms16m',
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
                'code': compile_result.returncode,
                'execution_time_ms': 0,
                'cpu_usage_percent': 0.0,
                'memory_usage_bytes': 0
            }
        
        start_time = time.time()
        process = subprocess.Popen(
            ['java', 
             '-Xmx32m', '-Xms8m',
             '-XX:ReservedCodeCacheSize=4m',
             '-XX:InitialCodeCacheSize=2m',
             '-XX:MaxMetaspaceSize=16m',
             '-XX:+UseSerialGC',
             '-XX:+TieredCompilation',
             '-XX:TieredStopAtLevel=1',
             '-XX:MaxDirectMemorySize=4m',
             '-XX:MaxRAMPercentage=10.0',
             '-cp', temp_dir, 'Main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env=clean_env
        )
        
        # Monitor CPU and memory
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

def execute_cpp(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute C++ code - same as Flask version"""
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
            env={'PATH': '/usr/local/bin:/usr/bin:/bin'}
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
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env={'PATH': '/usr/local/bin:/usr/bin:/bin'}
        )
        
        # Monitor CPU and memory
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

def execute_csharp(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute C# code - same as Flask version"""
    temp_dir = create_sandboxed_directory()
    
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

def execute_code(language: str, code: str, test_input: str, timeout: int):
    """Route to appropriate execution function"""
    language = language.lower()
    if language in ['python', 'py']:
        return execute_python(code, test_input, timeout)
    elif language in ['javascript', 'js', 'node']:
        return execute_node(code, test_input, timeout)
    elif language == 'java':
        return execute_java(code, test_input, timeout)
    elif language in ['cpp', 'c++']:
        return execute_cpp(code, test_input, timeout)
    elif language in ['csharp', 'c#', 'cs']:
        return execute_csharp(code, test_input, timeout)
    else:
        raise ValueError(f'Unsupported language: {language}')

async def save_submission_to_db(
    user_id: str,
    question_id: str,
    language: str,
    code: str,
    test_results: List[Dict],
    summary: Dict,
    execution_id: str
):
    """Save submission results to database"""
    if not db_pool:
        logger.warning("Database pool not available, skipping save")
        return
    
    try:
        async with db_pool.acquire() as conn:
            # Create submissions table if it doesn't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id SERIAL PRIMARY KEY,
                    submission_id VARCHAR(255) UNIQUE,
                    user_id VARCHAR(255) NOT NULL,
                    question_id VARCHAR(255) NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    code TEXT NOT NULL,
                    test_results JSONB NOT NULL,
                    summary JSONB NOT NULL,
                    execution_id VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert submission
            submission_id = str(uuid.uuid4())
            await conn.execute("""
                INSERT INTO submissions (
                    submission_id, user_id, question_id, language, code,
                    test_results, summary, execution_id
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, submission_id, user_id, question_id, language, code,
                json.dumps(test_results), json.dumps(summary), execution_id)
            
            logger.info(f"✅ Submission saved: {submission_id}")
            return submission_id
    except Exception as e:
        logger.error(f"❌ Error saving submission: {e}")
        raise

# API Endpoints

@app.get('/health')
async def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'Code Execution Service (FastAPI)',
        'version': '3.0.0',
        'replica': os.environ.get('REPLICA_NAME', 'unknown')
    }

@app.post('/run', response_model=ExecutionResponse)
@limiter.limit("50 per minute")
async def run(request: Request, run_req: RunRequest):
    """
    Run code with sample test cases only
    Input: code (including boilerplate) + sample_test_cases
    """
    execution_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    start_time = time.time()
    
    language = run_req.language.lower()
    code = run_req.code
    test_cases = run_req.sample_test_cases
    timeout = run_req.timeout or EXECUTION_TIMEOUT
    
    # Validate inputs
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    if not test_cases:
        raise HTTPException(status_code=400, detail="Sample test cases are required")
    
    # Sanitize code
    is_safe, error_msg = sanitize_code(code, language)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Code validation failed: {error_msg}")
    
    # Block network access
    original_socket = block_network_access()
    
    try:
        container_id = os.environ.get('HOSTNAME', 'unknown')
        replica_name = os.environ.get('REPLICA_NAME', container_id)
        
        test_results = []
        total_passed = 0
        total_failed = 0
        
        for idx, test_case in enumerate(test_cases):
            test_input = test_case.input
            expected_output = test_case.expected_output
            test_case_id = test_case.id or f'test_{idx + 1}'
            
            # Execute code
            test_start_time = time.time()
            try:
                execution_result = execute_code(language, code, test_input, timeout)
            except ValueError as e:
                restore_network_access(original_socket)
                raise HTTPException(status_code=400, detail=str(e))
            
            if 'execution_time_ms' not in execution_result:
                execution_result['execution_time_ms'] = int((time.time() - test_start_time) * 1000)
            
            # Detect error type
            error_type = detect_error_type(execution_result, timeout)
            actual_output = execution_result.get('stdout', '')
            stderr = execution_result.get('stderr', '')
            
            # Determine status and passed
            if error_type in ['tle', 'mle', 'syntax_error', 'runtime_error', 'error']:
                status = error_type
                passed = False
                total_failed += 1
            else:
                # Compare outputs
                passed = compare_outputs(actual_output, expected_output)
                status = 'passed' if passed else 'failed'
                if passed:
                    total_passed += 1
                else:
                    total_failed += 1
            
            test_result = {
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
            }
            
            test_results.append(test_result)
        
        # Calculate summary
        total_tests = len(test_cases)
        all_passed = total_passed == total_tests
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Aggregate metrics
        total_cpu = sum(t.get('cpu_usage_percent', 0) for t in test_results)
        total_memory = sum(t.get('memory_usage_bytes', 0) for t in test_results)
        avg_cpu = total_cpu / total_tests if total_tests > 0 else 0
        max_memory = max((t.get('memory_usage_bytes', 0) for t in test_results), default=0)
        
        response = ExecutionResponse(
            execution_id=execution_id,
            summary={
                'total_tests': total_tests,
                'passed': total_passed,
                'failed': total_failed,
                'all_passed': all_passed,
                'pass_percentage': round((total_passed / total_tests * 100) if total_tests > 0 else 0, 2)
            },
            test_results=[TestResult(**tr) for tr in test_results],
            metadata={
                'replica': replica_name,
                'container_id': container_id,
                'timeout': timeout,
                'execution_time_ms': execution_time_ms,
                'cpu_usage_percent': round(avg_cpu, 2),
                'memory_usage_bytes': max_memory,
                'memory_usage_mb': round(max_memory / (1024 * 1024), 2),
                'endpoint': 'run',
                'test_type': 'sample'
            },
            timestamp=timestamp
        )
        
        restore_network_access(original_socket)
        return response
        
    except HTTPException:
        restore_network_access(original_socket)
        raise
    except Exception as e:
        restore_network_access(original_socket)
        logger.error(f"Error in /run: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post('/runall', response_model=ExecutionResponse)
@limiter.limit("50 per minute")
async def runall(request: Request, runall_req: RunAllRequest):
    """
    Run code with all test cases (excluding sample)
    Input: code (including boilerplate) + test_cases (all except sample)
    """
    execution_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    start_time = time.time()
    
    language = runall_req.language.lower()
    code = runall_req.code
    test_cases = runall_req.test_cases  # All test cases except sample
    timeout = runall_req.timeout or EXECUTION_TIMEOUT
    
    # Validate inputs
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    if not test_cases:
        raise HTTPException(status_code=400, detail="Test cases are required")
    
    # Sanitize code
    is_safe, error_msg = sanitize_code(code, language)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Code validation failed: {error_msg}")
    
    # Block network access
    original_socket = block_network_access()
    
    try:
        container_id = os.environ.get('HOSTNAME', 'unknown')
        replica_name = os.environ.get('REPLICA_NAME', container_id)
        
        test_results = []
        total_passed = 0
        total_failed = 0
        
        for idx, test_case in enumerate(test_cases):
            test_input = test_case.input
            expected_output = test_case.expected_output
            test_case_id = test_case.id or f'test_{idx + 1}'
            
            # Execute code
            test_start_time = time.time()
            try:
                execution_result = execute_code(language, code, test_input, timeout)
            except ValueError as e:
                restore_network_access(original_socket)
                raise HTTPException(status_code=400, detail=str(e))
            
            if 'execution_time_ms' not in execution_result:
                execution_result['execution_time_ms'] = int((time.time() - test_start_time) * 1000)
            
            # Detect error type
            error_type = detect_error_type(execution_result, timeout)
            actual_output = execution_result.get('stdout', '')
            stderr = execution_result.get('stderr', '')
            
            # Determine status and passed
            if error_type in ['tle', 'mle', 'syntax_error', 'runtime_error', 'error']:
                status = error_type
                passed = False
                total_failed += 1
            else:
                # Compare outputs
                passed = compare_outputs(actual_output, expected_output)
                status = 'passed' if passed else 'failed'
                if passed:
                    total_passed += 1
                else:
                    total_failed += 1
            
            test_result = {
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
            }
            
            test_results.append(test_result)
        
        # Calculate summary
        total_tests = len(test_cases)
        all_passed = total_passed == total_tests
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Aggregate metrics
        total_cpu = sum(t.get('cpu_usage_percent', 0) for t in test_results)
        total_memory = sum(t.get('memory_usage_bytes', 0) for t in test_results)
        avg_cpu = total_cpu / total_tests if total_tests > 0 else 0
        max_memory = max((t.get('memory_usage_bytes', 0) for t in test_results), default=0)
        
        response = ExecutionResponse(
            execution_id=execution_id,
            summary={
                'total_tests': total_tests,
                'passed': total_passed,
                'failed': total_failed,
                'all_passed': all_passed,
                'pass_percentage': round((total_passed / total_tests * 100) if total_tests > 0 else 0, 2)
            },
            test_results=[TestResult(**tr) for tr in test_results],
            metadata={
                'replica': replica_name,
                'container_id': container_id,
                'timeout': timeout,
                'execution_time_ms': execution_time_ms,
                'cpu_usage_percent': round(avg_cpu, 2),
                'memory_usage_bytes': max_memory,
                'memory_usage_mb': round(max_memory / (1024 * 1024), 2),
                'endpoint': 'runall',
                'test_type': 'all'
            },
            timestamp=timestamp
        )
        
        restore_network_access(original_socket)
        return response
        
    except HTTPException:
        restore_network_access(original_socket)
        raise
    except Exception as e:
        restore_network_access(original_socket)
        logger.error(f"Error in /runall: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post('/submit', response_model=ExecutionResponse)
@limiter.limit("30 per minute")
async def submit(request: Request, submit_req: SubmitRequest):
    """
    Submit code with all test cases and save results to database
    Input: code (including boilerplate) + test_cases (all) + user_id + question_id
    Output: Results saved to DB with pass/fail details
    """
    execution_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    start_time = time.time()
    
    language = submit_req.language.lower()
    code = submit_req.code
    test_cases = submit_req.test_cases  # All test cases
    timeout = submit_req.timeout or EXECUTION_TIMEOUT
    user_id = submit_req.user_id
    question_id = submit_req.question_id
    
    # Validate inputs
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    if not test_cases:
        raise HTTPException(status_code=400, detail="Test cases are required")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required for submission")
    
    if not question_id:
        raise HTTPException(status_code=400, detail="question_id is required for submission")
    
    # Sanitize code
    is_safe, error_msg = sanitize_code(code, language)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Code validation failed: {error_msg}")
    
    # Block network access
    original_socket = block_network_access()
    
    try:
        container_id = os.environ.get('HOSTNAME', 'unknown')
        replica_name = os.environ.get('REPLICA_NAME', container_id)
        
        test_results = []
        total_passed = 0
        total_failed = 0
        
        for idx, test_case in enumerate(test_cases):
            test_input = test_case.input
            expected_output = test_case.expected_output
            test_case_id = test_case.id or f'test_{idx + 1}'
            
            # Execute code
            test_start_time = time.time()
            try:
                execution_result = execute_code(language, code, test_input, timeout)
            except ValueError as e:
                restore_network_access(original_socket)
                raise HTTPException(status_code=400, detail=str(e))
            
            if 'execution_time_ms' not in execution_result:
                execution_result['execution_time_ms'] = int((time.time() - test_start_time) * 1000)
            
            # Detect error type
            error_type = detect_error_type(execution_result, timeout)
            actual_output = execution_result.get('stdout', '')
            stderr = execution_result.get('stderr', '')
            
            # Determine status and passed
            if error_type in ['tle', 'mle', 'syntax_error', 'runtime_error', 'error']:
                status = error_type
                passed = False
                total_failed += 1
            else:
                # Compare outputs
                passed = compare_outputs(actual_output, expected_output)
                status = 'passed' if passed else 'failed'
                if passed:
                    total_passed += 1
                else:
                    total_failed += 1
            
            test_result = {
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
            }
            
            test_results.append(test_result)
        
        # Calculate summary
        total_tests = len(test_cases)
        all_passed = total_passed == total_tests
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Aggregate metrics
        total_cpu = sum(t.get('cpu_usage_percent', 0) for t in test_results)
        total_memory = sum(t.get('memory_usage_bytes', 0) for t in test_results)
        avg_cpu = total_cpu / total_tests if total_tests > 0 else 0
        max_memory = max((t.get('memory_usage_bytes', 0) for t in test_results), default=0)
        
        summary = {
            'total_tests': total_tests,
            'passed': total_passed,
            'failed': total_failed,
            'all_passed': all_passed,
            'pass_percentage': round((total_passed / total_tests * 100) if total_tests > 0 else 0, 2)
        }
        
        # Save to database
        try:
            submission_id = await save_submission_to_db(
                user_id=user_id,
                question_id=question_id,
                language=language,
                code=code,
                test_results=test_results,
                summary=summary,
                execution_id=execution_id
            )
        except Exception as e:
            logger.error(f"Failed to save submission: {e}")
            # Continue even if DB save fails
        
        response = ExecutionResponse(
            execution_id=execution_id,
            summary=summary,
            test_results=[TestResult(**tr) for tr in test_results],
            metadata={
                'replica': replica_name,
                'container_id': container_id,
                'timeout': timeout,
                'execution_time_ms': execution_time_ms,
                'cpu_usage_percent': round(avg_cpu, 2),
                'memory_usage_bytes': max_memory,
                'memory_usage_mb': round(max_memory / (1024 * 1024), 2),
                'endpoint': 'submit',
                'test_type': 'all',
                'submission_id': submission_id if 'submission_id' in locals() else None,
                'saved_to_db': db_pool is not None
            },
            timestamp=timestamp
        )
        
        restore_network_access(original_socket)
        return response
        
    except HTTPException:
        restore_network_access(original_socket)
        raise
    except Exception as e:
        restore_network_access(original_socket)
        logger.error(f"Error in /submit: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)

