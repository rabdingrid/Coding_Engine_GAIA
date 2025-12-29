# Daily Cost Summary - Current Scenario

## 💰 Total Daily Cost: **$2.22/day** (~$66.60/month)

---

## 📊 Cost Breakdown

### 1. Session Pool - Ready Sessions
- **1 Ready Session** (always running)
  - CPU: 0.5 vCPU × 86,400 seconds × $0.000024 = **$1.04/day**
  - Memory: 1.0 GB × 86,400 seconds × $0.000003 = **$0.26/day**
  - **Subtotal**: **$1.30/day** (~$39/month)

### 2. Backend Container App
- **1 Replica** (assuming 0.25 vCPU, 0.5 GB)
  - CPU: 0.25 × 86,400 × $0.000024 = **$0.52/day**
  - Memory: 0.5 × 86,400 × $0.000003 = **$0.13/day**
  - **Subtotal**: **$0.65/day** (~$19.50/month)

### 3. Fixed Costs
- **Container Apps Environment**: $0.10/day (~$3/month)
- **Container Registry (ACR)**: $0.17/day (~$5.10/month)
- **Subtotal**: **$0.27/day** (~$8.10/month)

### 4. Allocated Sessions (On-Demand)
- **Cost per execution**: ~$0.000045 (negligible)
- **100 executions/day**: ~$0.0045/day
- **Subtotal**: **~$0.00/day** (negligible)

---

## 📋 Summary Table

| Component | Daily Cost | Monthly Cost |
|-----------|------------|--------------|
| **Session Pool (1 ready)** | $1.30 | $39.00 |
| **Backend Container App** | $0.65 | $19.50 |
| **Fixed Costs** | $0.27 | $8.10 |
| **Allocated Sessions** | ~$0.00 | ~$0.00 |
| **TOTAL** | **$2.22** | **$66.60** |

---

## 💡 Cost Optimization

### If You Set Ready Sessions to 0:
- **Savings**: $1.30/day (~$39/month)
- **New Total**: $0.92/day (~$27.60/month)
- **Trade-off**: 3-5 second cold start on first request

### If You Scale Backend to Zero:
- **Savings**: $0.65/day (~$19.50/month)
- **New Total**: $1.57/day (~$47/month)
- **Trade-off**: 10-30 second cold start on first request

### If You Do Both:
- **Savings**: $1.95/day (~$58.50/month)
- **New Total**: $0.27/day (~$8/month)
- **Trade-off**: Slower response times

---

## 🎯 Current Configuration

- **Session Pool**: 1 ready session, max 5 concurrent
- **Backend**: 1 replica (always running)
- **Status**: Optimized for performance (fast response, no cold starts)
- **Cost**: $2.22/day is reasonable for testing/development

---

**Last Updated**: 2025-11-26  
**Current Daily Cost**: **$2.22/day** (~$66.60/month)


