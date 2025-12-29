"""
Code Execution Service with Test Case Support
Handles Python, JavaScript, Java, and C++ code execution with test cases
"""

from flask import Flask, request, jsonify
import subprocess
import resource
import tempfile
import shutil
import os
import sys
from datetime import datetime
import uuid

app = Flask(__name__)

# Resource limits for security
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 256 * 1024 * 1024  # 256MB
MAX_PROCESSES = 10
EXECUTION_TIMEOUT = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def set_resource_limits():
    """Set resource limits for code execution"""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_SIZE, MAX_FILE_SIZE))
    except Exception:
        pass  # Limits may not work in all environments


def normalize_output(output: str) -> str:
    """Normalize output for comparison (trim whitespace, handle newlines)"""
    if not output:
        return ""
    # Remove trailing whitespace and newlines
    return output.rstrip()


def compare_outputs(actual: str, expected: str) -> bool:
    """Compare actual output with expected output"""
    return normalize_output(actual) == normalize_output(expected)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Code Execution Service',
        'replica': os.environ.get('REPLICA_NAME', 'unknown')
    }), 200


@app.route('/execute', methods=['POST'])
def execute():
    """
    Execute code with test cases and return pass/fail results
    Expected JSON:
    {
        "language": "python",
        "code": "print('Hello World')",
        "test_cases": [
            {
                "id": "test_1",
                "input": "",
                "expected_output": "Hello World"
            }
        ],
        "timeout": 5,
        "user_id": "user123",
        "question_id": "q1"
    }
    """
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
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        if not test_cases:
            return jsonify({'error': 'No test cases provided'}), 400
        
        # Generate execution ID for tracking
        execution_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Run code against each test case
        test_results = []
        total_passed = 0
        total_failed = 0
        
        for idx, test_case in enumerate(test_cases):
            test_input = test_case.get('input', '')
            expected_output = test_case.get('expected_output', '')
            test_case_id = test_case.get('id', f'test_{idx + 1}')
            
            # Execute code with this test case
            if language in ['python', 'py']:
                execution_result = execute_python(code, test_input, timeout)
            elif language in ['javascript', 'js', 'node']:
                execution_result = execute_node(code, test_input, timeout)
            elif language in ['java']:
                execution_result = execute_java(code, test_input, timeout)
            elif language in ['cpp', 'c++']:
                execution_result = execute_cpp(code, test_input, timeout)
            else:
                return jsonify({
                    'error': f'Unsupported language: {language}',
                    'supported': ['python', 'javascript', 'java', 'cpp']
                }), 400
            
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
                    'execution_time': None
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
                    'execution_time': None  # Can be added if timing is needed
                }
                
                if passed:
                    total_passed += 1
                else:
                    total_failed += 1
            
            test_results.append(test_result)
        
        # Calculate overall status
        total_tests = len(test_cases)
        all_passed = total_passed == total_tests
        
        # Prepare response for database storage
        response_data = {
            'execution_id': execution_id,
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
                'replica': os.environ.get('REPLICA_NAME', 'unknown'),
                'timeout': timeout
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'execution_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


def execute_python(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Python code"""
    try:
        result = subprocess.run(
            ['python3', '-c', code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=set_resource_limits,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'PYTHONUNBUFFERED': '1'
            }
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }


def execute_node(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Node.js code"""
    try:
        result = subprocess.run(
            ['node', '-e', code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=set_resource_limits,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'NODE_ENV': 'production'
            }
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }


def execute_java(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Java code"""
    temp_dir = tempfile.mkdtemp(prefix='java_')
    
    try:
        # Write Java code to file
        java_file = os.path.join(temp_dir, 'Main.java')
        with open(java_file, 'w') as f:
            f.write(code)
        
        # Compile Java code
        compile_result = subprocess.run(
            ['javac', java_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir
        )
        
        if compile_result.returncode != 0:
            return {
                'stdout': '',
                'stderr': compile_result.stderr,
                'code': compile_result.returncode
            }
        
        # Execute compiled Java code
        result = subprocess.run(
            ['java', '-cp', temp_dir, 'Main'],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin'
            }
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def execute_cpp(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute C++ code"""
    temp_dir = tempfile.mkdtemp(prefix='cpp_')
    
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
            cwd=temp_dir
        )
        
        if compile_result.returncode != 0:
            return {
                'stdout': '',
                'stderr': compile_result.stderr,
                'code': compile_result.returncode
            }
        
        # Execute compiled C++ code
        result = subprocess.run(
            [os.path.join(temp_dir, 'main')],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin'
            }
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timeout (exceeded {timeout} seconds)',
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Code Execution Service with Test Cases',
        'version': '2.0.0',
        'status': 'running',
        'supported_languages': ['python', 'javascript', 'java', 'cpp'],
        'replica': os.environ.get('REPLICA_NAME', 'unknown')
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
