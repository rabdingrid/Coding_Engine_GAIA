# Per-User Container Analysis: Terraform On-Demand Creation

## 🎯 Your Senior's Suggestion

**Approach**:
1. **Common ACA Environment**: Set up once (takes time only once)
2. **Per-User Containers**: Create separate container for each user
3. **Terraform**: Create containers on-demand per user request
4. **Base Images**: Pre-built images for each language (Python, Node, etc.)
5. **Fast**: Because base images are already built

---

## ⚠️ Critical Issue: Terraform Apply Time

### How Long Does Terraform Take?

**Terraform `apply` typically takes**:
- **30-60 seconds** per container app creation
- **20-40 seconds** for container app update
- **10-20 seconds** for container app scale

**This is TOO SLOW for per-request creation!**

### Example Timeline

```
User submits code
    ↓
Backend receives request
    ↓
Call Terraform to create container (30-60 seconds) ❌ TOO SLOW!
    ↓
Container starts (10-20 seconds)
    ↓
Execute code (1-5 seconds)
    ↓
Return result
    ↓
Cleanup container (via Terraform destroy - 20-30 seconds)
```

**Total Time**: **60-115 seconds per request** ❌

**User Experience**: Users wait 1-2 minutes per code execution!

---

## 🔍 Can This Work? Analysis

### Option 1: Terraform Per-Request (NOT Feasible)

**Problem**: 
- Terraform apply: 30-60 seconds
- Too slow for real-time requests
- Users can't wait 1-2 minutes

**Verdict**: ❌ **NOT FEASIBLE** for per-request creation

---

### Option 2: Pre-Create Containers with Terraform (Possible)

**Approach**:
1. **Before Contest**: Use Terraform to create 1,000 containers
2. **During Contest**: Route requests to existing containers
3. **After Contest**: Destroy containers via Terraform

**Timeline**:
```
Before Contest (30 min before):
  Terraform apply (creates 1,000 containers)
  Time: 30-60 minutes (parallel creation)
  
During Contest:
  Route requests to existing containers
  Time: 1-2 seconds per request ✅
  
After Contest:
  Terraform destroy (removes containers)
  Time: 20-30 minutes
```

**Verdict**: ⚠️ **POSSIBLE but complex**

---

### Option 3: Use ACA Auto-Scaling (Better)

**Approach**:
1. **Create Container App** with base image (once, via Terraform)
2. **Configure Auto-Scaling**: 0-1,000 replicas
3. **On Request**: ACA automatically creates replica (fast)
4. **After Execution**: ACA automatically scales down

**How It Works**:
```
User Request
    ↓
Backend → Container App (auto-scales)
    ↓
ACA creates new replica (5-10 seconds) ✅
    ↓
Execute code (1-5 seconds)
    ↓
Return result
    ↓
ACA scales down (automatic)
```

**Total Time**: **6-15 seconds per request** ✅

**Verdict**: ✅ **FEASIBLE and better approach**

---

## 📊 Detailed Analysis: Per-User Containers

### Architecture Options

#### Option A: Separate Container App Per User

**Terraform**:
```hcl
# Create 1,000 separate Container Apps (one per user)
resource "azurerm_container_app" "user_container" {
  count = 1000  # One per user
  
  name = "user-container-${count.index}"
  # ... configuration ...
}
```

**Problems**:
- ❌ **1,000 separate Container Apps** (complex to manage)
- ❌ **Terraform state file** becomes huge (1,000 resources)
- ❌ **Apply time**: 30-60 minutes to create all
- ❌ **Cost**: High (1,000 apps, even if idle)
- ❌ **Quota limits**: May hit ACA environment limits

**Verdict**: ❌ **NOT RECOMMENDED**

---

#### Option B: Single Container App with 1,000 Replicas

**Terraform**:
```hcl
# Single Container App, scale to 1,000 replicas
resource "azurerm_container_app" "code_executor" {
  name = "code-executor"
  
  template {
    min_replicas = 0
    max_replicas = 1000  # Scale up to 1,000
    
    container {
      image = "your-acr.azurecr.io/python-base:v1"  # Base image
      # ... configuration ...
    }
  }
  
  scale {
    min_replicas = 0
    max_replicas = 1000
  }
}
```

**How It Works**:
1. **Before Contest**: Terraform creates Container App (once, 30-60 seconds)
2. **During Contest**: ACA auto-scales replicas based on requests (5-10 seconds per replica)
3. **After Contest**: Terraform destroys or scales down

**Pros**:
- ✅ **Single resource** (simple)
- ✅ **Auto-scaling** (ACA handles it)
- ✅ **Fast** (5-10 seconds per replica)
- ✅ **Base images** (pre-built, fast startup)

**Cons**:
- ⚠️ **Replica limit**: 1,000 per app (matches your need)
- ⚠️ **Core quota**: Need 1,000 cores (default is 100, need increase)

**Verdict**: ✅ **FEASIBLE** (if quota increased)

---

#### Option C: Multiple Container Apps (Hybrid)

**Terraform**:
```hcl
# Create 10 Container Apps, each with 100 replicas
resource "azurerm_container_app" "executor_pool" {
  count = 10  # 10 apps
  
  name = "executor-pool-${count.index}"
  
  template {
    min_replicas = 0
    max_replicas = 100  # 100 per app = 1,000 total
  }
}
```

**Pros**:
- ✅ **Distributed** (10 apps)
- ✅ **Within quotas** (100 cores per app)
- ✅ **Auto-scaling** per app

**Cons**:
- ⚠️ **Load balancing** needed (10 apps)
- ⚠️ **More complex** (10 resources)

**Verdict**: ⚠️ **POSSIBLE** (more complex)

---

## ⚡ Performance Analysis

### Base Image Advantage

**Your Senior's Point**: Base images are pre-built, so container creation is fast.

**Reality**:
- ✅ **Base images help**: Faster than building from scratch
- ⚠️ **But Terraform apply is still slow**: 30-60 seconds
- ✅ **ACA auto-scaling is fast**: 5-10 seconds (uses base images)

**Key Insight**: 
- **Terraform per-request**: ❌ Too slow (30-60 seconds)
- **ACA auto-scaling**: ✅ Fast (5-10 seconds, uses base images)

---

### Timeline Comparison

#### Terraform Per-Request (NOT Feasible)
```
Request → Terraform Apply → Container Start → Execute → Destroy
         (30-60s)         (10-20s)        (1-5s)   (20-30s)
Total: 60-115 seconds ❌
```

#### ACA Auto-Scaling (Feasible)
```
Request → ACA Auto-Scale → Execute → Auto-Scale Down
         (5-10s)        (1-5s)    (automatic)
Total: 6-15 seconds ✅
```

#### Session Pool (Current)
```
Request → Session Allocation → Execute → Cleanup
         (3-5s)            (1-5s)    (automatic)
Total: 4-10 seconds ✅
```

---

## 💰 Cost Analysis

### Per-User Container Approach

**Assumptions**:
- 1,000 containers (500 students × 2 questions)
- Each container: 0.5 CPU, 1GB memory
- Contest duration: 2 hours

**Cost**:
- **1,000 containers × 0.5 CPU × 1GB × 2 hours** = ~$100-150 per contest
- **Idle cost**: $0 (if scaled to 0)

**vs Session Pool**:
- **1,000 sessions × 0.5 CPU × 1GB × 2 hours** = ~$50-100 per contest
- **Idle cost**: $0 (ready-sessions: 0)

**Cost Difference**: Similar (~$50-100 per contest)

---

## ✅ Feasibility Summary

### Your Senior's Approach (Clarified)

**What They Likely Mean**:
1. ✅ **Common ACA Environment**: Set up once (Terraform)
2. ✅ **Base Images**: Pre-built for each language (fast startup)
3. ✅ **Auto-Scaling**: Use ACA auto-scaling (not Terraform per-request)
4. ✅ **Per-User Isolation**: Each execution gets its own replica

**This IS Feasible!** ✅

---

### Recommended Implementation

**Terraform** (One-time setup):
```hcl
resource "azurerm_container_app" "code_executor" {
  name = "code-executor"
  
  template {
    min_replicas = 0
    max_replicas = 1000
    
    container {
      image = "your-acr.azurecr.io/python-base:v1"  # Pre-built base image
      cpu   = 0.5
      memory = "1.0Gi"
    }
  }
  
  scale {
    min_replicas = 0
    max_replicas = 1000
  }
}
```

**Backend** (Route to Container App):
```python
CONTAINER_APP_URL = "https://code-executor.azurecontainerapps.io"

def execute_code(request):
    # ACA auto-scales replicas automatically
    response = requests.post(
        f"{CONTAINER_APP_URL}/execute",
        json={
            "language": request.language,
            "code": request.code
        }
    )
    return response.json()
```

**How It Works**:
1. **First Request**: ACA creates replica (5-10 seconds)
2. **Execute Code**: 1-5 seconds
3. **Auto-Scale Down**: ACA removes replica automatically

**Total Time**: **6-15 seconds** ✅

---

## 📊 Comparison: This Approach vs Session Pool

| Aspect | ACA Auto-Scaling | Session Pool |
|--------|-----------------|--------------|
| **Setup** | Terraform (once) | Azure CLI (once) |
| **Base Images** | ✅ Pre-built | ✅ Pre-built |
| **Per-Request Time** | 6-15 seconds | 4-10 seconds |
| **Max Capacity** | 1,000 replicas | 1,000+ sessions |
| **Auto-Scaling** | ✅ Yes | ✅ Yes |
| **Quota** | ⚠️ Need 1,000 cores | ✅ No hard limit |
| **Cost** | ~$100-150/contest | ~$50-100/contest |
| **Terraform Support** | ✅ Full | ⚠️ Limited |
| **Security** | 🟡 Container-level | 🟢 Hyper-V |

---

## 🎯 Final Verdict

### Is Your Senior's Approach Feasible?

**YES, but with clarification**:

1. ✅ **Common ACA Environment**: Set up once (feasible)
2. ✅ **Base Images**: Pre-built (feasible, fast)
3. ⚠️ **Terraform Per-Request**: NOT feasible (too slow)
4. ✅ **ACA Auto-Scaling**: Feasible (fast, uses base images)
5. ✅ **Per-User Isolation**: Each replica is isolated (feasible)

**Recommended Approach**:
- Use **Terraform to create Container App** (once)
- Use **ACA auto-scaling** (not Terraform per-request)
- Use **pre-built base images** (fast startup)
- Each execution gets its own replica (isolation)

---

## ✅ Recommendation

**For 500 Students (1,000 executions)**:

### Option 1: ACA Auto-Scaling (Your Senior's Approach - Clarified) ✅

**Pros**:
- ✅ Full Terraform support
- ✅ Pre-built base images (fast)
- ✅ Auto-scaling (6-15 seconds)
- ✅ Per-user isolation

**Cons**:
- ⚠️ Need quota increase (1,000 cores)
- ⚠️ Slightly slower than Session Pool
- ⚠️ Slightly more expensive

**Implementation**: ~3-5 days

---

### Option 2: Session Pool (Current) ✅

**Pros**:
- ✅ Fastest (4-10 seconds)
- ✅ Cheapest ($50-100 per contest)
- ✅ No quota issues
- ✅ Better security (Hyper-V)

**Cons**:
- ⚠️ Limited Terraform support
- ⚠️ Preview feature

**Implementation**: ~1-2 days (if ingress fixed)

---

## 📋 Next Steps

1. **Clarify with Senior**: 
   - Terraform per-request? (Not feasible)
   - Or Terraform + ACA auto-scaling? (Feasible)

2. **If ACA Auto-Scaling**:
   - Request quota increase (1,000 cores)
   - Create base images for each language
   - Set up Terraform for Container App
   - Test auto-scaling

3. **Compare Both**:
   - Test Session Pool (if ingress fixed)
   - Test ACA Auto-Scaling
   - Choose based on requirements

---

**Bottom Line**: Your senior's approach **IS feasible** if using **ACA auto-scaling** (not Terraform per-request). Base images help, but Terraform per-request is too slow.


