# Current Infrastructure Cost Analysis

## 💰 Cost Breakdown (Current Configuration)

### 1. Azure Container Apps - Code Executor

**Configuration:**
- Min Replicas: 10
- Max Replicas: 100
- CPU per Replica: 1.0 core
- Memory per Replica: 2.0 GiB

**Pricing (East US 2):**
- vCPU: $0.000012 per vCPU-second
- Memory: $0.0000015 per GiB-second

**Cost Calculation:**

#### Scenario A: Idle (10 replicas running)
```
10 replicas × (1.0 vCPU + 2.0 GiB) × $0.000012/sec
= 10 × $0.000012/sec
= $0.00012/sec
= $0.432/hour
= $10.37/day (if running 24/7)
```

#### Scenario B: Contest (2 hours, peak 100 replicas)
```
Pre-warmed (10 replicas × 2 hours):
  10 × $0.000012/sec × 7200 sec = $0.864

Peak (100 replicas × 30 minutes):
  100 × $0.000012/sec × 1800 sec = $2.16

Average (50 replicas × 1.5 hours):
  50 × $0.000012/sec × 5400 sec = $3.24

Total: ~$6.27 for 2-hour contest
```

#### Scenario C: Monthly (if running 24/7 with 10 replicas)
```
10 replicas × $0.000012/sec × 2,592,000 sec/month
= $311.04/month
```

---

### 2. Azure Container Registry (ACR)

**Configuration:**
- Basic tier (if using)
- Storage: ~1-2 GB (images)

**Cost:**
- Basic tier: ~$5/month
- Storage: ~$0.10/GB/month = $0.10-0.20/month
- **Total: ~$5-6/month**

---

### 3. Container Apps Environment

**Cost:**
- Included in Container Apps pricing
- **Total: $0** (no separate charge)

---

### 4. PostgreSQL Database (Railway - External)

**Note:** You're using Railway PostgreSQL, not Azure.

**Cost:**
- Railway pricing (external service)
- **Not included in Azure costs**

---

## 📊 Total Cost Summary

### For 200 Students Contest (2 hours):
```
Container Apps: $6.27
ACR: $0 (one-time, already running)
Environment: $0
─────────────────────────
Total: ~$6-7 per contest
```

### Monthly (if running 24/7):
```
Container Apps (10 replicas): $311/month
ACR: $5/month
─────────────────────────
Total: ~$316/month
```

### Cost-Optimized (Scale to 0 when not in use):
```
Container Apps (min_replicas = 0): $0 when idle
ACR: $5/month
─────────────────────────
Total: ~$5/month + usage costs
```

---

## 💡 Cost Optimization Tips

1. **Set min_replicas = 0** when not running contests
   - Saves $311/month
   - Containers start in 10-30 seconds when needed

2. **Use Auto-scaling**
   - Only pay for what you use
   - Scales down automatically after contest

3. **Reserve Capacity** (if running 24/7)
   - Can save up to 30% with reserved instances

4. **Monitor Usage**
   - Use Azure Cost Management
   - Set up alerts for spending

---

## 🎯 Recommended Configuration

### For Contests Only:
```terraform
min_replicas = 0   # Scale to zero when idle
max_replicas = 100  # Scale up for contests
```

**Cost:**
- Idle: $0/month
- Contest (2 hours): $6-7 per contest

### For Always-On:
```terraform
min_replicas = 5   # Minimal pre-warmed
max_replicas = 100  # Scale up for contests
```

**Cost:**
- Idle: ~$155/month (5 replicas)
- Contest: Additional $3-4 per contest

---

## 📈 Cost Comparison

| Scenario | Monthly Cost | Contest Cost |
|----------|-------------|--------------|
| **Scale to Zero** | $5 (ACR only) | $6-7 per contest |
| **Always-On (5 replicas)** | $160 | $3-4 per contest |
| **Always-On (10 replicas)** | $316 | $0 (already running) |

---

## ✅ Current Setup Cost

**Your current configuration:**
- Min Replicas: 10
- Max Replicas: 100

**If running 24/7:**
- **Monthly: ~$316**
- **Per Contest (2 hours): ~$6-7**

**Recommendation:** Set `min_replicas = 0` to save $311/month when not running contests.
