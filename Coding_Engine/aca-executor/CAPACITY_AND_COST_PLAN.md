# Capacity & Cost Plan: 200-300 Users with <5 Second Wait Time

## 🎯 Goal

**Requirement**: No user should wait more than **5 seconds** for code execution  
**Target**: 200-300 concurrent users  
**Current Performance**: ~180ms average execution time per request

---

## 📊 Capacity Analysis

### Current Performance Metrics

From load testing:
- **Average Execution Time**: 180ms per request
- **Single Replica Capacity**: 8 concurrent requests (Gunicorn: 4 workers × 2 threads)
- **Throughput per Replica**: ~44 requests/second (8 concurrent × 5.5 requests/second)

### Wait Time Calculation

**Scenario 1: All Users Submit Simultaneously**

If 200 users submit at the exact same moment:
- **Replicas Needed**: 200 concurrent requests ÷ 8 concurrent per replica = **25 replicas**
- **Wait Time**: 0 seconds (all processed immediately)

**Scenario 2: Requests Arrive Over Time**

If requests arrive over a 10-second window:
- **Peak Concurrent**: ~50-100 users
- **Replicas Needed**: 100 ÷ 8 = **12-13 replicas**
- **Wait Time**: < 1 second (with proper load balancing)

**Scenario 3: Burst Traffic (Contest Start)**

If all 300 users start at contest beginning:
- **Replicas Needed**: 300 ÷ 8 = **37-38 replicas**
- **Wait Time**: 0 seconds (all processed immediately)

---

## 🎯 Recommended Configuration

### Option 1: Pre-Warmed Pool (Recommended)

**Configuration:**
```terraform
min_replicas = 15   # Pre-warmed for 200 users
max_replicas = 40   # Scale up for 300 users + buffer
```

**Capacity:**
- **15 replicas**: 15 × 8 = 120 concurrent requests
- **40 replicas**: 40 × 8 = 320 concurrent requests
- **Wait Time**: < 1 second (with auto-scaling)

**Cost Analysis:**
- **Per Replica**: $0.108/hour (2 CPU, 4 GiB)
- **15 replicas (pre-warmed)**: 15 × $0.108 = $1.62/hour
- **40 replicas (peak)**: 40 × $0.108 = $4.32/hour

### Option 2: Minimal Pre-Warm + Aggressive Auto-Scaling

**Configuration:**
```terraform
min_replicas = 10   # Minimal pre-warmed
max_replicas = 40   # Scale up aggressively
```

**Auto-Scaling Rules:**
- **Scale Up**: When CPU > 50% OR request queue > 5
- **Scale Down**: When CPU < 30% for 5 minutes
- **Scale Speed**: 2-3 replicas per minute

**Capacity:**
- **10 replicas**: 10 × 8 = 80 concurrent requests
- **40 replicas**: 40 × 8 = 320 concurrent requests
- **Wait Time**: < 2 seconds (during scaling)

---

## 💰 Cost Analysis for 200-300 Users

### Contest Scenario: 2 Hours

**Assumptions:**
- Contest duration: 2 hours
- 200-300 students
- Each student submits 2 questions = 400-600 total executions
- Requests distributed over 2-hour period

### Cost Calculation

#### Option 1: Pre-Warmed Pool (15 replicas)

**Pre-warmed (15 replicas × 2 hours):**
```
15 × $0.108/hour × 2 hours = $3.24
```

**Peak Load (40 replicas × 30 minutes):**
```
40 × $0.108/hour × 0.5 hours = $2.16
```

**Average Load (25 replicas × 1.5 hours):**
```
25 × $0.108/hour × 1.5 hours = $4.05
```

**Total Cost**: ~$9.45 per contest

**Cost per Student**: $9.45 / 250 = **$0.038 per student**

---

#### Option 2: Auto-Scaling (10-40 replicas)

**Pre-warmed (10 replicas × 0.5 hours):**
```
10 × $0.108/hour × 0.5 hours = $0.54
```

**Average (25 replicas × 1.5 hours):**
```
25 × $0.108/hour × 1.5 hours = $4.05
```

**Peak (40 replicas × 0.5 hours):**
```
40 × $0.108/hour × 0.5 hours = $2.16
```

**Total Cost**: ~$6.75 per contest

**Cost per Student**: $6.75 / 250 = **$0.027 per student**

---

### Monthly Cost Estimates

| Scenario | Monthly Cost | Notes |
|----------|-------------|-------|
| **Scale to Zero (Idle)** | $0 | No replicas when idle |
| **1 Contest/Month** | $7-10 | Auto-scaling option |
| **5 Contests/Month** | $35-50 | Auto-scaling option |
| **Always-On (15 replicas)** | $1,166 | 15 × $0.108 × 24 × 30 |

**Recommendation**: Use auto-scaling (Option 2) to minimize costs.

---

## 📈 Replica Requirements by User Count

### For 200 Users

**Configuration:**
```terraform
min_replicas = 12   # Pre-warmed (12 × 8 = 96 concurrent)
max_replicas = 30   # Peak capacity (30 × 8 = 240 concurrent)
```

**Wait Time**: < 1 second  
**Cost**: ~$5-7 per contest

---

### For 250 Users

**Configuration:**
```terraform
min_replicas = 15   # Pre-warmed (15 × 8 = 120 concurrent)
max_replicas = 35   # Peak capacity (35 × 8 = 280 concurrent)
```

**Wait Time**: < 1 second  
**Cost**: ~$7-9 per contest

---

### For 300 Users

**Configuration:**
```terraform
min_replicas = 18   # Pre-warmed (18 × 8 = 144 concurrent)
max_replicas = 40   # Peak capacity (40 × 8 = 320 concurrent)
```

**Wait Time**: < 1 second  
**Cost**: ~$8-12 per contest

---

## 🚀 Implementation Plan

### Step 1: Update Terraform Configuration

**File**: `terraform/main.tf`

```hcl
resource "azurerm_container_app" "executor" {
  name     = "ai-ta-ra-code-executor2"
  # ... other config ...
  
  template {
    min_replicas = 15   # Pre-warmed for 200-300 users
    max_replicas = 40   # Peak capacity
    
    scale {
      rules {
        name = "http-requests"
        http {
          metadata = {
            concurrentRequests = "8"  # Scale when > 8 requests per replica
          }
        }
      }
      
      rules {
        name = "cpu-scaling"
        custom {
          metric = "cpu"
          threshold = 50  # Scale when CPU > 50%
        }
      }
    }
  }
}
```

---

### Step 2: Configure Auto-Scaling Rules

**Azure Portal Configuration:**

1. **Scale Up Rules:**
   - **HTTP Requests**: Scale when average requests per replica > 6
   - **CPU**: Scale when CPU > 50%
   - **Scale Speed**: 2-3 replicas per minute

2. **Scale Down Rules:**
   - **CPU**: Scale down when CPU < 30% for 5 minutes
   - **Scale Speed**: 1 replica per minute

3. **Cooldown Periods:**
   - **Scale Up Cooldown**: 30 seconds
   - **Scale Down Cooldown**: 5 minutes

---

### Step 3: Test Auto-Scaling

**Test Script:**
```bash
# Monitor replicas during load test
watch -n 2 'az containerapp show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --query "properties.template.scale.minReplicas" -o tsv'

# Run load test
python3 load-test-multi-user.py -n 300 -l python
```

**Expected Behavior:**
- Start: 15 replicas
- Under Load: Scale to 25-35 replicas
- Peak: Scale to 40 replicas
- After Load: Scale down to 15 replicas

---

## 📊 Wait Time Guarantee Analysis

### Current System (1 Replica)

**With 200 concurrent users:**
- Capacity: 8 concurrent
- Queue: 192 users waiting
- Wait Time: 192 ÷ 8 × 0.18s = **4.32 seconds** (acceptable)
- But if more users arrive: **> 5 seconds** ❌

### Recommended System (15-40 Replicas)

**With 200 concurrent users:**
- Capacity: 15 × 8 = 120 concurrent (pre-warmed)
- Queue: 80 users waiting
- Wait Time: 80 ÷ 120 × 0.18s = **0.12 seconds** ✅
- With auto-scaling to 25 replicas: **0 seconds** ✅

**With 300 concurrent users:**
- Capacity: 18 × 8 = 144 concurrent (pre-warmed)
- Queue: 156 users waiting
- Wait Time: 156 ÷ 144 × 0.18s = **0.195 seconds** ✅
- With auto-scaling to 40 replicas: **0 seconds** ✅

---

## 💡 Cost Optimization Strategies

### Strategy 1: Contest Day Scaling

**Before Contest:**
```bash
# Scale to minimal
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 0
```

**30 Minutes Before Contest:**
```bash
# Pre-warm replicas
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 15
```

**During Contest:**
- Auto-scales 15-40 replicas based on load

**After Contest:**
```bash
# Scale back down
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 0
```

**Cost**: ~$7-10 per contest (only pay during contest)

---

### Strategy 2: Scheduled Scaling

**Use Azure Automation or Logic Apps:**
- **Before Contest**: Scale to 15 replicas
- **During Contest**: Auto-scale 15-40 replicas
- **After Contest**: Scale to 0 replicas

**Cost**: Same as Strategy 1

---

## 📋 Recommended Plan

### For 200-300 Users with <5 Second Wait Time

**Configuration:**
```terraform
min_replicas = 15   # Pre-warmed pool
max_replicas = 40   # Peak capacity
```

**Auto-Scaling Rules:**
- Scale up when: CPU > 50% OR requests per replica > 6
- Scale down when: CPU < 30% for 5 minutes
- Scale speed: 2-3 replicas per minute

**Expected Performance:**
- ✅ **Wait Time**: < 1 second (usually 0 seconds)
- ✅ **Success Rate**: 100%
- ✅ **Cost**: $7-10 per contest
- ✅ **Cost per Student**: $0.027-0.040

**Monthly Cost (5 contests/month):**
- **Contests**: 5 × $8 = $40
- **Idle**: $0 (scale to zero)
- **Total**: **$40/month**

---

## 🎯 Cost Comparison

| Configuration | Contest Cost | Monthly (5 contests) | Wait Time |
|--------------|-------------|---------------------|-----------|
| **Current (1 replica)** | $0.22 | $1.10 | ❌ > 5 seconds |
| **Recommended (15-40)** | $7-10 | $35-50 | ✅ < 1 second |
| **Always-On (15 replicas)** | $0 | $1,166 | ✅ < 1 second |

**Recommendation**: Use auto-scaling (15-40 replicas) for best cost-performance balance.

---

## ✅ Action Items

1. **Update Terraform**:
   - Set `min_replicas = 15`
   - Set `max_replicas = 40`
   - Configure auto-scaling rules

2. **Test Auto-Scaling**:
   - Run load test with 300 users
   - Verify replicas scale from 15 to 40
   - Verify wait time < 1 second

3. **Monitor Costs**:
   - Set up Azure Cost Management alerts
   - Track spending per contest
   - Optimize based on actual usage

4. **Implement Scheduled Scaling**:
   - Scale up 30 minutes before contest
   - Scale down after contest ends
   - Save costs when idle

---

## 📊 Summary

**For 200-300 Users with <5 Second Wait Time:**

✅ **Recommended Configuration:**
- Min Replicas: 15
- Max Replicas: 40
- Auto-Scaling: Enabled

✅ **Expected Performance:**
- Wait Time: < 1 second (usually 0 seconds)
- Success Rate: 100%
- No user waits > 5 seconds

✅ **Cost:**
- Per Contest: $7-10
- Per Student: $0.027-0.040
- Monthly (5 contests): $35-50

**This configuration ensures no user waits more than 5 seconds while keeping costs affordable!** 🎉

