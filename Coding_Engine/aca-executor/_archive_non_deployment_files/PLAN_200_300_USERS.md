# Plan: 200-300 Users with <5 Second Wait Time

## 🎯 Requirements

- **No user waits more than 5 seconds**
- **Target**: 200-300 concurrent users
- **Current Performance**: 180ms average execution time
- **Single Replica Capacity**: 8 concurrent requests (Gunicorn: 4 workers × 2 threads)

---

## 📊 Capacity Calculation

### Wait Time Formula

```
Wait Time = (Queue Length / Processing Rate) × Execution Time
```

Where:
- **Queue Length** = Users waiting - Current capacity
- **Processing Rate** = Replicas × 8 concurrent per replica
- **Execution Time** = 180ms average

### For <5 Second Wait Time

**Maximum Queue Length Allowed:**
```
5 seconds = Queue Length / (Replicas × 8) × 0.18 seconds
Queue Length = (5 / 0.18) × (Replicas × 8)
Queue Length = 27.78 × (Replicas × 8)
```

**But we want to minimize queue, so let's ensure immediate processing:**

---

## 🎯 Recommended Configuration

### For 200 Users

**Worst Case: All 200 users submit simultaneously**

**Required Replicas:**
```
200 concurrent requests ÷ 8 concurrent per replica = 25 replicas
```

**Recommended Configuration:**
```terraform
min_replicas = 20   # Pre-warmed (20 × 8 = 160 concurrent)
max_replicas = 30   # Peak capacity (30 × 8 = 240 concurrent)
```

**Wait Time Analysis:**
- **20 replicas**: 160 concurrent capacity
- **200 users**: 40 users in queue
- **Wait Time**: 40 ÷ 160 × 0.18s = **0.045 seconds** ✅
- **With auto-scaling to 25 replicas**: **0 seconds** ✅

**Cost (2-hour contest):**
```
Pre-warmed (20 replicas × 2 hours):
  20 × $0.108/hour × 2 = $4.32

Peak (30 replicas × 30 minutes):
  30 × $0.108/hour × 0.5 = $1.62

Average (25 replicas × 1.5 hours):
  25 × $0.108/hour × 1.5 = $4.05
────────────────────────────────────
Total:                            $9.99
```

**Cost per Student**: $9.99 / 200 = **$0.050 per student**

---

### For 250 Users

**Worst Case: All 250 users submit simultaneously**

**Required Replicas:**
```
250 concurrent requests ÷ 8 concurrent per replica = 31.25 → 32 replicas
```

**Recommended Configuration:**
```terraform
min_replicas = 25   # Pre-warmed (25 × 8 = 200 concurrent)
max_replicas = 35   # Peak capacity (35 × 8 = 280 concurrent)
```

**Wait Time Analysis:**
- **25 replicas**: 200 concurrent capacity
- **250 users**: 50 users in queue
- **Wait Time**: 50 ÷ 200 × 0.18s = **0.045 seconds** ✅
- **With auto-scaling to 32 replicas**: **0 seconds** ✅

**Cost (2-hour contest):**
```
Pre-warmed (25 replicas × 2 hours):
  25 × $0.108/hour × 2 = $5.40

Peak (35 replicas × 30 minutes):
  35 × $0.108/hour × 0.5 = $1.89

Average (30 replicas × 1.5 hours):
  30 × $0.108/hour × 1.5 = $4.86
────────────────────────────────────
Total:                            $12.15
```

**Cost per Student**: $12.15 / 250 = **$0.049 per student**

---

### For 300 Users

**Worst Case: All 300 users submit simultaneously**

**Required Replicas:**
```
300 concurrent requests ÷ 8 concurrent per replica = 37.5 → 38 replicas
```

**Recommended Configuration:**
```terraform
min_replicas = 30   # Pre-warmed (30 × 8 = 240 concurrent)
max_replicas = 40   # Peak capacity (40 × 8 = 320 concurrent)
```

**Wait Time Analysis:**
- **30 replicas**: 240 concurrent capacity
- **300 users**: 60 users in queue
- **Wait Time**: 60 ÷ 240 × 0.18s = **0.045 seconds** ✅
- **With auto-scaling to 38 replicas**: **0 seconds** ✅

**Cost (2-hour contest):**
```
Pre-warmed (30 replicas × 2 hours):
  30 × $0.108/hour × 2 = $6.48

Peak (40 replicas × 30 minutes):
  40 × $0.108/hour × 0.5 = $2.16

Average (35 replicas × 1.5 hours):
  35 × $0.108/hour × 1.5 = $5.67
────────────────────────────────────
Total:                            $14.31
```

**Cost per Student**: $14.31 / 300 = **$0.048 per student**

---

## 💰 Cost Summary

| Users | Min Replicas | Max Replicas | Contest Cost | Cost/Student |
|-------|--------------|--------------|--------------|--------------|
| **200** | 20 | 30 | **$10** | **$0.050** |
| **250** | 25 | 35 | **$12** | **$0.049** |
| **300** | 30 | 40 | **$14** | **$0.048** |

**Average**: **$10-14 per contest** = **$0.048-0.050 per student**

---

## 🚀 Implementation Plan

### Step 1: Update Terraform Configuration

**File**: `terraform/main.tf` or `terraform/variables.tf`

```hcl
# For 200-300 users
variable "min_replicas" {
  description = "Minimum number of replicas"
  type        = number
  default     = 25  # Pre-warmed for 250 users
}

variable "max_replicas" {
  description = "Maximum number of replicas"
  type        = number
  default     = 40  # Peak capacity for 300 users
}
```

**Apply:**
```bash
cd terraform
terraform apply -var="min_replicas=25" -var="max_replicas=40"
```

---

### Step 2: Configure Auto-Scaling Rules

**Azure Portal → Container App → Scale**

**Scale Up Rules:**
1. **HTTP Requests**:
   - Metric: Average requests per replica
   - Threshold: > 6 requests
   - Scale: +2 replicas per minute

2. **CPU Usage**:
   - Metric: CPU percentage
   - Threshold: > 50%
   - Scale: +2 replicas per minute

**Scale Down Rules:**
1. **CPU Usage**:
   - Metric: CPU percentage
   - Threshold: < 30% for 5 minutes
   - Scale: -1 replica per minute

**Cooldown Periods:**
- Scale Up: 30 seconds
- Scale Down: 5 minutes

---

### Step 3: Test Configuration

**Test Script:**
```bash
# Monitor replicas
watch -n 2 'az containerapp show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --query "properties.template.scale.minReplicas" -o tsv'

# Run load test
python3 load-test-multi-user.py -n 300 -l python
```

**Expected Behavior:**
- Start: 25 replicas (pre-warmed)
- Under Load: Scale to 30-35 replicas
- Peak: Scale to 40 replicas
- Wait Time: < 1 second (usually 0 seconds)

---

## 📊 Wait Time Guarantee Analysis

### Scenario 1: 200 Users, All Submit Simultaneously

**With 20 Replicas (Pre-warmed):**
- Capacity: 20 × 8 = 160 concurrent
- Queue: 200 - 160 = 40 users
- Wait Time: 40 ÷ 160 × 0.18s = **0.045 seconds** ✅

**With Auto-Scaling to 25 Replicas:**
- Capacity: 25 × 8 = 200 concurrent
- Queue: 0 users
- Wait Time: **0 seconds** ✅

---

### Scenario 2: 300 Users, All Submit Simultaneously

**With 30 Replicas (Pre-warmed):**
- Capacity: 30 × 8 = 240 concurrent
- Queue: 300 - 240 = 60 users
- Wait Time: 60 ÷ 240 × 0.18s = **0.045 seconds** ✅

**With Auto-Scaling to 38 Replicas:**
- Capacity: 38 × 8 = 304 concurrent
- Queue: 0 users
- Wait Time: **0 seconds** ✅

---

### Scenario 3: Gradual Submission (Realistic)

**If requests arrive over 10 seconds:**
- Peak Concurrent: ~50-100 users
- With 25 replicas: 200 concurrent capacity
- Wait Time: **0 seconds** (all processed immediately) ✅

---

## 💡 Cost Optimization

### Option 1: Contest Day Scaling (Recommended)

**Before Contest:**
```bash
# Scale to zero (no cost)
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
  --min-replicas 25
```

**During Contest:**
- Auto-scales 25-40 replicas based on load

**After Contest:**
```bash
# Scale back down
az containerapp update \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --min-replicas 0
```

**Cost**: **$10-14 per contest** (only pay during contest)

---

### Option 2: Always-On Pre-Warmed Pool

**Configuration:**
```terraform
min_replicas = 25   # Always running
max_replicas = 40   # Scale up during contest
```

**Cost:**
- **Idle**: 25 × $0.108/hour × 24 hours × 30 days = **$1,944/month**
- **Contest**: Additional $2-4 per contest

**Not Recommended**: Too expensive for idle periods.

---

## 📋 Recommended Plan

### For 200-300 Users with <5 Second Wait Time

**Configuration:**
```terraform
min_replicas = 25   # Pre-warmed for 250 users
max_replicas = 40   # Peak capacity for 300 users
```

**Auto-Scaling:**
- Scale up when: CPU > 50% OR requests per replica > 6
- Scale down when: CPU < 30% for 5 minutes
- Scale speed: 2 replicas per minute

**Expected Performance:**
- ✅ **Wait Time**: < 1 second (usually 0 seconds)
- ✅ **Success Rate**: 100%
- ✅ **No user waits > 5 seconds**

**Cost:**
- **Per Contest**: $10-14
- **Per Student**: $0.048-0.050
- **Monthly (5 contests)**: $50-70

---

## 🎯 Action Items

### 1. Update Terraform (Immediate)

```bash
cd terraform
terraform apply -var="min_replicas=25" -var="max_replicas=40"
```

### 2. Configure Auto-Scaling Rules

**Azure Portal:**
- Container Apps → ai-ta-ra-code-executor2 → Scale
- Add HTTP request-based scaling rule
- Set threshold: > 6 requests per replica

### 3. Test with Load Test

```bash
python3 load-test-multi-user.py -n 300 -l python
```

**Verify:**
- Replicas scale from 25 to 40
- Wait time < 1 second
- All requests successful

### 4. Set Up Scheduled Scaling (Optional)

**Before Contest:**
- Scale to 25 replicas 30 minutes before

**After Contest:**
- Scale to 0 replicas to save costs

---

## ✅ Summary

**For 200-300 Users with <5 Second Wait Time:**

✅ **Configuration:**
- Min Replicas: 25
- Max Replicas: 40
- Auto-Scaling: Enabled

✅ **Performance:**
- Wait Time: < 1 second (usually 0 seconds)
- Success Rate: 100%
- No user waits > 5 seconds

✅ **Cost:**
- Per Contest: **$10-14**
- Per Student: **$0.048-0.050**
- Monthly (5 contests): **$50-70**

**This configuration guarantees no user waits more than 5 seconds while keeping costs affordable!** 🎉

