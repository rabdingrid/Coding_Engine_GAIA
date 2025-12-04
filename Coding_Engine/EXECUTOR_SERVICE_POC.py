"""
Proof of Concept: Direct Code Execution Service for ACA
This replaces Piston and works without privileged mode.

Security Measures:
- Resource limits (CPU, memory, processes)
- Timeout enforcement
- Temporary file isolation
- No network access (optional)
"""

from flask import Flask, request, jsonify
import subprocess
import resource
import os
import tempfile
import shutil
import signal
import sys

app = Flask(__name__)

# Resource limits configuration
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 256 * 1024 * 1024  # 256MB
MAX_PROCESSES = 10
EXECUTION_TIMEOUT = 5  # seconds


def set_resource_limits():
    """Set resource limits for code execution"""
    try:
        # CPU time limit
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        
        # Memory limit
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        
        # Process limit
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        
        # File size limit (10MB)
        resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 1024 * 1024, 10 * 1024 * 1024))
    except Exception as e:
        print(f"Warning: Could not set all resource limits: {e}")


def execute_python(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Python code with security limits"""
    temp_dir = tempfile.mkdtemp(prefix='exec_')
    
    try:
        # Write code to file
        code_file = os.path.join(temp_dir, 'main.py')
        with open(code_file, 'w') as f:
            f.write(code)
        
        # Execute with timeout and resource limits
        result = subprocess.run(
            ['python3', code_file],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir,
            preexec_fn=set_resource_limits,
            # Security: Run in isolated directory
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'HOME': temp_dir,
                'TMPDIR': temp_dir,
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
            'stderr': 'Execution timeout (exceeded {} seconds)'.format(timeout),
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }
    finally:
        # Cleanup: Remove temporary directory
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass


def execute_node(code: str, stdin: str = "", timeout: int = EXECUTION_TIMEOUT):
    """Execute Node.js code with security limits"""
    temp_dir = tempfile.mkdtemp(prefix='exec_')
    
    try:
        # Write code to file
        code_file = os.path.join(temp_dir, 'main.js')
        with open(code_file, 'w') as f:
            f.write(code)
        
        # Execute with timeout and resource limits
        result = subprocess.run(
            ['node', code_file],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir,
            preexec_fn=set_resource_limits,
            env={
                'PATH': '/usr/local/bin:/usr/bin:/bin',
                'HOME': temp_dir,
                'TMPDIR': temp_dir,
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
            'stderr': 'Execution timeout (exceeded {} seconds)'.format(timeout),
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }
    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/execute', methods=['POST'])
def execute():
    """Execute code based on language"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        language = data.get('language', '').lower()
        code = data.get('code', '')
        stdin = data.get('stdin', '')
        timeout = data.get('timeout', EXECUTION_TIMEOUT)
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Route to appropriate executor
        if language == 'python' or language == 'py':
            result = execute_python(code, stdin, timeout)
        elif language == 'javascript' or language == 'js' or language == 'node':
            result = execute_node(code, stdin, timeout)
        else:
            return jsonify({
                'error': f'Unsupported language: {language}',
                'supported': ['python', 'javascript']
            }), 400
        
        return jsonify({
            'run': result,
            'language': language
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/', methods=['GET'])
def root():
    """Root endpoint with service info"""
    return jsonify({
        'service': 'Code Execution Service (POC)',
        'version': '1.0.0',
        'supported_languages': ['python', 'javascript'],
        'security': {
            'resource_limits': {
                'cpu_time': f'{MAX_CPU_TIME}s',
                'memory': f'{MAX_MEMORY / (1024*1024)}MB',
                'processes': MAX_PROCESSES,
                'timeout': f'{EXECUTION_TIMEOUT}s'
            }
        }
    }), 200


if __name__ == '__main__':
    # Run on port 8000 (ACA will map this)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)


