# Azure Container Apps Executor: Architecture, Cost & Load Handling

## 📋 Table of Contents
1. [Executor Architecture](#executor-architecture)
2. [Azure Container Apps Cost Analysis](#azure-container-apps-cost-analysis)
3. [Load Handling & Capacity](#load-handling--capacity)
4. [Cost Optimization Strategies](#cost-optimization-strategies)
5. [Real-World Scenarios](#real-world-scenarios)

---

## 🏗️ Executor Architecture

### Overview

The executor service runs on **Azure Container Apps (ACA)**, providing a scalable, serverless code execution platform for programming contests and coding challenges.

### Architecture Components

```
┌─────────────────────────────────────────────────────────┐
│              Azure Container Apps Environment            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │     Container App: ai-ta-ra-code-executor2       │   │
│  ├──────────────────────────────────────────────────┤   │
│  │                                                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │   │
│  │  │ Replica 1│  │ Replica 2│  │ Replica 3│  ...  │   │
│  │  │          │  │          │  │          │      │   │
│  │  │ Gunicorn │  │ Gunicorn │  │ Gunicorn │      │   │
│  │  │ 4 workers│  │ 4 workers│  │ 4 workers│      │   │
│  │  │ 2 threads│  │ 2 threads│  │ 2 threads│      │   │
│  │  │          │  │          │  │          │      │   │
│  │  │ 8 conc.  │  │ 8 conc.  │  │ 8 conc.  │      │   │
│  │  │ requests │  │ requests │  │ requests │      │   │
│  │  └──────────┘  └──────────┘  └──────────┘      │   │
│  │                                                   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Key Concepts

#### 1. Container App vs Replicas

- **1 Container App** = One service (e.g., `ai-ta-ra-code-executor2`)
- **Multiple Replicas** = Multiple containers running the same service
- **Each Replica** = One container that can handle multiple concurrent requests

#### 2. Request Handling

**Current Configuration:**
- **Server**: Gunicorn (production WSGI server)
- **Workers per Replica**: 4
- **Threads per Worker**: 2
- **Concurrent Capacity per Replica**: 4 workers × 2 threads = **8 concurrent requests**
- **Total Capacity (3 replicas)**: 3 × 8 = **24 concurrent requests**

**Before (Flask Dev Server):**
- ❌ Single-threaded
- ❌ Only 1 request per replica
- ❌ Requests hung when queue built up

**After (Gunicorn):**
- ✅ 8 concurrent requests per replica
- ✅ Production-grade queue handling
- ✅ No hanging issues
- ✅ 60-second timeout protection

#### 3. Execution Flow

```
User Request
    ↓
Azure Load Balancer
    ↓
Available Replica (e.g., Replica 2)
    ↓
Gunicorn Worker Thread
    ↓
Code Execution (isolated subprocess)
    ├── Temporary directory (/tmp/exec_*)
    ├── Resource limits (CPU, memory, processes)
    ├── Network isolation
    └── Code sanitization
    ↓
Result Returned
    ↓
Replica Ready for Next Request
```

#### 4. Container Reuse Model

**Important**: Containers are **REUSED**, NOT one per user.

- **Shared Pool**: Containers are shared across all requests
- **Load Balancing**: Requests distributed across available replicas
- **Auto-scaling**: Replicas scale up/down based on demand
- **Isolation**: Each execution runs in a separate subprocess with:
  - Isolated temporary directory
  - Resource limits (CPU, memory, processes)
  - Network isolation
  - Code sanitization

### Supported Languages

- **Python** (3.x)
- **Java** (17+)
- **C++** (GCC)
- **JavaScript** (Node.js)

### Security Features

1. **Code Sanitization**
   - Blocks dangerous imports (`os`, `subprocess`, `sys`)
   - Blocks `eval()`, `exec()`, `compile()`
   - Blocks file write operations
   - Blocks network operations

2. **Network Isolation**
   - Socket creation blocked during execution
   - No outbound HTTP/HTTPS requests
   - No DNS resolution

3. **Resource Limits**
   - CPU: 10 seconds max per execution
   - Memory: 256MB max per execution
   - Processes: 10 max per execution
   - File size: 10MB max
   - Execution timeout: 5-10 seconds

4. **Filesystem Sandboxing**
   - Temporary directories with restricted permissions (700)
   - Cleanup after execution
   - No access to host filesystem

5. **Rate Limiting**
   - 50 requests per minute per IP
   - Prevents abuse and DoS attacks

---

## 💰 Azure Container Apps Cost Analysis

### Pricing Model

Azure Container Apps uses **pay-per-use** pricing based on:
- **vCPU consumption**: Per vCPU-second
- **Memory consumption**: Per GiB-second
- **Container Apps Environment**: Fixed daily cost

### Current Pricing (East US 2)

| Resource | Unit | Cost |
|----------|------|------|
| **vCPU** | Per vCPU-second | $0.000012 |
| **Memory** | Per GiB-second | $0.0000015 |
| **Container Apps Environment** | Per day | $0.10 (fixed) |
| **ACR (Basic)** | Per month | ~$5 (storage) |

### Current Configuration

**Per Replica:**
- **CPU**: 2.0 cores (increased for Java support)
- **Memory**: 4.0 GiB (increased for Java support)
- **Min Replicas**: 1 (can scale to 0 when idle)
- **Max Replicas**: 100 (for contest capacity)

**Cost per Replica:**
```
vCPU:  2.0 × $0.000012 = $0.000024/second
Memory: 4.0 × $0.0000015 = $0.000006/second
─────────────────────────────────────────
Total:                    $0.00003/second
                          = $0.108/hour
                          = $2.592/day
```

### Cost Scenarios

#### Scenario 1: Idle (1 replica running 24/7)

```
1 replica × $0.00003/second × 86,400 seconds/day
= $2.592/day
= $77.76/month
```

#### Scenario 2: Scale to Zero (Idle)

```
min_replicas = 0
Cost when idle: $0/day
```

#### Scenario 3: Contest (200 students × 2 questions, 2 hours)

**Auto-scaling Configuration:**
- Pre-warmed: 10 replicas
- Peak: 50-100 replicas
- Average: 30-50 replicas

**Cost Calculation:**
```
Pre-warmed (10 replicas × 0.5 hours):
  10 × $0.108/hour × 0.5 = $0.54

Average (30 replicas × 1.5 hours):
  30 × $0.108/hour × 1.5 = $4.86

Peak (50 replicas × 0.5 hours):
  50 × $0.108/hour × 0.5 = $2.70
────────────────────────────────────
Total:                            $8.10
```

**Cost per Student**: $8.10 / 200 = **$0.0405 per student**

#### Scenario 4: Contest (250 students × 2 questions, 3.5 hours)

**Auto-scaling Configuration:**
- Pre-warmed: 10 replicas
- Peak: 50 replicas
- Average: 30 replicas

**Cost Calculation:**
```
Pre-warmed (10 replicas × 0.5 hours):
  10 × $0.108/hour × 0.5 = $0.54

Average (30 replicas × 2.5 hours):
  30 × $0.108/hour × 2.5 = $8.10

Peak (50 replicas × 0.5 hours):
  50 × $0.108/hour × 0.5 = $2.70
────────────────────────────────────
Total:                            $11.34
```

**Cost per Student**: $11.34 / 250 = **$0.045 per student**

### Monthly Cost Estimates

| Scenario | Monthly Cost | Notes |
|----------|-------------|-------|
| **Scale to Zero (Idle)** | $0 | No replicas when idle |
| **Always On (1 replica)** | $77.76 | 1 replica running 24/7 |
| **Contest Only (1 contest/month)** | $8-12 | Contest cost only |
| **Regular Usage (5 contests/month)** | $40-60 | 5 contests × $8-12 |

### Cost Comparison: Old vs New Configuration

| Configuration | CPU | Memory | Cost/Hour | Cost/Day |
|--------------|-----|--------|-----------|----------|
| **Old** | 1.0 | 2.0 GiB | $0.054 | $1.30 |
| **New** | 2.0 | 4.0 GiB | $0.108 | $2.59 |

**Why the increase?**
- Java support requires more memory (4 GiB minimum)
- Higher CPU allocation needed for 4 GiB memory
- **Result**: 2x cost per replica, but Java now works! ✅

---

## 📊 Load Handling & Capacity

### Capacity Per Replica

**Current Configuration:**
- **CPU**: 2.0 cores per replica
- **Memory**: 4.0 GiB per replica
- **Gunicorn**: 4 workers × 2 threads = 8 concurrent requests
- **Execution Time**: 500ms - 2 seconds (average)

**Concurrent Capacity:**
- **Per Replica**: 8 concurrent executions
- **With 3 Replicas**: 24 concurrent executions
- **With 10 Replicas**: 80 concurrent executions
- **With 30 Replicas**: 240 concurrent executions
- **With 50 Replicas**: 400 concurrent executions

### Load Scenarios

#### Scenario 1: 200 Students Contest

**Requirements:**
- 200 students × 2 questions = 400 executions
- Duration: 2 hours
- Peak: All students submit simultaneously

**Capacity Analysis:**
```
Peak concurrent: 400 executions
Required replicas: 400 / 8 = 50 replicas
Recommended: 50-80 replicas (with buffer)
```

**Auto-scaling Pattern:**
```
Contest Start (10:00 AM)
    ↓
10 replicas (pre-warmed)
    ↓
Students start submitting
    ↓
Auto-scales to 30 replicas (10:05 AM)
    ↓
Peak traffic (10:15 AM)
    ↓
Auto-scales to 50-80 replicas (10:15 AM)
    ↓
Traffic decreases (10:30 AM)
    ↓
Auto-scales down to 20 replicas (10:30 AM)
    ↓
Contest ends (12:00 PM)
    ↓
Auto-scales down to 0-10 replicas (12:00 PM)
```

**Result**: ✅ Handles 200 students smoothly

#### Scenario 2: 250 Students Contest

**Requirements:**
- 250 students × 2 questions = 500 executions
- Duration: 3.5 hours
- Peak: 50-100 concurrent requests

**Capacity Analysis:**
```
Peak concurrent: 100 executions
Required replicas: 100 / 8 = 12.5 → 15 replicas
Recommended: 30 replicas (with buffer)
```

**Result**: ✅ Handles 250 students smoothly

#### Scenario 3: 500 Students Contest

**Requirements:**
- 500 students × 2 questions = 1,000 executions
- Duration: 3 hours
- Peak: All students submit simultaneously

**Capacity Analysis:**
```
Peak concurrent: 1,000 executions
Required replicas: 1,000 / 8 = 125 replicas
```

**Azure Limit**: 300 replicas per Container App ✅

**Result**: ✅ Can handle 500 students (within Azure limits)

### Throughput Analysis

**Per Replica Throughput:**
- Execution time: 500ms - 2 seconds (average)
- Concurrent capacity: 8 executions
- Throughput: 8 executions / 2 seconds = **4 executions/second**
- Per minute: 4 × 60 = **240 executions/minute**

**Total Throughput (30 replicas):**
- 30 replicas × 240 executions/minute = **7,200 executions/minute**
- For 1,000 executions: 1,000 / 7,200 = **0.14 minutes (8.4 seconds)**

**Result**: ✅ Very high throughput capacity

### Bottleneck Analysis

#### CPU Bottleneck
- Each execution uses ~97% of 1 CPU core
- Each replica has 2 CPU cores
- **Per replica**: Can handle ~2 concurrent executions (CPU-limited)
- **With Gunicorn**: 8 concurrent (multiple workers share CPU)

#### Memory Bottleneck
- Each execution uses ~39 MB
- Each replica has 4 GiB = 4,096 MB
- **Per replica**: 4,096 / 39 = **~105 concurrent executions** (memory-limited)

**Verdict**: **CPU is the bottleneck** → Gunicorn workers help distribute load

### Auto-Scaling Configuration

**Recommended Terraform Configuration:**

```hcl
min_replicas = 5    # Pre-warmed pool for contest start
max_replicas = 100   # Scale up to handle burst traffic

# Auto-scaling rules
scaling {
  min_replicas = 5
  max_replicas = 100
  
  rules {
    name = "cpu-scaling"
    metric = "cpu"
    threshold = 70
    scale_direction = "increase"
  }
  
  rules {
    name = "memory-scaling"
    metric = "memory"
    threshold = 80
    scale_direction = "increase"
  }
}
```

**Scaling Behavior:**
- **Scale Up**: When CPU > 70% or Memory > 80%
- **Scale Down**: When CPU < 30% and Memory < 50% (after 5 minutes)
- **Scale Speed**: 1-2 replicas per minute

---

## 💡 Cost Optimization Strategies

### Strategy 1: Scale to Zero When Idle

**Configuration:**
```hcl
min_replicas = 0  # Scale to zero when no traffic
```

**Savings:**
- Idle cost: $0/day (vs $2.59/day for 1 replica)
- Monthly savings: $77.76/month

**Trade-off:**
- Cold start: 10-30 seconds when first request arrives
- **Recommendation**: Use for non-critical periods

### Strategy 2: Pre-warmed Pool

**Configuration:**
```hcl
min_replicas = 5   # Pre-warmed pool
max_replicas = 100 # Scale up during contest
```

**Cost:**
- Idle: 5 × $0.108/hour = $0.54/hour = $12.96/day
- Contest: Additional $3-8 per contest

**Benefits:**
- No cold start delay
- Ready for contest start
- Auto-scales during peak

### Strategy 3: Contest Day Scaling

**Before Contest:**
```hcl
min_replicas = 0  # No cost
```

**Contest Start (30 minutes before):**
```bash
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --min-replicas 10
```

**During Contest:**
- Auto-scales 20-50 replicas based on load

**After Contest:**
```bash
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --min-replicas 0
```

**Estimated Cost**: $8-12 per contest

### Strategy 4: Reserved Capacity (For Always-On)

**If running 24/7:**
- Azure Reserved Instances can save up to 30%
- **Monthly savings**: $77.76 × 0.30 = $23.33/month

**Recommendation**: Only if running 24/7 for extended periods

### Strategy 5: Monitor and Optimize

**Azure Cost Management:**
- Set up spending alerts
- Review usage reports monthly
- Optimize based on actual usage patterns

---

## 🎯 Real-World Scenarios

### Scenario 1: Small Contest (50 students)

**Requirements:**
- 50 students × 2 questions = 100 executions
- Duration: 1 hour

**Configuration:**
```hcl
min_replicas = 2
max_replicas = 20
```

**Cost:**
```
2 replicas × $0.108/hour × 1 hour = $0.216
```

**Result**: ✅ Very affordable ($0.216 per contest)

### Scenario 2: Medium Contest (200 students)

**Requirements:**
- 200 students × 2 questions = 400 executions
- Duration: 2 hours

**Configuration:**
```hcl
min_replicas = 10
max_replicas = 50
```

**Cost:**
```
Auto-scaling: ~$8-10 per contest
```

**Result**: ✅ Cost-effective ($0.04 per student)

### Scenario 3: Large Contest (500 students)

**Requirements:**
- 500 students × 2 questions = 1,000 executions
- Duration: 3 hours

**Configuration:**
```hcl
min_replicas = 15
max_replicas = 100
```

**Cost:**
```
Auto-scaling: ~$15-20 per contest
```

**Result**: ✅ Still affordable ($0.03-0.04 per student)

### Scenario 4: Multiple Contests Per Month

**Requirements:**
- 5 contests per month
- Average: 200 students per contest

**Configuration:**
```hcl
min_replicas = 0  # Scale to zero when idle
max_replicas = 50
```

**Cost:**
```
5 contests × $10 = $50/month
Idle: $0
─────────────────────────
Total: $50/month
```

**Result**: ✅ Very cost-effective

---

## 📈 Summary

### Executor Architecture
- ✅ **Gunicorn** production server (4 workers × 2 threads)
- ✅ **8 concurrent requests** per replica
- ✅ **Container reuse** model (efficient)
- ✅ **Auto-scaling** based on demand
- ✅ **Security** features (code sanitization, isolation)

### Cost Analysis
- ✅ **Pay-per-use** pricing model
- ✅ **$0.108/hour** per replica (2 CPU, 4 GiB)
- ✅ **$8-12 per contest** (200-250 students)
- ✅ **$0.03-0.05 per student** (very affordable)
- ✅ **Scale to zero** when idle ($0 cost)

### Load Handling
- ✅ **8 concurrent executions** per replica
- ✅ **240 executions/minute** per replica
- ✅ **Handles 500+ students** (within Azure limits)
- ✅ **Auto-scaling** handles traffic spikes
- ✅ **Low latency** (500ms - 2 seconds per execution)

### Recommendations

1. **For Contests:**
   - Use `min_replicas = 5-10` (pre-warmed)
   - Use `max_replicas = 50-100` (handle peak)
   - Estimated cost: $8-12 per contest

2. **For Idle Periods:**
   - Use `min_replicas = 0` (scale to zero)
   - Saves $77.76/month
   - Cold start: 10-30 seconds (acceptable)

3. **For Always-On:**
   - Use `min_replicas = 1-5` (minimal pre-warmed)
   - Cost: $2.59-12.96/day
   - No cold start delay

---

## ✅ Conclusion

The Azure Container Apps executor is:
- ✅ **Scalable**: Handles 500+ students
- ✅ **Cost-effective**: $0.03-0.05 per student
- ✅ **Reliable**: Production-grade Gunicorn server
- ✅ **Secure**: Multiple layers of protection
- ✅ **Flexible**: Auto-scaling based on demand

**Status**: ✅ **Production-ready and cost-optimized!**

