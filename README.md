# FastAPI Code Execution Service - Complete Guide

## 🎯 Overview

This is a **production-ready FastAPI-based code execution service** deployed on Azure Container Apps. It executes user-submitted code in 5 languages (Python, JavaScript, Java, C++, C#) with security guardrails, test case validation, and database integration.

---

## 🏗️ Architecture

### **Components**

1. **FastAPI Application** (`executor-service-fastapi.py`)
   - Main service handling code execution
   - 3 endpoints: `/run`, `/runall`, `/submit`
   - Security: Code sanitization, resource limits, network isolation

2. **Gunicorn + Uvicorn Workers** (Production Server)
   - 4 workers × 2 threads = **8 concurrent requests per replica**
   - Queue system with backlog of 200 requests
   - Auto-scales based on load

3. **Azure Container Apps** (Deployment Platform)
   - Auto-scaling: 1-3 replicas (configurable)
   - Resources: 2 vCPU, 4GB RAM per replica
   - Health checks and monitoring

4. **PostgreSQL Database** (Azure)
   - Stores submission results via `/submit` endpoint
   - Lazy connection pooling (only connects when needed)

---

## 📊 How It Works

### **Request Flow**

```
User → Frontend → FastAPI Service → Code Execution → Results → Database
                                      ↓
                              Security Sandbox
                              (Isolated execution)
```

### **Endpoints**

#### 1. `/run` - Single Test Case Execution
- **Purpose**: Test code with one sample test case
- **Rate Limit**: 50 requests/minute
- **Use Case**: Quick code testing during development
- **Response**: Immediate result for one test case

#### 2. `/runall` - All Test Cases Execution
- **Purpose**: Run code against all test cases (except sample)
- **Rate Limit**: 1000 requests/minute
- **Use Case**: Full validation before submission
- **Response**: Results for all test cases sequentially

#### 3. `/submit` - Final Submission
- **Purpose**: Submit final code and save to database
- **Rate Limit**: 200 requests/minute
- **Use Case**: Final submission for grading
- **Response**: Saved submission with all test results

### **Execution Process**

1. **Code Sanitization**: Blocks dangerous patterns (file I/O, network, system calls)
2. **Sandbox Creation**: Isolated temporary directory
3. **Resource Limits Applied**:
   - CPU: 10 seconds max
   - Memory: 1GB max
   - Execution Timeout: 5 seconds per test case
4. **Code Execution**: Language-specific compilation/interpretation
5. **Output Comparison**: Compare actual vs expected output
6. **Result Collection**: CPU, memory, execution time metrics
7. **Cleanup**: Remove sandbox files

---

## 💪 Capacity Analysis: 200 Users, 3 Hours, 2 DSA Questions

### **Scenario Breakdown**

- **Total Users**: 200
- **Questions per User**: 2
- **Total Submissions**: 400 (200 × 2)
- **Duration**: 3 hours (180 minutes)
- **Average Submission Rate**: ~2.2 submissions/minute
- **Peak Submission Rate**: ~10-20 submissions/minute (during contest start/end)

### **Current Configuration**

#### **Per Replica Capacity**
- **Workers**: 4 Gunicorn workers
- **Threads per Worker**: 2
- **Concurrent Requests**: **8 per replica**
- **Queue Backlog**: 200 requests

#### **Total System Capacity** (3 replicas max)
- **Concurrent Capacity**: 3 × 8 = **24 concurrent requests**
- **Queue Capacity**: 200 requests (handled sequentially)
- **Peak Throughput**: ~288 submissions/minute (theoretical max)

### **Execution Time Analysis**

**Per Submission** (assuming 20 test cases per question):
- Test case execution: ~2-3 seconds each
- Sequential execution: 20 × 2.5s = **~50 seconds per submission**
- With queue: Additional wait time if all replicas busy

**Peak Load Scenario**:
- 20 simultaneous submissions
- 20 ÷ 24 = **~83% capacity utilization**
- Average wait time: **< 1 minute** (if queue is empty)
- With queue backlog: **< 2 minutes** (worst case)

### **✅ Capacity Assessment**

**For 200 Users × 2 Questions:**

| Metric | Value | Status |
|--------|-------|--------|
| Total Submissions | 400 | ✅ |
| Peak Concurrent | 20 | ✅ (24 capacity) |
| Average Rate | 2.2/min | ✅ |
| Peak Rate | 20/min | ✅ (288/min capacity) |
| Queue Backlog | 200 | ✅ |
| Wait Time (avg) | < 1 min | ✅ |
| Wait Time (peak) | < 2 min | ✅ |

### **Recommendations**

#### **Current Setup (1-3 Replicas)**
- ✅ **Sufficient for 200 users** with current load distribution
- ✅ **Queue system handles bursts** gracefully
- ⚠️ **Consider increasing max_replicas to 5** for better peak handling

#### **Optimization Options**

1. **Increase Max Replicas** (in `terraform/variables.tf`):
   ```hcl
   max_replicas = 5  # Instead of 3
   ```
   - Capacity: 5 × 8 = 40 concurrent
   - Better peak handling

2. **Increase Workers** (in `Dockerfile.fastapi`):
   ```dockerfile
   --workers 6  # Instead of 4
   ```
   - Capacity: 6 × 2 = 12 per replica
   - Total: 5 × 12 = 60 concurrent

3. **Optimize Test Case Execution**:
   - Current: Sequential (20 test cases × 2.5s = 50s)
   - Could parallelize: 20 test cases ÷ 4 = 5 batches = ~12.5s
   - **Note**: Parallel execution was tested but reverted due to thread-safety issues

---

## 🔒 Security Features

1. **Code Sanitization**: Blocks dangerous imports and functions
2. **Resource Limits**: CPU (10s), Memory (1GB), Timeout (5s)
3. **Network Isolation**: Blocks all network access during execution
4. **Filesystem Sandbox**: Temporary isolated directories
5. **Process Isolation**: Subprocess execution with limits
6. **Rate Limiting**: Prevents abuse (50-1000 req/min per endpoint)
7. **Non-Root User**: Runs as `executor` user (uid 1000)

---

## 📦 Deployment Files

```
.
├── executor-service-fastapi.py    # Main FastAPI service
├── Dockerfile.fastapi             # Container build file
├── requirements-fastapi.txt       # Python dependencies
├── terraform/
│   ├── main.tf                    # Container App configuration
│   ├── variables.tf               # Variable definitions
│   ├── postgresql.tf              # PostgreSQL setup (optional)
│   └── postgresql-variables.tf    # DB variables
└── README.md                       # This file
```

---

## 🚀 Quick Deployment

### **Prerequisites**
- Azure CLI installed and logged in
- Docker installed
- Terraform installed (optional)

### **Steps**

1. **Build and Push Docker Image**:
   ```bash
   az acr login --name aitaraacr1763805702
   docker build -f Dockerfile.fastapi -t aitaraacr1763805702.azurecr.io/executor-fastapi:v1 .
   docker push aitaraacr1763805702.azurecr.io/executor-fastapi:v1
   ```

2. **Update Terraform Variables** (if needed):
   ```bash
   cd terraform
   # Edit terraform.tfvars or set via command line
   ```

3. **Deploy with Terraform**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Get Service URL**:
   ```bash
   terraform output container_app_url
   ```

---

## 🧪 Testing

### **Local Testing**

```bash
# Install dependencies
pip install -r requirements-fastapi.txt

# Run service
uvicorn executor-service-fastapi:app --reload --port 8000

# Test endpoint
curl http://localhost:8000/health
```

### **Test Execution**

```bash
curl -X POST http://localhost:8000/runall \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "boilerplate": "",
    "test_cases": [
      {"id": "test_1", "input": "", "expected_output": "42"}
    ]
  }'
```

---

## 📈 Monitoring

### **Key Metrics to Monitor**

1. **Replica Count**: Should scale 1-3 (or 1-5 if optimized)
2. **Request Rate**: Should stay below 288/min per replica
3. **Queue Length**: Should stay below 200
4. **Error Rate**: Should be < 1%
5. **Average Response Time**: Should be < 60 seconds

### **Azure Container Apps Logs**

```bash
az containerapp logs show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --follow
```

---

## ⚙️ Configuration

### **Resource Limits** (in `executor-service-fastapi.py`)

```python
MAX_CPU_TIME = 10        # seconds
MAX_MEMORY = 1024 * 1024 * 1024  # 1GB
EXECUTION_TIMEOUT = 5   # seconds per test case
```

### **Gunicorn Workers** (in `Dockerfile.fastapi`)

```dockerfile
--workers 4              # Number of worker processes
--threads 2              # Threads per worker
--backlog 200            # Queue size
--timeout 300            # Request timeout (5 minutes)
```

### **Auto-Scaling** (in `terraform/main.tf`)

```hcl
min_replicas = 1         # Minimum containers (cost optimization)
max_replicas = 3         # Maximum containers (increase for higher load)
```

---

## 🎓 Supported Languages

1. **Python 3.11**: Direct execution
2. **JavaScript (Node.js 16)**: Node.js runtime
3. **Java**: OpenJDK (HotSpot JVM)
4. **C++**: GCC compiler
5. **C#**: Mono compiler (mono-mcs)

---

## 📝 API Request/Response Format

### **Request** (`/runall`)

```json
{
  "language": "python",
  "code": "def solve(n):\n    return n * 2",
  "boilerplate": "",
  "test_cases": [
    {
      "id": "test_1",
      "input": "5",
      "expected_output": "10"
    }
  ]
}
```

### **Response**

```json
{
  "success": true,
  "test_results": [
    {
      "test_case_id": "test_1",
      "status": "passed",
      "passed": true,
      "execution_time_ms": 45,
      "cpu_usage_percent": 12.5,
      "memory_usage_bytes": 1024000
    }
  ],
  "summary": {
    "total_tests": 1,
    "passed": 1,
    "failed": 0,
    "total_execution_time_ms": 45
  }
}
```

---

## ✅ Final Verdict: Can It Handle 200 Users?

### **YES, with Current Configuration**

**Reasons:**
1. ✅ **Capacity**: 24 concurrent (3 replicas × 8) > 20 peak concurrent
2. ✅ **Queue System**: 200 request backlog handles bursts
3. ✅ **Rate Limits**: 1000/min for `/runall` > 20/min peak
4. ✅ **Auto-Scaling**: Replicas scale 1-3 based on load
5. ✅ **Execution Time**: ~50s per submission is acceptable

### **Recommendations for Production**

1. **Increase `max_replicas` to 5** for better peak handling
2. **Monitor queue length** during contest
3. **Set up alerts** for high error rates or long wait times
4. **Consider pre-warming** 2 replicas before contest starts

---

## 🆘 Troubleshooting

### **High Wait Times**
- Increase `max_replicas` in Terraform
- Check queue length in logs
- Verify auto-scaling is working

### **Out of Memory Errors**
- Reduce `MAX_MEMORY` if needed
- Increase container memory in Terraform
- Check for memory leaks in code

### **Rate Limit Errors**
- Increase rate limits in `executor-service-fastapi.py`
- Check if single user is making too many requests

---

## 📚 Additional Resources

- **Azure Container Apps Docs**: https://docs.microsoft.com/azure/container-apps/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Gunicorn Docs**: https://docs.gunicorn.org/

---

## 📞 Support

For issues or questions:
1. Check Azure Container Apps logs
2. Review executor service logs
3. Verify Terraform configuration
4. Check database connectivity (if using `/submit`)

---

**Last Updated**: December 2024  
**Version**: 3.0.0 (FastAPI)  
**Status**: ✅ Production Ready
