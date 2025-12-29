# ACA Code Executor - Deployment Guide

## 🎯 Overview

Simple, deployable solution for Azure Container Apps that executes user code for **100-500 users** (200-1,000 executions) with **minimal pre-warmed pool** (cost-optimized).

---

## 📋 Prerequisites

1. **Azure CLI** installed and logged in
2. **Docker** installed
3. **Terraform** installed (optional, can use Azure CLI)
4. **Azure Container Registry** (ACR) - already have `aitaraacr1763805702`
5. **Container Apps Environment** - already have `ai-ta-RA-env`

---

## 🚀 Quick Deployment (4 Steps)

### Step 0: Test Locally First (Recommended)

**Before deploying to Azure, test locally**:

```bash
cd aca-executor

# Install dependencies
pip install -r requirements.txt

# Run locally
python3 executor-service.py
```

**Test in another terminal**:
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [{"id": "test_1", "input": "", "expected_output": "42"}],
    "user_id": "test",
    "question_id": "test"
  }'
```

**See `LOCAL_TESTING.md` for detailed local testing guide.**

---

### Step 1: Build and Push Container Image

```bash
cd aca-executor

# Login to ACR
az acr login --name aitaraacr1763805702

# Build image
docker build -t aitaraacr1763805702.azurecr.io/executor-image:v1 .

# Push to ACR
docker push aitaraacr1763805702.azurecr.io/executor-image:v1
```

**Time**: ~5-10 minutes

---

### Step 2: Deploy with Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Review plan
terraform plan

# Deploy
terraform apply
```

**Time**: ~2-3 minutes

---

### Step 3: Update Backend

Update your backend to use the executor:

```python
# In backend/executor.py, add:
import os
EXECUTOR_URL = os.getenv(
    'EXECUTOR_URL',
    'https://code-executor.happypond-428960e8.eastus2.azurecontainerapps.io'
)

# Use the executor
def execute_code_in_session(request: ExecuteRequest):
    # ... use EXECUTOR_URL ...
```

**Time**: ~5 minutes

---

## 📊 Configuration

### Pre-Warmed Pool (Cost-Optimized)

**Default Configuration**:
- **Min Replicas**: 5 (minimal pre-warmed pool)
- **Max Replicas**: 1,000 (handles 500 users × 2 questions)

**Cost**:
- **Idle**: ~$2-5/day (5 containers)
- **Peak (500 users)**: ~$100-150 for 2-hour contest
- **Monthly (if always on)**: ~$60-150

### Adjust for Your Needs

**For 100 users (200 executions)**:
```hcl
min_replicas = 2
max_replicas = 200
```

**For 500 users (1,000 executions)**:
```hcl
min_replicas = 5
max_replicas = 1000
```

---

## 🧪 Testing

### Test Health Endpoint

```bash
# Get the URL from Terraform output or Azure Portal
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

**Expected**:
```json
{
  "status": "healthy",
  "service": "Code Execution Service",
  "replica": "code-executor-..."
}
```

### Test Code Execution

```bash
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "stdin": "",
    "timeout": 5
  }'
```

**Expected**:
```json
{
  "run": {
    "stdout": "42\n",
    "stderr": "",
    "code": 0
  },
  "language": "python"
}
```

---

## 🔧 Manual Deployment (Without Terraform)

If you prefer Azure CLI:

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name aitaraacr1763805702 --resource-group ai-ta-2 --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name aitaraacr1763805702 --resource-group ai-ta-2 --query passwords[0].value -o tsv)

# Create Container App
az containerapp create \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --environment ai-ta-RA-env \
  --image aitaraacr1763805702.azurecr.io/executor-image:v1 \
  --target-port 8000 \
  --ingress external \
  --min-replicas 5 \
  --max-replicas 1000 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --registry-server aitaraacr1763805702.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD
```

---

## 📈 Scaling

### Before Contest (Scale Up)

```bash
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 10 \
  --max-replicas 1000
```

### After Contest (Scale Down)

```bash
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 5 \
  --max-replicas 1000
```

### Cost Optimization (Idle)

```bash
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 0 \
  --max-replicas 1000
```

**Cost when idle**: $0 (scales to 0)

---

## 🔒 Security Features

1. **Resource Limits**:
   - CPU: 10 seconds max
   - Memory: 256MB max
   - Processes: 10 max
   - File size: 10MB max

2. **Non-Root User**: Container runs as non-root

3. **Isolated Execution**: Each request gets isolated execution

4. **Timeout Protection**: 5 seconds default timeout

---

## 📊 Performance

### Expected Performance

- **Pre-warmed requests**: 1-3 seconds
- **Cold start requests**: 5-10 seconds (auto-scaling)
- **Concurrent capacity**: 1,000 executions

### For 500 Users (1,000 executions)

- **First 5 requests**: Instant (pre-warmed)
- **Next 995 requests**: 5-10 seconds (auto-scaling)
- **Total time**: ~10-15 minutes (if all submit simultaneously)
- **Better**: Stagger submissions (realistic scenario)

---

## 💰 Cost Breakdown

### Monthly Cost (Always On)

- **5 pre-warmed containers**: ~$2-5/day = $60-150/month
- **Peak scaling**: Pay-per-use during contests

### Per Contest (2 hours, 500 users)

- **Pre-warmed (5)**: ~$0.50
- **Auto-scaled (up to 1,000)**: ~$50-100
- **Total**: ~$50-100 per contest

### Cost Optimization

**Idle (min-replicas=0)**:
- Cost: $0/day
- First request: 5-10 seconds (cold start)

**Minimal (min-replicas=2)**:
- Cost: ~$1-2/day
- First requests: Instant

**Recommended (min-replicas=5)**:
- Cost: ~$2-5/day
- First requests: Instant
- Good balance

---

## 🐛 Troubleshooting

### Container Not Starting

```bash
# Check logs
az containerapp logs show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --follow
```

### Health Check Failing

```bash
# Check health endpoint
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

### Execution Errors

Check executor logs:
```bash
az containerapp logs show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --follow
```

---

## ✅ Verification Checklist

- [ ] Container image built and pushed to ACR
- [ ] Container App created and running
- [ ] Health endpoint returns 200
- [ ] Code execution works (test with Python)
- [ ] Backend updated to use executor URL
- [ ] Scaling configured (min/max replicas)
- [ ] Cost monitoring set up

---

## 📋 Next Steps

1. **Deploy**: Follow steps above
2. **Test**: Run test cases
3. **Monitor**: Check logs and metrics
4. **Optimize**: Adjust min-replicas based on usage
5. **Scale**: Adjust max-replicas for capacity

---

**Status**: Ready to deploy! ✅

