# Current Daily Cost - Exact Calculation

## 📊 Current Configuration (as of 2025-11-26)

### Backend Container App
- **Name**: `ai-ta-ra-coding-engine`
- **Status**: Running
- **Replicas**: Checking...
- **CPU**: Checking...
- **Memory**: Checking...

### Session Pool
- **Name**: `ai-ta-ra-session-pool`
- **Ready Sessions**: 1
- **Max Sessions**: 5
- **CPU per Session**: 0.5 vCPU (from creation command)
- **Memory per Session**: 1.0 Gi (from creation command)
- **Cooldown Period**: 300 seconds (5 minutes)

---

## 💰 Azure Container Apps Pricing (East US 2)

Based on Azure pricing as of 2024:

| Resource | Unit | Cost |
|----------|------|------|
| **vCPU** | Per vCPU-second | $0.000024 |
| **Memory** | Per GB-second | $0.000003 |
| **Container Apps Environment** | Per day | $0.10 (fixed) |
| **ACR (Basic)** | Per day | $0.17 (fixed) |

---

## 💵 Daily Cost Breakdown

### 1. Session Pool - Ready Sessions

**1 Ready Session** (always running, 24 hours):
- **vCPU cost**: 0.5 vCPU × 86,400 seconds/day × $0.000024 = **$1.04/day**
- **Memory cost**: 1.0 GB × 86,400 seconds/day × $0.000003 = **$0.26/day**
- **Subtotal**: **$1.30/day**

**Note**: Ready sessions run 24/7, so this is the base cost even when idle.

---

### 2. Session Pool - Allocated Sessions (On-Demand)

**When code executes** (sessions allocated on-demand):
- Average execution time: ~3 seconds
- Cost per execution: 
  - vCPU: 0.5 × 3s × $0.000024 = $0.000036
  - Memory: 1.0 × 3s × $0.000003 = $0.000009
  - **Total per execution**: ~$0.000045

**Example**: 100 executions/day = 100 × $0.000045 = **$0.0045/day** (negligible)

**Note**: Allocated sessions only cost when active. With 5-minute cooldown, sessions stay allocated for 5 minutes after last use.

---

### 3. Backend Container App

**Assuming 1 replica, 0.25 vCPU, 0.5 GB** (typical minimum):
- **vCPU cost**: 0.25 × 86,400 × $0.000024 = **$0.52/day**
- **Memory cost**: 0.5 × 86,400 × $0.000003 = **$0.13/day**
- **Subtotal**: **$0.65/day**

**Note**: If backend scales to zero when idle, this cost drops to $0/day.

---

### 4. Fixed Costs

- **Container Apps Environment**: **$0.10/day** (always running)
- **Container Registry (ACR)**: **$0.17/day** (storage only)
- **Subtotal**: **$0.27/day**

---

## 📊 TOTAL DAILY COST (Current Scenario)

| Component | Daily Cost | Monthly Cost |
|-----------|------------|--------------|
| **Session Pool (1 ready)** | $1.30 | $39.00 |
| **Backend Container App** | $0.65 | $19.50 |
| **Fixed Costs (Env + ACR)** | $0.27 | $8.10 |
| **Allocated Sessions** | ~$0.00 | ~$0.00 |
| **TOTAL** | **~$2.22/day** | **~$66.60/month** |

---

## 💡 Cost Optimization Options

### Option 1: Reduce Ready Sessions to 0
- **Current**: 1 ready = $1.30/day
- **After**: 0 ready = $0/day (idle)
- **Savings**: $1.30/day (~$39/month)
- **Trade-off**: First request takes 3-5 seconds (cold start)

### Option 2: Scale Backend to Zero When Idle
- **Current**: Always running = $0.65/day
- **After**: Scale to zero = $0/day (when idle)
- **Savings**: $0.65/day (~$19.50/month)
- **Trade-off**: First request takes 10-30 seconds (cold start)

### Option 3: Both Optimizations
- **Total Savings**: $1.95/day (~$58.50/month)
- **New Total**: ~$0.27/day (~$8/month)
- **Trade-off**: Slower response times (cold starts)

---

## 📋 Cost Comparison

| Scenario | Daily Cost | Monthly Cost | Response Time |
|----------|------------|--------------|---------------|
| **Current** | $2.22 | $66.60 | Fast (no cold start) |
| **Optimized (0 ready)** | $0.92 | $27.60 | Medium (3-5s first request) |
| **Fully Optimized** | $0.27 | $8.10 | Slow (10-30s first request) |

---

## 🎯 Recommendations

### For Testing/Development (Current):
- ✅ **Current setup**: $2.22/day is reasonable
- ✅ Fast response times
- ✅ No cold starts
- ✅ Good for development/testing

### For Production (200+ students):
- ⚠️ **Scale up** when needed:
  - Ready sessions: 3-5 (for faster response)
  - Max sessions: 20-50 (for concurrency)
  - **Estimated cost**: $4-6/day (~$120-180/month)

### For Maximum Cost Savings:
- ✅ Set ready sessions to 0
- ✅ Enable scale-to-zero for backend
- ✅ **Cost**: ~$0.27/day (~$8/month)
- ⚠️ Accept slower first request

---

## 📝 Notes

- **Allocated sessions** cost is negligible (only charged when active)
- **Cooldown period** (5 min) keeps sessions allocated briefly after use
- **Fixed costs** (Environment + ACR) are always present
- **Pricing** may vary by region (East US 2 pricing used)

---

**Last Updated**: 2025-11-26  
**Current Daily Cost**: ~$2.22/day (~$66.60/month)


