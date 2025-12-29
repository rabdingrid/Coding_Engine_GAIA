# Azure Session Pool Cost Analysis

## 💰 Cost Breakdown

### **Resource Pricing (East US 2)**

| Resource | Unit | Cost |
|----------|------|------|
| **vCPU** | Per vCPU-second | $0.000024 |
| **Memory** | Per GB-second | $0.000003 |
| **Container Apps Environment** | Per day | $0.10 (fixed) |
| **ACR (Basic)** | Per day | $0.17 (fixed) |
| **Session Pool Overhead** | Per hour | ~$0.15 |

---

## 📊 Testing Configuration (Minimum Cost)

### **Current Test Setup**
```bash
--max-sessions 5              # Maximum 5 concurrent sessions
--ready-sessions 1            # 1 always-ready session (minimum required)
--cooldown-period 300         # 5 minutes (minimum allowed)
--cpu 0.5 --memory 1.0Gi     # Per session resources
```

### **Daily Cost Calculation**

#### **When IDLE (no requests)**
- **1 Ready Session** (always running):
  - vCPU: 0.5 × 86,400 seconds × $0.000024 = **$1.04/day**
  - Memory: 1 GB × 86,400 seconds × $0.000003 = **$0.26/day**
  - Session overhead: ~$0.15/hour × 24 = **$3.60/day**
  - **Subtotal: $4.90/day**

- **Fixed Costs**:
  - Container Apps Environment: **$0.10/day**
  - ACR: **$0.17/day**
  - **Subtotal: $0.27/day**

- **Backend Container App** (1 replica, idle):
  - vCPU: 0.25 × 86,400 × $0.000024 = **$0.52/day**
  - Memory: 0.5 GB × 86,400 × $0.000003 = **$0.13/day**
  - **Subtotal: $0.65/day**

**TOTAL IDLE COST: ~$5.82/day** ($174/month)

---

#### **When ACTIVE (with code execution)**
- **Ready Session**: $4.90/day (same as idle)
- **Active Sessions** (on-demand, per execution):
  - Average execution time: 3 seconds
  - Cost per execution: 0.5 vCPU × 3s × $0.000024 + 1GB × 3s × $0.000003 = **$0.00004** per execution
  - 100 executions/day: 100 × $0.00004 = **$0.004/day** (negligible)

- **Fixed Costs**: $0.27/day (same)
- **Backend**: $0.65/day (same)

**TOTAL ACTIVE COST: ~$5.82/day** (execution cost is negligible)

---

## 🎯 Contest Configuration (200+ Students)

### **Contest Setup**
```bash
--max-sessions 50             # Maximum 50 concurrent sessions
--ready-sessions 5            # 5 always-ready sessions
--cooldown-period 300         # 5 minutes
--cpu 0.5 --memory 1.0Gi     # Per session resources
```

### **Contest Cost (2-hour contest)**

#### **Ready Sessions (5 sessions, 2 hours)**
- vCPU: 5 × 0.5 × 7,200 seconds × $0.000024 = **$0.43**
- Memory: 5 × 1 GB × 7,200 seconds × $0.000003 = **$0.11**
- Session overhead: 5 × $0.15/hour × 2 hours = **$1.50**
- **Subtotal: $2.04**

#### **Active Sessions (on-demand, 2 hours)**
- Average: 30 active sessions during peak
- Average execution: 3 seconds
- Total executions: ~200 students × 10 submissions = 2,000 executions
- Cost: 2,000 × $0.00004 = **$0.08**

#### **Backend Scaling (2-10 replicas, 2 hours)**
- Average: 5 replicas
- vCPU: 5 × 0.25 × 7,200 × $0.000024 = **$0.22**
- Memory: 5 × 0.5 GB × 7,200 × $0.000003 = **$0.05**
- **Subtotal: $0.27**

**TOTAL CONTEST COST: ~$2.39 for 2-hour contest**

---

## 💡 Cost Optimization Strategies

### **1. Testing Phase (Current)**
✅ **Recommended**: Use minimum configuration
- `max-sessions: 5`
- `ready-sessions: 1` (minimum required)
- **Cost: ~$5.82/day** when running

### **2. Idle/Development Phase**
✅ **Recommended**: Scale to zero or delete
- Delete session pool when not in use
- Scale backend to 0 replicas
- **Cost: $0.27/day** (only ACR + Environment)

### **3. Contest Phase**
✅ **Recommended**: Scale up 30 minutes before, scale down after
- Scale up: `max-sessions: 50`, `ready-sessions: 5`
- Run contest: **$2.39 for 2 hours**
- Scale down immediately after: Back to $0.27/day

### **4. Production (24/7)**
⚠️ **Expensive**: Not recommended for testing
- `max-sessions: 20`
- `ready-sessions: 2`
- **Cost: ~$12-15/day** ($360-450/month)

---

## 📈 Cost Comparison

| Scenario | Configuration | Daily Cost | Monthly Cost |
|----------|--------------|------------|--------------|
| **Stopped** | All resources stopped | $0.27 | $8 |
| **Testing (Min)** | max: 5, ready: 1 | $5.82 | $174 |
| **Contest (2h)** | max: 50, ready: 5 | $2.39 | N/A (one-time) |
| **Production** | max: 20, ready: 2 | $12-15 | $360-450 |

---

## 🎯 Recommendations

### **For Testing Phase:**
1. ✅ Use minimum configuration: `max-sessions: 5`, `ready-sessions: 1`
2. ✅ **Stop/delete resources when not actively testing** to save costs
3. ✅ Use `ready-sessions: 0` if possible (but Azure requires minimum 1)

### **For Contest:**
1. ✅ Scale up 30 minutes before contest starts
2. ✅ Use `max-sessions: 50`, `ready-sessions: 5` for 200 students
3. ✅ **Scale down immediately after contest ends**
4. ✅ Expected cost: **~$2-3 per contest**

### **Cost Savings Tips:**
- ❌ **Never leave `ready-sessions > 0` when idle** (costs $4.90/day per session)
- ✅ **Delete session pool when not in use** (saves $5.82/day)
- ✅ **Scale backend to 0 replicas when idle** (saves $0.65/day)
- ✅ **Use cooldown period effectively** (300s minimum, keeps sessions warm)

---

## 📊 Execution Cost Breakdown

### **Per Code Execution:**
- **Cold Start** (first request, no ready session):
  - Session creation: 3-5 seconds
  - Cost: ~$0.0001 per cold start
  
- **Warm Execution** (session ready):
  - Execution time: 1-3 seconds
  - Cost: ~$0.00004 per execution

### **Cost per 1000 Executions:**
- With ready sessions: **$0.04** (warm)
- Without ready sessions: **$0.10** (cold starts included)

**Conclusion**: Execution cost is negligible. The main cost is **ready sessions running 24/7**.

---

## ⚠️ Important Notes

1. **Ready Sessions = Always Running = Always Costing Money**
   - `ready-sessions: 1` = $4.90/day even with 0 requests
   - `ready-sessions: 5` = $24.50/day even with 0 requests

2. **Azure Minimum Requirements**:
   - `ready-sessions` must be > 0 (minimum 1)
   - `cooldown-period` must be >= 300 seconds (5 minutes)
   - Cannot set `ready-sessions: 0` (Azure limitation)

3. **Best Practice for Testing**:
   - Deploy only when actively testing
   - Delete session pool when done
   - Recreate before next test session

---

**Last Updated**: December 2024  
**Region**: East US 2  
**Currency**: USD


