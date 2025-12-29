"""Main FastAPI application"""
import os
import uuid
import time
import logging
from datetime import datetime
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from executor_service.config import (
    EXECUTION_TIMEOUT, RATE_LIMIT_RUN, RATE_LIMIT_RUNALL
)
from executor_service.models import (
    RunRequest, RunAllRequest, ExecutionResponse, TestResult
)
from executor_service.security.sanitizer import sanitize_code, validate_test_case
from executor_service.security.network import block_network_access, restore_network_access
from executor_service.executors.python_executor import execute as execute_python
from executor_service.executors.node_executor import execute as execute_node
from executor_service.executors.java_executor import execute as execute_java
from executor_service.executors.cpp_executor import execute as execute_cpp
from executor_service.executors.cpp_batch_executor import execute_batch as execute_cpp_batch
from executor_service.executors.csharp_executor import execute as execute_csharp
from executor_service.utils.output import compare_outputs
from executor_service.utils.errors import detect_error_type

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def execute_code(language: str, code: str, test_input: str, timeout: int) -> Dict:
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    logger.info("🚀 Code execution service starting")
    yield
    logger.info("✅ Code execution service shutting down")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Code Execution Service",
    description="FastAPI-based code execution service with enhanced endpoints",
    version="4.0.0",
    lifespan=lifespan
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware (keeping as-is for now - will restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
async def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'Code Execution Service (FastAPI)',
        'version': '4.0.0',
        'replica': os.environ.get('REPLICA_NAME', 'unknown')
    }

@app.post('/run', response_model=ExecutionResponse)
@limiter.limit(RATE_LIMIT_RUN)
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
    
    # SECURITY FIX: Validate test case sizes
    for test_case in test_cases:
        is_valid, error_msg = validate_test_case(test_case)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
    
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
@limiter.limit(RATE_LIMIT_RUNALL)
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
    test_cases = runall_req.test_cases
    timeout = runall_req.timeout or EXECUTION_TIMEOUT
    
    # Validate inputs
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    if not test_cases:
        raise HTTPException(status_code=400, detail="Test cases are required")
    
    # SECURITY FIX: Validate test case sizes
    for test_case in test_cases:
        is_valid, error_msg = validate_test_case(test_case)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
    
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
        
        # Performance tracking: Test execution phase
        test_execution_start = time.time()
        logger.info(f"🚀 Starting execution of {len(test_cases)} test cases")
        
        # OPTIMIZATION: For compiled languages (C++) with multiple test cases, use batch execution
        if language in ['cpp', 'c++'] and len(test_cases) > 1:
            logger.info(f"⚡ Using optimized batch execution for C++ ({len(test_cases)} test cases)")
            test_inputs = [tc.input for tc in test_cases]
            
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
                
                error_type = detect_error_type(execution_result, timeout)
                actual_output = execution_result.get('stdout', '')
                stderr = execution_result.get('stderr', '')
                
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
            # Sequential execution for interpreted languages or single test case
            logger.info(f"📝 Using sequential execution (language: {language}, tests: {len(test_cases)})")
            for idx, test_case in enumerate(test_cases):
                test_input = test_case.input
                expected_output = test_case.expected_output
                test_case_id = test_case.id or f'test_{idx + 1}'
                
                test_start_time = time.time()
                try:
                    execution_result = execute_code(language, code, test_input, timeout)
                except Exception as e:
                    import traceback
                    error_trace = traceback.format_exc()
                    logger.error(f"Error in execute_code for test {test_case_id}: {e}\n{error_trace}")
                    restore_network_access(original_socket)
                    raise HTTPException(status_code=400, detail=f"Test case {test_case_id} execution failed: {str(e)}")
                
                if 'execution_time_ms' not in execution_result:
                    execution_result['execution_time_ms'] = int((time.time() - test_start_time) * 1000)
                
                error_type = detect_error_type(execution_result, timeout)
                actual_output = execution_result.get('stdout', '')
                stderr = execution_result.get('stderr', '')
                
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
        
        # Performance logging
        test_execution_time = int((time.time() - test_execution_start) * 1000)
        avg_time = test_execution_time / len(test_cases) if len(test_cases) > 0 else 0
        logger.info(f"⏱️ Test execution completed: {test_execution_time}ms for {len(test_cases)} test cases (avg: {avg_time:.1f}ms per test)")
        
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


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)

