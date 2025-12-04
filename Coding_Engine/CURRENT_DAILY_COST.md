# Current Daily Cost Analysis

## 📊 Current Configuration

### Backend Container App
- **Name**: `ai-ta-ra-coding-engine`
- **Status**: Running
- **CPU**: Checking...
- **Memory**: Checking...
- **Replicas**: Checking...

### Session Pool
- **Name**: `ai-ta-ra-session-pool`
- **Status**: Running
- **Ready Sessions**: 1
- **Max Sessions**: 5
- **CPU per Session**: 0.5 vCPU
- **Memory per Session**: 1.0 Gi
- **Cooldown Period**: 300 seconds (5 minutes)

---

## 💰 Azure Container Apps Pricing (as of 2024)

### Base Pricing:
- **vCPU**: ~$0.000012 per vCPU-second
- **Memory**: ~$0.0000015 per GB-second
- **Environment**: ~$0.10/day (fixed)

### Session Pool Specific:
- Sessions are billed based on:
  - **Ready sessions** (always running)
  - **Allocated sessions** (when in use)
  - CPU and memory consumed

---

## 💵 Daily Cost Calculation

### Backend Container App:
**Formula**: (vCPU × vCPU_rate × seconds) + (Memory_GB × Memory_rate × seconds)

**Per Day** (assuming 1 replica, 0.5 vCPU, 1.0 Gi):
- vCPU cost: 0.5 × $0.000012 × 86,400 seconds = **$0.5184/day**
- Memory cost: 1.0 × $0.0000015 × 86,400 seconds = **$0.1296/day**
- **Total Backend**: ~**$0.65/day** (~$19.50/month)

### Session Pool:
**Ready Sessions** (1 session always running):
- vCPU cost: 0.5 × $0.000012 × 86,400 = **$0.5184/day**
- Memory cost: 1.0 × $0.0000015 × 86,400 = **$0.1296/day**
- **Per Ready Session**: ~**$0.65/day**

**Allocated Sessions** (only when in use):
- Same cost as ready sessions, but only charged when active
- With cooldown of 5 minutes, sessions stay allocated for 5 min after last use

**Total Session Pool** (1 ready session):
- **~$0.65/day** (~$19.50/month)

### Container Apps Environment:
- **Fixed cost**: ~**$0.10/day** (~$3/month)

### Container Registry (ACR):
- **Storage**: ~$0.17/day (for images)
- **No compute cost** (just storage)

---

## 📊 Total Daily Cost (Current Scenario)

| Component | Daily Cost | Monthly Cost |
|-----------|------------|--------------|
| **Backend Container App** | ~$0.65 | ~$19.50 |
| **Session Pool (1 ready)** | ~$0.65 | ~$19.50 |
| **Container Apps Environment** | ~$0.10 | ~$3.00 |
| **Container Registry (ACR)** | ~$0.17 | ~$5.10 |
| **TOTAL** | **~$1.57/day** | **~$47/month** |

---

## 💡 Cost Optimization Options

### Option 1: Reduce Ready Sessions to 0
- **Current**: 1 ready session = $0.65/day
- **After**: 0 ready sessions = $0/day (idle)
- **Savings**: $0.65/day (~$19.50/month)
- **Trade-off**: First request takes 3-5 seconds (cold start)

### Option 2: Scale Backend to Zero When Idle
- **Current**: Always running = $0.65/day
- **After**: Scale to zero = $0/day (when idle)
- **Savings**: $0.65/day (~$19.50/month)
- **Trade-off**: First request takes 10-30 seconds (cold start)

### Option 3: Both Optimizations
- **Total Savings**: $1.30/day (~$39/month)
- **New Total**: ~$0.27/day (~$8/month)
- **Trade-off**: Slower response times (cold starts)

---

## 📋 Current vs Optimized

| Scenario | Daily Cost | Monthly Cost | Notes |
|----------|------------|--------------|-------|
| **Current** | $1.57 | $47 | 1 ready session, backend always on |
| **Optimized** | $0.27 | $8 | 0 ready sessions, backend scale-to-zero |
| **Savings** | $1.30 | $39 | 83% cost reduction |

---

## 🎯 Recommendations

### For Testing/Development:
- ✅ **Current setup is fine** ($1.57/day)
- ✅ Fast response times
- ✅ No cold starts

### For Production (200+ students):
- ⚠️ **Scale up** when needed:
  - Ready sessions: 2-3 (for faster response)
  - Max sessions: 10-20 (for concurrency)
  - **Estimated cost**: $2-3/day (~$60-90/month)

### For Cost Savings:
- ✅ Set ready sessions to 0
- ✅ Enable scale-to-zero for backend
- ✅ **Cost**: ~$0.27/day (~$8/month)

---

**Last Updated**: 2025-11-26  
**Status**: Current configuration costs ~$1.57/day


