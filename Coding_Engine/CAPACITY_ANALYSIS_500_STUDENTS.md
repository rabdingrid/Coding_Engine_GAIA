# Capacity Analysis: 500 Students × 2 Questions = 1000 Executions

## 🎯 Scenario

- **Students**: 500
- **Questions per student**: 2
- **Total executions**: 1,000
- **Timeline**: Contest duration (typically 2-3 hours)
- **Peak concurrency**: All students submitting simultaneously

---

## 📊 Azure Container Apps (ACA) - Pre-Warmed Pool

### Scaling Limits

**Key Constraint**: **30 replicas maximum per Container App** ⚠️

This is a **hard limit** in Azure Container Apps.

### Capacity Calculation

**Assumptions**:
- Each execution takes: **3-5 seconds** (average)
- Each replica can handle: **1 execution at a time** (sequential)
- Peak scenario: All 500 students submit at once

**Single Container App (30 replicas max)**:
```
30 replicas × (60 seconds / 5 seconds per execution) = 360 executions/minute
30 replicas × (60 seconds / 3 seconds per execution) = 600 executions/minute

For 1,000 executions:
- At 5 seconds/execution: 1,000 / 360 = 2.8 minutes
- At 3 seconds/execution: 1,000 / 600 = 1.7 minutes
```

**Problem**: If all 1,000 executions arrive simultaneously:
- **30 replicas can only handle 30 concurrent executions**
- **970 executions must wait in queue**
- **Queue time**: 970 / 30 = ~32 batches × 5 seconds = **~160 seconds (2.7 minutes)**

### Solution: Multiple Container Apps

**To handle 1,000 concurrent executions**, you need:

```
1,000 concurrent executions / 30 replicas per app = 34 container apps
```

**Architecture**:
```
┌─────────────────────────────────────────┐
│  Load Balancer / Backend Router        │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│ App 1 │  │ App 2 │  │ App 3 │  ... (34 apps)
│ 30 rep│  │ 30 rep│  │ 30 rep│
└───────┘  └───────┘  └───────┘
```

**Total Capacity**:
- 34 apps × 30 replicas = **1,020 concurrent executions** ✅
- Can handle 1,000 executions simultaneously

---

## 📊 Session Pool - Capacity

### Scaling Limits

**Key Advantage**: **No hard limit on max-sessions** ✅

Session Pool can scale to **hundreds or thousands** of sessions.

### Capacity Calculation

**Configuration for 500 students**:
```bash
az containerapp sessionpool update \
  --name ai-ta-RA-session-pool \
  --max-sessions 1000 \
  --ready-sessions 50
```

**Capacity**:
- **Max sessions**: 1,000 (can handle all 1,000 concurrent executions)
- **Ready sessions**: 50 (instant start for first 50)
- **On-demand**: 950 (allocated as needed, 3-5 second cold start)

**Performance**:
- First 50 executions: **Instant** (0.1 seconds)
- Next 950 executions: **3-5 seconds** (cold start)
- Total time to handle all: **~5-10 seconds** (vs 2.7 minutes for ACA)

---

## 💰 Cost Comparison

### ACA Pre-Warmed Pool (34 Apps)

**Pre-warmed (idle)**:
- 34 apps × 5 min-replicas × 0.5 CPU × 1GB = **170 replicas**
- Cost: ~$68-85/day when idle
- **Monthly**: ~$2,040-2,550

**During Contest (2 hours)**:
- 34 apps × 30 max-replicas = **1,020 replicas**
- Cost: ~$408-510 for 2 hours
- **Per contest**: ~$400-500

**Total (idle + contest)**:
- Monthly idle: $2,040-2,550
- Per contest: $400-500
- **Annual (12 contests)**: ~$6,480-8,100

### Session Pool

**Pre-warmed (idle)**:
- 0 ready-sessions = **$0/day**
- Monthly: **$0**

**During Contest (2 hours)**:
- 1,000 max-sessions (50 ready + 950 on-demand)
- Cost: ~$50-100 for 2 hours
- **Per contest**: ~$50-100

**Total (idle + contest)**:
- Monthly idle: **$0**
- Per contest: $50-100
- **Annual (12 contests)**: ~$600-1,200

---

## ⚡ Performance Comparison

### Scenario: 500 Students Submit Simultaneously

| Metric | ACA (34 Apps) | Session Pool |
|--------|---------------|-------------|
| **Max Concurrent** | 1,020 executions | 1,000 executions |
| **First 50 Executions** | 0.1-2 seconds | 0.1 seconds |
| **All 1,000 Executions** | 2.7-5 minutes | 5-10 seconds |
| **Queue Time** | High (if simultaneous) | Low (fast allocation) |
| **Cold Start** | Minimal (pre-warmed) | 3-5 seconds (on-demand) |

---

## 🎯 Feasibility Analysis

### ACA Pre-Warmed Pool

**Pros**:
- ✅ Standard ACA features
- ✅ Full Terraform support
- ✅ Predictable performance (pre-warmed)

**Cons**:
- ❌ **30 replica limit** (requires 34 apps)
- ❌ **High idle cost** ($2,040-2,550/month)
- ❌ **Complex architecture** (34 apps to manage)
- ❌ **Load balancing complexity** (routing to 34 apps)
- ❌ **Terraform complexity** (managing 34 resources)

**Feasibility**: ⚠️ **Possible but complex and expensive**

### Session Pool

**Pros**:
- ✅ **No replica limit** (can scale to 1,000+)
- ✅ **Low idle cost** ($0/day)
- ✅ **Simple architecture** (single pool)
- ✅ **Fast allocation** (3-5 seconds)
- ✅ **Better security** (Hyper-V isolation)

**Cons**:
- ⚠️ Preview feature
- ⚠️ Limited Terraform support
- ⚠️ Ingress configuration complexity

**Feasibility**: ✅ **Feasible and cost-effective**

---

## 📋 Implementation Complexity

### ACA Pre-Warmed Pool (34 Apps)

**Setup Steps**:
1. Create 34 Container Apps (Terraform loop)
2. Set up load balancer/routing logic
3. Configure scaling for each app
4. Test load distribution
5. Monitor 34 separate resources

**Terraform Complexity**:
```hcl
# Need to create 34 resources
resource "azurerm_container_app" "executor_pool" {
  count = 34  # ← 34 apps!
  
  name = "code-executor-pool-${count.index}"
  # ... configuration ...
}
```

**Backend Complexity**:
```python
# Need to route to 34 different URLs
POOL_URLS = [
    "https://code-executor-pool-0.azurecontainerapps.io",
    "https://code-executor-pool-1.azurecontainerapps.io",
    # ... 32 more ...
]

def route_request():
    # Round-robin or load-based routing
    url = select_pool_url()  # Complex logic needed
    return requests.post(f"{url}/execute", ...)
```

**Estimated Time**: **2-3 weeks**

### Session Pool

**Setup Steps**:
1. Create single Session Pool
2. Configure max-sessions=1000
3. Update backend to use pool endpoint
4. Test scaling

**Terraform Complexity**:
```hcl
# Single resource
resource "azurerm_container_app_session_pool" "main" {
  name = "code-executor-pool"
  max_sessions = 1000
  # ... configuration ...
}
```

**Backend Complexity**:
```python
# Single endpoint
POOL_URL = "https://session-pool.azurecontainerapps.io"

def execute_code():
    return requests.post(f"{POOL_URL}/python/execute", ...)
```

**Estimated Time**: **1-2 days** (if ingress is fixed)

---

## 🎯 Recommendation for 500 Students

### Option 1: Session Pool (Recommended) ✅

**Why**:
- ✅ Handles 1,000 concurrent executions easily
- ✅ Low cost ($0 idle, $50-100 per contest)
- ✅ Simple architecture (single pool)
- ✅ Fast allocation (5-10 seconds for all)
- ✅ Better security (Hyper-V)

**Configuration**:
```bash
az containerapp sessionpool update \
  --name ai-ta-RA-session-pool \
  --max-sessions 1000 \
  --ready-sessions 50 \
  --cooldown-period 300
```

**Cost**: ~$50-100 per contest

---

### Option 2: ACA Pre-Warmed Pool (If Terraform is Required)

**Why**:
- ✅ Full Terraform support
- ✅ Standard ACA features
- ⚠️ Requires 34 container apps
- ⚠️ High idle cost ($2,040-2,550/month)
- ⚠️ Complex architecture

**Configuration**:
- 34 Container Apps
- Each with 30 max-replicas
- Load balancer for routing

**Cost**: ~$400-500 per contest + $2,040-2,550/month idle

---

### Option 3: Hybrid Approach

**Use Session Pool for execution, Terraform for infrastructure**:

1. **Session Pool**: Handle code execution (best for this)
2. **Terraform**: Manage Session Pool lifecycle
3. **Best of both worlds**: Low cost + Infrastructure as Code

**Configuration**:
```hcl
resource "azurerm_container_app_session_pool" "main" {
  name = "code-executor-pool"
  max_sessions = 1000
  ready_sessions = 50
  # ... other config ...
}
```

**Cost**: Same as Session Pool (~$50-100 per contest)

---

## 📊 Final Comparison Table

| Aspect | ACA (34 Apps) | Session Pool | Hybrid |
|--------|---------------|--------------|--------|
| **Max Capacity** | 1,020 concurrent | 1,000+ concurrent | 1,000+ concurrent |
| **Idle Cost** | $2,040-2,550/mo | $0 | $0 |
| **Contest Cost** | $400-500 | $50-100 | $50-100 |
| **Setup Time** | 2-3 weeks | 1-2 days | 3-5 days |
| **Complexity** | 🔴 High | 🟢 Low | 🟡 Medium |
| **Terraform** | ✅ Full | ⚠️ Limited | ✅ Full |
| **Security** | 🟡 Medium | 🟢 High | 🟢 High |
| **Feasibility** | ⚠️ Complex | ✅ Easy | ✅ Easy |

---

## ✅ Conclusion

**For 500 students (1,000 executions)**:

1. **Session Pool is the best choice** ✅
   - Handles capacity easily
   - Low cost
   - Simple architecture
   - Fast performance

2. **ACA Pre-Warmed Pool is feasible but not ideal** ⚠️
   - Requires 34 apps (complexity)
   - High idle cost
   - More complex to manage

3. **Hybrid approach** (if Terraform is required) ✅
   - Use Session Pool for execution
   - Use Terraform for management
   - Best of both worlds

---

## 🎯 Next Steps

1. **Fix Session Pool ingress** (current blocker)
2. **Test with 100-200 students** (validate capacity)
3. **Scale to 500 students** (if needed)
4. **Consider Hybrid** (if Terraform is required)

---

**Bottom Line**: Session Pool is **feasible, cost-effective, and simple** for 500 students. ACA Pre-Warmed Pool works but is **complex and expensive**.


