"""
Simple Code Execution Service for Pre-Warmed ACA Container Pool
This runs in regular ACA containers (no privileged mode needed)
"""

from flask import Flask, request, jsonify
import subprocess
import resource
import tempfile
import shutil
import os

app = Flask(__name__)

# Resource limits
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 256 * 1024 * 1024  # 256MB
EXECUTION_TIMEOUT = 5  # seconds


def set_resource_limits():
    """Set resource limits for security"""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
    except:
        pass  # Limits may not work in all environments


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/execute', methods=['POST'])
def execute():
    """
    Execute code in the container
    No privileged mode needed - just runs Python/Node directly
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        language = data.get('language', '').lower()
        code = data.get('code', '')
        stdin = data.get('stdin', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Execute based on language
        if language == 'python' or language == 'py':
            result = execute_python(code, stdin)
        elif language == 'javascript' or language == 'js' or language == 'node':
            result = execute_node(code, stdin)
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


def execute_python(code: str, stdin: str = ""):
    """Execute Python code"""
    try:
        result = subprocess.run(
            ['python3', '-c', code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT,
            preexec_fn=set_resource_limits
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timeout (exceeded {EXECUTION_TIMEOUT} seconds)',
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }


def execute_node(code: str, stdin: str = ""):
    """Execute Node.js code"""
    try:
        result = subprocess.run(
            ['node', '-e', code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT,
            preexec_fn=set_resource_limits
        )
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': f'Execution timeout (exceeded {EXECUTION_TIMEOUT} seconds)',
            'code': 124
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': f'Execution error: {str(e)}',
            'code': 1
        }


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Code Execution Service',
        'version': '1.0.0',
        'status': 'running',
        'supported_languages': ['python', 'javascript'],
        'replicas': os.environ.get('REPLICA_COUNT', 'unknown')
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)


