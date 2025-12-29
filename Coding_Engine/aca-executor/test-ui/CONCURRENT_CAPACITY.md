# Concurrent User Capacity Analysis (3 Replicas)

## 📊 Current Configuration

- **Replicas**: 3
- **CPU per replica**: 2.0 cores
- **Memory per replica**: 4GB
- **Total CPU**: 6 cores
- **Total Memory**: 12GB

---

## 🔍 Current Metrics per Execution

| Metric | Value | Notes |
|--------|-------|-------|
| CPU Usage | ~194% (97% per CPU) | Almost maxed out per execution |
| Memory | ~39 MB | Very low usage |
| Execution Time | ~1300-2000ms | Java compilation + execution |

---

## 💡 Capacity Calculations

### **Scenario 1: True Concurrent (All at Exact Same Time)**

**CPU Bottleneck Analysis:**
- Each execution uses ~194% CPU = ~97% per CPU core
- Each replica has 2 CPU cores
- **Per replica**: Can handle ~2 concurrent executions (CPU-limited)
- **With 3 replicas**: **6 concurrent executions maximum**

**Memory Bottleneck Analysis:**
- Each execution uses ~39 MB
- Each replica has 4GB = 4096 MB
- **Per replica**: 4096 / 39 = **~105 concurrent executions** (memory-limited)
- **With 3 replicas**: **~315 concurrent executions** (memory-limited)

**Verdict**: **CPU is the bottleneck** → **6 concurrent users maximum**

---

### **Scenario 2: Sequential Requests (Over Time)**

**Throughput Analysis:**
- Execution time: ~2 seconds per request
- Each replica can serve: 60 seconds / 2 seconds = **30 requests/minute**
- **With 3 replicas**: 3 × 30 = **90 requests/minute**
- **Per second**: 90 / 60 = **~1.5 requests/second**

**If requests come in over time (not all at once):**
- **200 users over 3.5 hours** = 200 / 210 minutes = **~0.95 requests/minute**
- **Capacity**: 90 requests/minute
- **Verdict**: ✅ **Easily handles 200 users** (only ~0.95 req/min needed)

---

## 🎯 **Answer: How Many Users Can Run Code at the Same Time?**

### **True Concurrent (Exact Same Moment):**
**6 users maximum** (CPU-limited)

- Each replica can handle 2 concurrent executions
- 3 replicas × 2 = **6 concurrent users**

### **Sequential (Over Time):**
**90 users per minute** (throughput)

- Each replica: 30 requests/minute
- 3 replicas: **90 requests/minute**
- For a 3.5-hour contest: **~18,900 requests total capacity**

---

## 📈 **Real-World Scenario: 200 Users Contest**

### **Contest Start (Peak Load):**
- **200 users** all start at once
- **Capacity**: 6 concurrent executions
- **What happens**:
  - First 6 users: Execute immediately
  - Remaining 194 users: **Queue and wait**
  - Each execution takes ~2 seconds
  - **Time to process all**: 200 / 6 × 2 = **~67 seconds** (1.1 minutes)

### **During Contest (Steady State):**
- Users submit at different times
- **Peak**: Maybe 20-30 users submit simultaneously
- **Capacity**: 6 concurrent
- **Queue time**: ~10-20 seconds (acceptable)

### **Recommendation for 200 Users:**
- ✅ **Current setup (3 replicas)**: Works, but may have queue delays at start
- ⚠️ **Better**: Increase to **5-10 replicas** for smoother experience
- 💡 **Auto-scaling**: Set `max_replicas=10` to handle peaks automatically

---

## 🔧 **Scaling Recommendations**

### **For Smooth 200-User Contest:**

| Scenario | Min Replicas | Max Replicas | Concurrent Capacity |
|----------|--------------|--------------|---------------------|
| **Current** | 3 | 3 | 6 users |
| **Recommended** | 5 | 10 | 10-20 users |
| **Optimal** | 10 | 20 | 20-40 users |

### **Cost vs Performance:**

- **3 replicas**: $0.36/hour = **$1.26 for 3.5-hour contest**
- **10 replicas**: $1.20/hour = **$4.20 for 3.5-hour contest**
- **20 replicas**: $2.40/hour = **$8.40 for 3.5-hour contest**

**Recommendation**: **5-10 replicas** for best balance (cost: $2.10-$4.20 per contest)

---

## ✅ **Summary**

### **Current Capacity (3 Replicas):**
- **True concurrent**: **6 users** (all at exact same time)
- **Throughput**: **90 users/minute** (sequential)
- **For 200 users**: ✅ Works, but may queue at contest start

### **For Production (200 Users):**
- **Recommended**: **5-10 replicas** (10-20 concurrent capacity)
- **Cost**: $2.10-$4.20 per 3.5-hour contest
- **Experience**: Smooth, minimal queuing

---

**Bottom Line**: With **3 replicas**, you can handle **6 users running code at the exact same time**. For a 200-user contest, consider scaling to **5-10 replicas** for better experience.


