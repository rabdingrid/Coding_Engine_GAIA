# Azure Container Apps Architecture - Explained Simply

## 🏗️ Basic Concepts

### **Container App vs Replicas vs Containers**

```
┌─────────────────────────────────────────┐
│     ONE Container App                    │
│     (ai-ta-ra-code-executor2)           │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  │ Replica 1│  │ Replica 2│  │ Replica 3│  ← Multiple Replicas (Containers)
│  │          │  │          │  │          │
│  │ Handles  │  │ Handles  │  │ Handles  │
│  │ Multiple│  │ Multiple │  │ Multiple │
│  │ Requests│  │ Requests │  │ Requests │
│  └──────────┘  └──────────┘  └──────────┘
└─────────────────────────────────────────┘
```

**Key Points:**
- **1 Container App** = Your service (like `ai-ta-ra-code-executor2`)
- **Multiple Replicas** = Multiple containers running the same service
- **Each Replica** = One container that can handle **multiple concurrent requests**

---

## 📊 How Many Requests Per Replica?

### **Each Replica Can Handle Multiple Requests Simultaneously**

**Current Configuration:**
- **CPU**: 1.0 core per replica
- **Memory**: 2.0 GiB per replica
- **Execution Time**: 2-5 seconds per execution

**Capacity Per Replica:**
- **Concurrent Executions**: 2-5 at a time (depending on language)
- **Throughput**: ~12-30 executions per minute per replica

**Example:**
```
Replica 1: Handles Request A, B, C simultaneously
           ↓
           Request A finishes → Handles Request D
           Request B finishes → Handles Request E
           Request C finishes → Handles Request F
```

---

## 🎯 For 200 Students × 2 Questions = 400 Executions

### **Scenario 1: All Students Submit at Once (Burst Traffic)**

**Peak Concurrent Requests**: 200 students × 2 questions = **400 concurrent executions**

**Required Replicas:**
```
400 concurrent executions ÷ 5 executions per replica = 80 replicas
```

**But wait!** Azure Container Apps limit: **300 replicas per Container App** ✅

**Answer**: **ONE Container App with 80-100 replicas** is enough!

---

### **Scenario 2: Gradual Submission (Realistic)**

**Assumptions:**
- Students submit over 5-minute window
- Peak: 50-100 concurrent requests
- Average: 20-40 concurrent requests

**Required Replicas:**
```
Peak (100 concurrent) ÷ 5 per replica = 20 replicas
Average (40 concurrent) ÷ 5 per replica = 8 replicas
```

**Answer**: **ONE Container App with 20-50 replicas** is enough!

---

## 💰 Cost Calculation

### **Per Replica Cost:**
- **CPU**: 1.0 core × $0.000012 per vCPU-second
- **Memory**: 2.0 GiB × $0.0000015 per GiB-second
- **Total per replica**: ~$0.000012 per second

### **Cost for 200 Students Contest (2 hours):**

#### **Option 1: Pre-warmed Pool (10 replicas) + Auto-scale to 100**
```
Pre-warmed (10 replicas × 2 hours):
  10 × $0.000012/sec × 7200 sec = $0.864

Peak (100 replicas × 30 minutes):
  100 × $0.000012/sec × 1800 sec = $2.16

Average (50 replicas × 1.5 hours):
  50 × $0.000012/sec × 5400 sec = $3.24

Total: ~$6-7 for 2-hour contest
```

#### **Option 2: Minimal Pre-warm (5 replicas) + Auto-scale to 80**
```
Pre-warmed (5 replicas × 2 hours):
  5 × $0.000012/sec × 7200 sec = $0.432

Peak (80 replicas × 30 minutes):
  80 × $0.000012/sec × 1800 sec = $1.728

Average (40 replicas × 1.5 hours):
  40 × $0.000012/sec × 5400 sec = $2.592

Total: ~$4-5 for 2-hour contest
```

---

## ✅ Final Answer

### **How Many Container Apps?**
**Answer: ONE Container App** ✅

### **How Many Replicas?**
**Answer: 20-100 replicas** (auto-scales based on demand)

### **Configuration:**
```terraform
min_replicas = 10   # Pre-warmed for contest start
max_replicas = 100  # Can scale up to handle burst
```

### **Cost:**
**Answer: $4-7 for 2-hour contest** (200 students × 2 questions)

---

## 🔄 How It Works

### **Request Flow:**
```
Student 1 submits Question 1
    ↓
Load Balancer (Azure)
    ↓
Available Replica (e.g., Replica 5)
    ↓
Replica 5 executes code (2-5 seconds)
    ↓
Returns result
    ↓
Replica 5 ready for next request
```

### **Auto-Scaling:**
```
Contest Starts (10:00 AM)
    ↓
10 replicas (pre-warmed)
    ↓
Students start submitting
    ↓
Azure detects high load
    ↓
Auto-scales to 50 replicas (10:05 AM)
    ↓
Peak traffic (10:15 AM)
    ↓
Auto-scales to 100 replicas (10:15 AM)
    ↓
Traffic decreases (10:30 AM)
    ↓
Auto-scales down to 20 replicas (10:30 AM)
    ↓
Contest ends (12:00 PM)
    ↓
Auto-scales down to 10 replicas (12:00 PM)
```

---

## 📋 Summary Table

| Metric | Value |
|-------|-------|
| **Container Apps Needed** | **1** |
| **Min Replicas** | 10 (pre-warmed) |
| **Max Replicas** | 100 (handles burst) |
| **Replicas Per Request** | **NOT 1:1** - Each replica handles multiple requests |
| **Concurrent Capacity** | 200-500 executions (100 replicas × 2-5 each) |
| **Total Executions** | 400 (200 students × 2 questions) |
| **Cost (2 hours)** | **$4-7** |

---

## ✅ Key Takeaways

1. **ONE Container App** is enough for 200 students
2. **Replicas are shared** - not one per user
3. **Each replica handles multiple requests** simultaneously
4. **Auto-scaling** handles traffic spikes automatically
5. **Cost is low** - $4-7 for entire contest

---

## 🚀 Ready to Deploy?

**Current Configuration:**
- ✅ Already set to `max_replicas = 100`
- ✅ Already set to `min_replicas = 10`
- ✅ Auto-scaling enabled
- ✅ Security enabled

**Just run:**
```bash
cd terraform
terraform apply
```

**That's it!** One Container App will handle all 200 students smoothly.


