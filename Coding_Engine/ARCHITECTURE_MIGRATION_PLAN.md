# Architecture Migration Plan: Session Pool → ACA Only

## 🎯 Executive Summary

**Current**: Azure Session Pool (Dynamic Sessions) with Piston  
**Proposed**: Azure Container Apps (ACA) only with GitHub Actions + Terraform  
**Challenge**: Piston requires privileged mode, ACA doesn't support it

---

## 📊 Current vs Proposed Architecture

### Current Architecture (Session Pool)
```
User Request
    ↓
Backend (ACA) - Port 8000
    ↓
Session Pool (Dynamic Sessions)
    ↓
Container with Piston (privileged mode)
    ↓
Code Execution
```

**Pros**:
- ✅ Hyper-V isolation (hardware-level security)
- ✅ Automatic scaling
- ✅ Pay-per-use pricing
- ✅ No privileged mode issues (runs in Session Pool)

**Cons**:
- ⚠️ Ingress configuration complexity
- ⚠️ Session Pool is preview feature
- ⚠️ Limited language support (custom images needed)

---

### Proposed Architecture (ACA Only)
```
User Request
    ↓
GitHub Actions (Request Queue/Spinner)
    ↓
Terraform Script (via GitHub Actions)
    ↓
Deploy New ACA Container per Request
    ↓
Code Execution in Container
    ↓
Cleanup Container
```

**Pros**:
- ✅ No privileged mode needed (if using alternatives)
- ✅ Full control over container lifecycle
- ✅ Standard ACA features (scaling, ingress)
- ✅ Infrastructure as Code (Terraform)

**Cons**:
- ❌ **Container creation overhead** (30-60 seconds per request)
- ❌ **Cost**: Each execution = new container = higher cost
- ❌ **Complexity**: GitHub Actions + Terraform orchestration
- ❌ **Security**: Container-level isolation (not hardware-level)
- ❌ **Scalability**: Limited by GitHub Actions concurrency

---

## 🔍 Critical Analysis: Is This Feasible?

### ❌ Problem 1: Container Creation Latency

**Issue**: Creating a new ACA container per code execution takes **30-60 seconds**.

```
Request → GitHub Actions → Terraform → ACA Deploy → Execute → Cleanup
         (5-10s)         (20-30s)    (10-20s)     (1-5s)   (5-10s)
Total: ~50-75 seconds per code execution
```

**Impact**: 
- Users wait 50-75 seconds for code execution
- Not suitable for real-time coding contests
- Poor user experience

**Current Session Pool**: ~1-3 seconds (container already running)

---

### ❌ Problem 2: GitHub Actions as Request Queue

**Limitations**:
- GitHub Actions has **concurrency limits**:
  - Free: 20 concurrent jobs
  - Pro: 40 concurrent jobs
  - Enterprise: 180 concurrent jobs
- **Not designed for request queuing**
- **Rate limiting**: 1000 API calls/hour per repository
- **Cost**: GitHub Actions minutes cost money at scale

**Better Alternatives**:
- Azure Service Bus (proper message queue)
- Azure Queue Storage
- Azure Functions (event-driven)
- Azure Logic Apps

---

### ❌ Problem 3: Piston Alternative Needed

**Why Piston Needs Privileged Mode**:
- Piston dynamically creates/manages containers
- Requires Docker daemon access
- Needs `CAP_SYS_ADMIN` capabilities

**Alternatives That Work in ACA**:

#### Option A: **Code-Server / Theia** (Browser-based IDE)
- ✅ No privileged mode needed
- ✅ Runs in regular container
- ❌ Not for code execution, only editing
- ❌ Doesn't solve execution problem

#### Option B: **Direct Language Runtimes** (Python, Node, etc.)
- ✅ No privileged mode needed
- ✅ Fast execution
- ❌ **Security Risk**: User code runs directly in container
- ❌ No sandboxing/isolation
- ❌ Vulnerable to container escape

#### Option C: **Firecracker MicroVMs** (via Kata Containers)
- ✅ Hardware-level isolation
- ✅ No privileged mode in host
- ❌ **Not supported in ACA**
- ❌ Requires AKS or VMs

#### Option D: **gVisor** (User-space kernel)
- ✅ Better isolation than regular containers
- ✅ No privileged mode needed
- ❌ **Not supported in ACA**
- ❌ Requires Kubernetes

#### Option E: **Custom Sandbox** (Python `subprocess` with restrictions)
- ✅ No privileged mode needed
- ✅ Works in ACA
- ⚠️ **Limited security**: Not as secure as Piston
- ⚠️ Requires careful implementation

---

## ✅ Recommended Solution: Hybrid Approach

### Architecture: ACA + Azure Functions + Direct Execution

```
User Request
    ↓
Backend (ACA) - Port 8000
    ↓
Azure Function (Queue Manager)
    ↓
ACA Container (Pre-warmed Pool)
    ↓
Direct Language Runtime (Python/Node/etc.)
    ↓
Code Execution (with resource limits)
```

**Components**:

1. **Backend (ACA)**: Receives requests
2. **Azure Function**: Manages queue and container allocation
3. **ACA Container Pool**: Pre-warmed containers ready for execution
4. **Execution Engine**: Direct language runtime (Python, Node, etc.)

**Security Measures**:
- Resource limits (CPU, memory, timeout)
- Network restrictions
- File system read-only (except temp)
- Process limits
- No network access (or restricted)

---

## 📋 Detailed Implementation Plan

### Phase 1: Replace Piston with Direct Execution

#### Step 1: Create Execution Container

**Dockerfile** (`Dockerfile.executor`):
```dockerfile
FROM python:3.11-slim

# Install language runtimes
RUN apt-get update && apt-get install -y \
    nodejs \
    openjdk-17-jdk \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Create execution service
COPY executor-service.py /app/executor-service.py
WORKDIR /app

# Run as non-root user
RUN useradd -m executor && chown -R executor:executor /app
USER executor

EXPOSE 8000
CMD ["python", "executor-service.py"]
```

#### Step 2: Execution Service (Python)

**`executor-service.py`**:
```python
from flask import Flask, request, jsonify
import subprocess
import resource
import os
import tempfile
import shutil

app = Flask(__name__)

# Set resource limits
def set_limits():
    # CPU time: 10 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
    # Memory: 256MB
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    # Max processes: 10
    resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    language = data.get('language')
    code = data.get('code')
    stdin = data.get('stdin', '')
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        set_limits()
        
        if language == 'python':
            # Write code to file
            code_file = os.path.join(temp_dir, 'main.py')
            with open(code_file, 'w') as f:
                f.write(code)
            
            # Execute with timeout
            result = subprocess.run(
                ['python3', code_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=temp_dir,
                preexec_fn=set_limits
            )
            
            return jsonify({
                'stdout': result.stdout,
                'stderr': result.stderr,
                'code': result.returncode
            })
        
        # Add other languages...
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'stdout': '',
            'stderr': 'Execution timeout',
            'code': 124
        }), 200
    except Exception as e:
        return jsonify({
            'stdout': '',
            'stderr': str(e),
            'code': 1
        }), 200
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Security Limitations**:
- ⚠️ Not as secure as Piston (no container isolation)
- ⚠️ User code runs in same process space
- ⚠️ Potential for resource exhaustion
- ✅ Better than nothing (resource limits help)

---

### Phase 2: Container Pool Management

#### Option A: Pre-warmed Pool (Recommended)

**Azure Function** (`pool-manager`):
```python
import azure.functions as func
import requests
import os

# Pre-warmed container pool
POOL_SIZE = 10
CONTAINER_URL = os.environ['CONTAINER_APP_URL']

def get_available_container():
    # Check health of containers
    # Return URL of available container
    # If none available, scale up
    pass

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get execution request
    execution_request = req.get_json()
    
    # Get available container
    container_url = get_available_container()
    
    # Forward request to container
    response = requests.post(
        f"{container_url}/execute",
        json=execution_request,
        timeout=10
    )
    
    return func.HttpResponse(
        response.text,
        status_code=response.status_code
    )
```

**Pros**:
- ✅ Fast execution (~1-2 seconds)
- ✅ Containers pre-warmed
- ✅ Auto-scaling

**Cons**:
- ⚠️ Cost: Keep containers running
- ⚠️ Resource management needed

---

#### Option B: On-Demand Containers (Not Recommended)

**GitHub Actions Workflow**:
```yaml
name: Execute Code

on:
  workflow_dispatch:
    inputs:
      code:
        description: 'Code to execute'
        required: true
      language:
        description: 'Programming language'
        required: true

jobs:
  execute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy Container
        run: |
          terraform init
          terraform apply -auto-approve \
            -var="code=${{ github.event.inputs.code }}" \
            -var="language=${{ github.event.inputs.language }}"
      
      - name: Wait for Execution
        run: |
          # Poll for results
          sleep 30
      
      - name: Get Results
        run: |
          # Fetch execution results
          terraform output -json
```

**Problems**:
- ❌ **30-60 seconds latency** per execution
- ❌ GitHub Actions concurrency limits
- ❌ Not suitable for real-time use
- ❌ High cost (GitHub Actions minutes)

---

### Phase 3: Request Queue (Better than GitHub Actions)

**Azure Service Bus Queue**:
```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Backend sends to queue
def queue_execution(request):
    client = ServiceBusClient.from_connection_string(CONN_STR)
    with client:
        sender = client.get_queue_sender("execution-queue")
        message = ServiceBusMessage(json.dumps(request))
        sender.send_messages(message)

# Azure Function processes queue
def process_queue(message):
    # Get available container
    container = get_container_from_pool()
    
    # Execute
    result = execute_code(container, message)
    
    # Return result
    return result
```

**Pros**:
- ✅ Proper message queue
- ✅ High throughput
- ✅ Reliable
- ✅ Auto-scaling

---

## 🔒 Security Comparison

| Aspect | Session Pool (Current) | ACA Direct Execution | ACA + gVisor (Not Supported) |
|--------|------------------------|---------------------|------------------------------|
| **Isolation** | Hyper-V (hardware) | Container (OS-level) | User-space kernel |
| **Security Level** | 🟢 High | 🟡 Medium | 🟢 High |
| **Container Escape Risk** | ✅ Very Low | ⚠️ Medium | ✅ Low |
| **Resource Limits** | ✅ Enforced | ✅ Enforced | ✅ Enforced |
| **Network Isolation** | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 💰 Cost Comparison

### Current (Session Pool)
- **Idle**: $0/day (ready-sessions: 0)
- **Active**: ~$0.10-0.50/hour per session
- **200 users, 2 hours**: ~$10-15

### Proposed (ACA Only)
- **Pre-warmed Pool (10 containers)**: ~$2-3/day
- **Per execution**: ~$0.001-0.01
- **200 users, 2 hours**: ~$5-10 (if pool-based)
- **On-demand**: ~$20-30 (if creating containers per request)

---

## ✅ Final Recommendation

### **Option 1: Keep Session Pool (Recommended)**
- ✅ Best security (Hyper-V isolation)
- ✅ Fast execution
- ✅ Cost-effective
- ✅ Already working (just needs ingress fix)

**Action**: Fix ingress issue, continue using Session Pool

---

### **Option 2: ACA + Pre-warmed Pool + Direct Execution**
- ✅ No privileged mode needed
- ✅ Standard ACA features
- ⚠️ Less secure than Session Pool
- ⚠️ Requires custom execution engine

**Implementation**:
1. Replace Piston with direct language runtimes
2. Use Azure Functions for queue management
3. Maintain pre-warmed container pool
4. Implement resource limits and security measures

---

### **Option 3: Hybrid (Session Pool + ACA Fallback)**
- ✅ Best of both worlds
- ✅ Session Pool for security-critical code
- ✅ ACA for simple/trusted code
- ⚠️ More complex

---

## 📋 Proof of Concept Plan

### Step 1: Create Execution Container (1-2 days)
- [ ] Build Dockerfile with language runtimes
- [ ] Create execution service (Python/Node)
- [ ] Test basic code execution
- [ ] Implement resource limits

### Step 2: Deploy to ACA (1 day)
- [ ] Deploy container to ACA
- [ ] Test execution endpoint
- [ ] Verify resource limits work
- [ ] Test security measures

### Step 3: Create Pool Manager (2-3 days)
- [ ] Azure Function for queue management
- [ ] Container pool management logic
- [ ] Health checks
- [ ] Auto-scaling

### Step 4: Integration (2-3 days)
- [ ] Update backend to use new system
- [ ] Test end-to-end flow
- [ ] Load testing
- [ ] Security testing

### Step 5: Comparison Testing (1-2 days)
- [ ] Compare with Session Pool
- [ ] Performance benchmarks
- [ ] Cost analysis
- [ ] Security assessment

**Total**: ~7-11 days for POC

---

## 🎯 Decision Matrix

| Criteria | Session Pool | ACA Direct | ACA + Queue |
|----------|--------------|------------|-------------|
| **Security** | 🟢 High | 🟡 Medium | 🟡 Medium |
| **Speed** | 🟢 Fast (1-3s) | 🟢 Fast (1-2s) | 🟡 Medium (2-5s) |
| **Cost** | 🟢 Low | 🟡 Medium | 🟡 Medium |
| **Complexity** | 🟡 Medium | 🟢 Low | 🔴 High |
| **Scalability** | 🟢 High | 🟢 High | 🟢 High |
| **Privileged Mode** | ✅ Not needed | ✅ Not needed | ✅ Not needed |

---

## 📝 Conclusion

**Your senior's suggestion has merit BUT**:

1. ✅ **ACA-only is possible** (with direct execution, not Piston)
2. ⚠️ **GitHub Actions is NOT ideal** for request queuing (use Azure Service Bus)
3. ⚠️ **On-demand containers are too slow** (use pre-warmed pool)
4. ⚠️ **Security is reduced** (container-level vs hardware-level)

**Recommendation**: 
- **Short-term**: Fix Session Pool ingress issue (easiest)
- **Long-term**: Evaluate ACA + Direct Execution if Session Pool doesn't meet needs

---

**Next Steps**: 
1. Fix current Session Pool ingress issue
2. Create POC of ACA + Direct Execution
3. Compare both approaches
4. Make informed decision


