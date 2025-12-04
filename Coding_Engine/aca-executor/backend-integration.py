"""
Backend Integration for ACA Code Executor
Update your backend/executor.py to use this
"""

import os
import requests
from models import ExecuteRequest, ExecuteResponse

# Get Container App URL from environment
# Default URL will be set after deployment (get from Terraform output)
EXECUTOR_URL = os.getenv(
    'EXECUTOR_URL',
    'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io'
)


def execute_code_in_aca(request: ExecuteRequest) -> ExecuteResponse:
    """
    Execute code using ACA Code Executor
    """
    try:
        # Extract code from files
        code = request.files[0].content if request.files else ""
        language = request.language.lower()
        stdin = request.stdin or ""
        
        # Prepare payload
        payload = {
            'language': language,
            'code': code,
            'stdin': stdin,
            'timeout': 5
        }
        
        # Call ACA executor
        response = requests.post(
            f"{EXECUTOR_URL}/execute",
            json=payload,
            timeout=15,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            return ExecuteResponse(
                run={
                    'stdout': '',
                    'stderr': f'Executor error: {response.status_code} - {response.text}',
                    'code': 1
                },
                language=request.language,
                version=request.version
            )
        
        result = response.json()
        run_result = result.get('run', {})
        
        return ExecuteResponse(
            run={
                'stdout': run_result.get('stdout', ''),
                'stderr': run_result.get('stderr', ''),
                'code': run_result.get('code', 1)
            },
            language=request.language,
            version=request.version
        )
        
    except requests.exceptions.Timeout:
        return ExecuteResponse(
            run={
                'stdout': '',
                'stderr': 'Execution timeout - executor did not respond',
                'code': 124
            },
            language=request.language,
            version=request.version
        )
    except Exception as e:
        return ExecuteResponse(
            run={
                'stdout': '',
                'stderr': f'Error calling executor: {str(e)}',
                'code': 1
            },
            language=request.language,
            version=request.version
        )

