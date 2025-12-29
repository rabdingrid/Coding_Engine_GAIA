# Terraform Pre-Warmed Container Pool Approach

## 🎯 Your Senior's Suggestion - Clarified

**The Idea**: Use Terraform to manage a **pre-warmed pool of ACA containers** that are already running with packages installed. When a request comes in, just **activate/route to an existing container** instead of creating a new one.

This is actually **much better** than what I initially analyzed!

---

## ✅ How This Works

### Architecture

```
User Request
    ↓
Backend (ACA) - Port 8000
    ↓
GitHub Actions (or Azure Function) - Request Router
    ↓
Terraform (or Azure API) - Scale/Activate Container
    ↓
Pre-warmed ACA Container Pool (already running)
    ↓
Container executes code (Python/Node already installed)
    ↓
Return result
```

### Key Difference from Previous Analysis

**Previous (Wrong)**: Create new container per request ❌  
**This (Correct)**: Use existing pre-warmed containers ✅

---

## 📋 Implementation Plan

### Step 1: Create Pre-Warmed Container Pool

**Terraform Configuration** (`main.tf`):

```hcl
resource "azurerm_container_app" "code_executor_pool" {
  name                         = "code-executor-pool"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    min_replicas = 5  # ← Pre-warmed: 5 containers always running
    max_replicas = 50  # ← Can scale up to 50 during peak

    container {
      name   = "executor"
      image  = "your-acr.azurecr.io/executor-image:v1"
      cpu    = 0.5
      memory = "1.0Gi"
      
      env {
        name  = "PORT"
        value = "8000"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "http"
  }

  scale {
    min_replicas = 5   # ← Always keep 5 warm
    max_replicas = 50
  }
}
```

**What This Does**:
- ✅ Creates 5 containers that are **always running** (pre-warmed)
- ✅ Containers have Python/Node already installed
- ✅ Can scale up to 50 containers during peak traffic
- ✅ No privileged mode needed (just regular containers)

---

### Step 2: Container Image (Simple Execution Service)

**Dockerfile** (`Dockerfile.executor`):

```dockerfile
FROM python:3.11-slim

# Install Node.js and other runtimes
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy execution service
COPY executor-service.py /app/executor-service.py
WORKDIR /app

# Run as non-root (ACA requirement)
RUN useradd -m executor && chown -R executor:executor /app
USER executor

EXPOSE 8000
CMD ["python", "executor-service.py"]
```

**executor-service.py** (Simple version):

```python
from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    language = data.get('language')
    code = data.get('code')
    stdin = data.get('stdin', '')
    
    if language == 'python':
        # Execute Python code
        result = subprocess.run(
            ['python3', '-c', code],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'code': result.returncode
        })
    
    # Add other languages...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Key Points**:
- ✅ No Piston needed
- ✅ No privileged mode
- ✅ Simple Python/Node execution
- ✅ Works in regular ACA containers

---

### Step 3: Request Routing (GitHub Actions or Azure Function)

#### Option A: GitHub Actions (Simple but Limited)

**`.github/workflows/route-request.yml`**:

```yaml
name: Route Code Execution Request

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
  route:
    runs-on: ubuntu-latest
    steps:
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Get Container URL
        id: get-url
        run: |
          URL=$(az containerapp show \
            --name code-executor-pool \
            --resource-group ai-ta-2 \
            --query "properties.configuration.ingress.fqdn" \
            -o tsv)
          echo "url=$URL" >> $GITHUB_OUTPUT
      
      - name: Execute Code
        run: |
          curl -X POST "https://${{ steps.get-url.outputs.url }}/execute" \
            -H "Content-Type: application/json" \
            -d '{
              "language": "${{ github.event.inputs.language }}",
              "code": "${{ github.event.inputs.code }}"
            }'
```

**Limitations**:
- ⚠️ GitHub Actions concurrency limits (20-180 jobs)
- ⚠️ Not ideal for high-volume traffic
- ✅ Simple to implement

---

#### Option B: Azure Function (Better for Production)

**`function_app.py`**:

```python
import azure.functions as func
import requests
import json
import os

# Container pool URL (pre-warmed containers)
CONTAINER_POOL_URL = os.environ['CONTAINER_POOL_URL']

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get execution request
        execution_request = req.get_json()
        
        # Route to pre-warmed container
        response = requests.post(
            f"{CONTAINER_POOL_URL}/execute",
            json=execution_request,
            timeout=10
        )
        
        return func.HttpResponse(
            response.text,
            status_code=response.status_code,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
```

**Pros**:
- ✅ High throughput (no concurrency limits)
- ✅ Fast (just HTTP routing)
- ✅ Auto-scaling
- ✅ Cost-effective

---

#### Option C: Direct Backend Routing (Simplest)

**Backend just routes to container pool**:

```python
# backend/executor.py
import requests
import os

CONTAINER_POOL_URL = os.environ.get(
    'CONTAINER_POOL_URL',
    'https://code-executor-pool.happypond-428960e8.eastus2.azurecontainerapps.io'
)

def execute_code_in_pool(request: ExecuteRequest) -> ExecuteResponse:
    """Route to pre-warmed container pool"""
    
    payload = {
        'language': request.language,
        'code': request.files[0].content if request.files else '',
        'stdin': request.stdin or ''
    }
    
    response = requests.post(
        f"{CONTAINER_POOL_URL}/execute",
        json=payload,
        timeout=10
    )
    
    result = response.json()
    
    return ExecuteResponse(
        run={
            'stdout': result.get('stdout', ''),
            'stderr': result.get('stderr', ''),
            'code': result.get('code', 0)
        },
        language=request.language,
        version=request.version
    )
```

**This is the simplest!** No GitHub Actions, no Terraform per request - just HTTP routing.

---

### Step 4: Terraform for Scaling (Optional)

**Terraform can scale the pool before contests**:

```hcl
# Scale up before contest
resource "azurerm_container_app" "code_executor_pool" {
  # ... existing config ...
  
  template {
    min_replicas = 20  # ← Scale up to 20 before contest
    max_replicas = 50
  }
}
```

**Or use Azure CLI**:

```bash
# Before contest
az containerapp update \
  --name code-executor-pool \
  --resource-group ai-ta-2 \
  --min-replicas 20 \
  --max-replicas 50

# After contest
az containerapp update \
  --name code-executor-pool \
  --resource-group ai-ta-2 \
  --min-replicas 5 \
  --max-replicas 50
```

---

## 📊 Comparison: This Approach vs Session Pool

| Aspect | Session Pool | ACA Pre-Warmed Pool |
|--------|--------------|---------------------|
| **Pre-warmed Containers** | ✅ Yes (ready-sessions) | ✅ Yes (min-replicas) |
| **Privileged Mode** | ✅ Not needed | ✅ Not needed |
| **Security** | 🟢 Hyper-V isolation | 🟡 Container isolation |
| **Speed** | 🟢 1-3 seconds | 🟢 1-2 seconds |
| **Cost (Idle)** | 🟢 $0 (ready-sessions: 0) | 🟡 ~$2-5/day (5 replicas) |
| **Cost (Active)** | 🟢 Pay-per-use | 🟡 Pay-per-replica |
| **Setup Complexity** | 🟡 Medium | 🟢 Low |
| **Terraform Support** | ⚠️ Limited | ✅ Full support |
| **Standard ACA Features** | ⚠️ Preview feature | ✅ Standard |

---

## ✅ Advantages of This Approach

1. **No Privileged Mode** ✅
   - Regular ACA containers
   - No Piston needed
   - Simple execution service

2. **Pre-Warmed Pool** ✅
   - Containers already running
   - Fast execution (1-2 seconds)
   - No cold start delay

3. **Terraform Support** ✅
   - Full Infrastructure as Code
   - Easy to manage
   - Version controlled

4. **Standard ACA** ✅
   - Not a preview feature
   - Full documentation
   - Better tooling support

5. **Simple Architecture** ✅
   - Just HTTP routing
   - No complex orchestration
   - Easy to understand

---

## ⚠️ Considerations

### Cost

**Pre-warmed Pool (5 replicas)**:
- 5 containers × 0.5 CPU × 1GB memory
- Cost: ~$2-5/day when idle
- vs Session Pool: $0/day when idle (ready-sessions: 0)

**During Contest (20 replicas)**:
- 20 containers × 0.5 CPU × 1GB memory
- Cost: ~$8-12/day
- vs Session Pool: ~$10-15 for 2-hour contest

### Security

**Container Isolation**:
- Less secure than Session Pool (Hyper-V)
- Still acceptable for most use cases
- Can add additional security measures

### Scaling

**Auto-scaling**:
- ACA can auto-scale based on HTTP traffic
- Can set min/max replicas
- Similar to Session Pool scaling

---

## 🎯 Implementation Steps

### Phase 1: Create Container Image (1 day)
1. Build Dockerfile with execution service
2. Push to ACR
3. Test locally

### Phase 2: Deploy with Terraform (1 day)
1. Create Terraform config
2. Deploy container app with min-replicas=5
3. Test execution endpoint

### Phase 3: Update Backend (1 day)
1. Update backend to route to container pool
2. Test end-to-end
3. Verify performance

### Phase 4: Optimization (1 day)
1. Fine-tune scaling rules
2. Add monitoring
3. Cost optimization

**Total**: ~4 days (much faster than previous estimate!)

---

## 💡 Recommendation

**This approach is MUCH better** than what I initially analyzed!

**Pros**:
- ✅ No privileged mode needed
- ✅ Pre-warmed containers (fast)
- ✅ Simple architecture
- ✅ Full Terraform support
- ✅ Standard ACA features

**Cons**:
- ⚠️ Higher idle cost ($2-5/day vs $0)
- ⚠️ Less secure than Session Pool (but acceptable)

**Decision**:
- If you want **standard ACA** and **Terraform**: Use this approach ✅
- If you want **maximum security** and **lowest cost**: Keep Session Pool ✅

---

## 📋 Next Steps

1. **Create container image** with execution service
2. **Deploy with Terraform** (min-replicas=5)
3. **Update backend** to route to pool
4. **Test and compare** with Session Pool
5. **Decide** based on requirements

---

**Status**: This approach is **feasible and much simpler** than initially thought! ✅


