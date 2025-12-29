import os
import requests
import subprocess
import sys
import tempfile
import json
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from models import ExecuteRequest, ExecuteResponse

# Configuration
POOL_MANAGEMENT_ENDPOINT = os.getenv("POOL_MANAGEMENT_ENDPOINT")
USE_LOCAL_EXECUTOR = os.getenv("USE_LOCAL_EXECUTOR", "false").lower() == "true"

def get_auth_token():
    """
    Retrieves an authentication token for Azure Dynamic Sessions.
    Based on Azure docs: resource should be https://dynamicsessions.io
    """
    credential = DefaultAzureCredential()
    try:
        # Use the correct resource for Dynamic Sessions
        token = credential.get_token("https://dynamicsessions.io/.default")
        return token.token
    except Exception as e:
        print(f"⚠️  Auth token error: {e}")
        raise e

def execute_locally(request: ExecuteRequest) -> ExecuteResponse:
    """
    Executes code locally using subprocess.
    WARNING: This is for testing only and is NOT secure.
    """
    print("⚠️  WARNING: Executing code locally. This is insecure and for testing only.")
    
    code = request.files[0].content if request.files else ""
    language = request.language.lower()
    
    stdout = ""
    stderr = ""
    return_code = 0
    
    try:
        if language == "python":
            # Run Python code
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=5,
                input=request.stdin or ""
            )
            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode
            
        elif language == "javascript":
            # Try running with node if available
            try:
                result = subprocess.run(
                    ["node", "-e", code],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    input=request.stdin or ""
                )
                stdout = result.stdout
                stderr = result.stderr
                return_code = result.returncode
            except FileNotFoundError:
                stderr = "Node.js not found locally. Install node to test JS."
                return_code = 1
                
        else:
            stdout = f"Local execution for {language} not implemented in this mock."
            stderr = "Please use Python for local testing or deploy to Azure."
            return_code = 1
            
    except subprocess.TimeoutExpired:
        stderr = "Execution timed out."
        return_code = 124
    except Exception as e:
        stderr = f"Local execution error: {str(e)}"
        return_code = 1

    return {
        "run": {
            "stdout": stdout,
            "stderr": stderr,
            "code": return_code,
            "signal": None
        },
        "language": request.language,
        "version": request.version
    }

def execute_code_in_session(request: ExecuteRequest) -> ExecuteResponse:
    """
    Executes code using Azure Dynamic Sessions with correct session lifecycle.
    Follows the 3-step flow: Create Session → Execute Code → Cleanup Session
    """
    # NEVER fall back to local execution - all code must run in Azure
    if not POOL_MANAGEMENT_ENDPOINT:
        return {
            "run": {
                "stdout": "",
                "stderr": "ERROR: POOL_MANAGEMENT_ENDPOINT not configured. Code execution requires Azure Session Pool.",
                "code": 1,
                "signal": None
            },
            "language": request.language,
            "version": request.version
        }

    try:
        token = get_auth_token()
    except Exception as e:
        return {
            "run": {
                "stdout": "",
                "stderr": f"ERROR: Azure authentication failed: {str(e)}. Code execution requires Azure Session Pool.",
                "code": 1,
                "signal": None
            },
            "language": request.language,
            "version": request.version
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Use identifier-based flow (old API) - current pool doesn't support preview API
    # IMPORTANT: Use a STABLE identifier to reuse sessions and avoid 429 errors
    # Azure binds 1 pod per identifier - if identifier changes, Azure tries to allocate new pod
    # With max 5 concurrent sessions, random identifiers cause 429 errors
    
    # For now, use a stable test identifier (in production, use user_id + project_id or job_id)
    session_identifier = "test-session-1"
    
    # TODO: In production, use something like:
    # session_identifier = f"{request.user_id}-{request.project_id}" if hasattr(request, 'user_id') else "default-session"
    
    try:
        # ------------------------------------------
        # Execute code using identifier-based flow
        # ------------------------------------------
        code = request.files[0].content if request.files else ""
        stdin = request.stdin or ""
        
        # Old API: POST /sessions?identifier=<id> then POST /<path>?identifier=<id>
        # Azure will create/reuse session with this identifier
        execute_url = f"{POOL_MANAGEMENT_ENDPOINT}/python/execute?identifier={session_identifier}"
        payload = {
            "properties": {
                "code": code,
                "stdin": stdin
            }
        }
        
        print(f"🔍 Executing code with identifier: {execute_url}")
        print(f"🔍 Payload: {json.dumps(payload)[:150]}")
        
        exec_resp = requests.post(execute_url, headers=headers, json=payload)
        exec_resp.raise_for_status()
        result = exec_resp.json()
        
        # Extract response from adapter service format
        # Adapter returns: { "run": { "stdout": "...", "stderr": "...", "code": 0 } }
        run_data = result.get("run", {})
        
        return {
            "run": {
                "stdout": run_data.get("stdout", ""),
                "stderr": run_data.get("stderr", ""),
                "code": run_data.get("code", 0),
                "signal": None
            },
            "language": request.language,
            "version": request.version
        }
        
    except requests.exceptions.HTTPError as e:
        # Log the error but don't fall back to local - we want ALL code in Azure
        error_msg = f"Azure Session Pool Error: {str(e)}"
        if hasattr(e.response, 'text'):
            error_msg += f" - Response: {e.response.text[:200]}"
        print(f"❌ {error_msg}")
        return {
            "run": {
                "stdout": "",
                "stderr": error_msg,
                "code": 1,
                "signal": None
            },
            "language": request.language,
            "version": request.version
        }
    except Exception as e:
        # Any other error - still don't fall back to local
        error_msg = f"Azure Session Pool Error: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "run": {
                "stdout": "",
                "stderr": error_msg,
                "code": 1,
                "signal": None
            },
            "language": request.language,
            "version": request.version
        }

