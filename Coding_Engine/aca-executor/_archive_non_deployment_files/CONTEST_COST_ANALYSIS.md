# Cost Analysis: 250 Students Contest (3.5 Hours)

## 📊 **Current Configuration**

### **Resource Settings:**
- **Memory**: 4Gi (increased from 2Gi for Java support)
- **CPU**: 2.0 (increased from 1.0 for 4Gi memory requirement)
- **Min Replicas**: 1 (for testing, can scale to 0 when idle)
- **Max Replicas**: 3 (for testing, should be 50-100 for contest)

### **Cost per Replica:**
- **vCPU**: 2.0 × $0.000012/vCPU-second = **$0.000024/second**
- **Memory**: 4Gi × $0.0000015/GB-second = **$0.000006/second**
- **Total**: **$0.00003/second = $0.108/hour per replica**

---

## 🎯 **Contest Scenario: 250 Students × 2 Questions**

### **Load Analysis:**
- **Total Executions**: 500 (250 students × 2 questions)
- **Duration**: 3.5 hours
- **Average Execution Time**: ~500ms per execution
- **Peak Concurrent Requests**: ~50-100 students (if all submit at once)
- **Realistic Concurrent**: ~20-40 students (distributed over time)

### **Replica Requirements:**

| Scenario | Replicas Needed | Reasoning |
|----------|----------------|-----------|
| **Pre-warmed Pool** | 10 | Ready for contest start |
| **Peak Load** | 30-50 | Handle burst traffic |
| **Average Load** | 20-30 | Normal distribution |
| **Minimum** | 15 | Bare minimum (may have delays) |

**Recommended**: **30 replicas** (balanced performance and cost)

---

## 💰 **Cost Breakdown**

### **Per Replica Cost:**
```
vCPU:  2.0 × $0.000012 = $0.000024/second
Memory: 4Gi × $0.0000015 = $0.000006/second
─────────────────────────────────────────
Total:                    $0.00003/second
                          = $0.108/hour
                          = $2.592/day
```

### **Contest Cost (3.5 hours):**

#### **Scenario 1: Pre-warmed Only (10 replicas)**
```
10 replicas × $0.108/hour × 3.5 hours = $3.78
```
**Result**: May have delays during peak

#### **Scenario 2: Recommended (30 replicas)**
```
30 replicas × $0.108/hour × 3.5 hours = $11.34
```
**Result**: Smooth operation, handles peak load

#### **Scenario 3: Peak Load (50 replicas)**
```
50 replicas × $0.108/hour × 3.5 hours = $18.90
```
**Result**: Excellent performance, no delays

#### **Scenario 4: Auto-scaling (10-30 replicas)**
```
Pre-warmed (10): 10 × $0.108 × 0.5 = $0.54  (first 30 min)
Average (20):    20 × $0.108 × 2.5 = $5.40  (middle 2.5 hours)
Peak (30):       30 × $0.108 × 0.5 = $1.62  (last 30 min)
────────────────────────────────────────────
Total:                                    $7.56
```
**Result**: Optimal cost-performance balance

---

## 📈 **Cost Comparison**

### **Old Configuration (2Gi, 1 CPU):**
- **Per replica**: $0.054/hour
- **30 replicas × 3.5 hours**: **$5.67**

### **New Configuration (4Gi, 2 CPU):**
- **Per replica**: $0.108/hour (2x increase)
- **30 replicas × 3.5 hours**: **$11.34**

### **Cost Increase:**
- **2x more expensive** per replica
- **But**: Java now works! ✅
- **Total contest cost**: ~$8-12 (vs $3-6 before)

---

## 💡 **Cost Optimization Strategies**

### **1. Scale to Zero When Idle**
```terraform
min_replicas = 0  # Scale to zero when no traffic
```
**Savings**: $0 when idle (vs $2.59/day for 1 replica)

### **2. Use Auto-scaling**
```terraform
min_replicas = 5   # Pre-warmed pool
max_replicas = 50  # Scale up during contest
```
**Savings**: Only pay for what you use

### **3. Contest Day Scaling**
- **Before contest**: `min_replicas = 0` (no cost)
- **Contest start**: Scale to 10-15 replicas
- **During contest**: Auto-scale 20-30 replicas
- **After contest**: Scale back to 0

**Estimated Contest Cost**: **$7-12** (auto-scaling)

---

## 📊 **Monthly Cost Estimates**

### **Idle (min_replicas = 0):**
```
Cost: $0/month
```

### **Always On (min_replicas = 1):**
```
1 replica × $0.108/hour × 24 hours × 30 days = $77.76/month
```

### **Contest Only (1 contest/month):**
```
Contest: $7-12
Idle: $0
────────────────
Total: $7-12/month
```

### **Regular Usage (5 contests/month):**
```
5 contests × $10 = $50/month
Idle: $0
────────────────
Total: $50/month
```

---

## 🎯 **Recommendations**

### **For 250 Students Contest:**

1. **Terraform Configuration:**
   ```terraform
   min_replicas = 5   # Pre-warmed for contest start
   max_replicas = 50  # Handle peak load
   ```

2. **Estimated Cost**: **$7-12 per contest** (with auto-scaling)

3. **Cost per Student**: **$0.028 - $0.048** (very affordable!)

4. **Monthly Cost** (1 contest/month): **$7-12/month**

---

## ✅ **Summary**

**Q: Will new config cost more?**
**A: Yes, 2x more per replica, but:**
- ✅ Java now works (was broken before)
- ✅ Still very affordable ($7-12 per contest)
- ✅ Can scale to zero when idle ($0 cost)

**Q: Cost for 250 students × 2 questions, 3.5 hours?**
**A: ~$7-12 per contest** (with auto-scaling)

**Cost per Student**: **$0.028 - $0.048** (extremely affordable!)

---

**Status**: ✅ **Cost-effective and production-ready!**


