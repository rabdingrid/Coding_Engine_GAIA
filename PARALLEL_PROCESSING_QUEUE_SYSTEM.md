# Parallel Processing, Queue System & Load Distribution

## 🎯 Overview

This document explains how the FastAPI code execution service handles **parallel processing**, **queue management**, and **load distribution** across multiple replicas in Azure Container Apps.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Container Apps                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Replica 1   │  │   Replica 2   │  │   Replica 3   │    │
│  │               │  │               │  │               │    │
│  │  Gunicorn     │  │  Gunicorn     │  │  Gunicorn     │    │
│  │  ┌─────────┐  │  │  ┌─────────┐  │  │  ┌─────────┐  │    │
│  │  │Worker 1 │  │  │  │Worker 1 │  │  │  │Worker 1 │  │    │
│  │  │Worker 2 │  │  │  │Worker 2 │  │  │  │Worker 2 │  │    │
│  │  │Worker 3 │  │  │  │Worker 3 │  │  │  │Worker 3 │  │    │
│  │  │Worker 4 │  │  │  │Worker 4 │  │  │  │Worker 4 │  │    │
│  │  └─────────┘  │  │  └─────────┘  │  │  └─────────┘  │    │
│  │  2 threads    │  │  2 threads    │  │  2 threads    │    │
│  │  per worker   │  │  per worker   │  │  per worker   │    │
│  │               │  │               │  │               │    │
│  │  Capacity: 8  │  │  Capacity: 8  │  │  Capacity: 8  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Load Balancer (Azure Container Apps)          │  │
│  │         Distributes requests across replicas          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
                    HTTP Requests
                    (20 questions)
```

---

## ⚙️ Parallel Processing Model

### **1. Multi-Level Concurrency**

#### **Level 1: Replica Level (Horizontal Scaling)**
- **Multiple Replicas**: 1-3 replicas (configurable)
- **Load Balancing**: Azure Container Apps automatically distributes requests
- **Auto-Scaling**: Replicas scale up/down based on load

#### **Level 2: Worker Level (Process-Based)**
- **Gunicorn Workers**: 4 worker processes per replica
- **Process Isolation**: Each worker is a separate process
- **Memory Isolation**: Each worker has its own memory space

#### **Level 3: Thread Level (Thread-Based)**
- **Threads per Worker**: 2 threads per worker
- **Thread Pool**: Each worker can handle 2 concurrent requests
- **Shared Memory**: Threads share worker's memory space

### **2. Total Concurrent Capacity**

**Per Replica:**
```
4 workers × 2 threads = 8 concurrent requests per replica
```

**Total System (3 replicas):**
```
3 replicas × 8 concurrent = 24 concurrent requests
```

**With Queue:**
```
24 concurrent + 200 queue backlog = 224 total capacity
```

---

## 📊 Queue System Architecture

### **Gunicorn Queue System**

```
Request Flow:
┌──────────┐
│  Client  │
└────┬─────┘
     │ HTTP Request
     ▼
┌─────────────────────────────────────┐
│   Azure Load Balancer               │
│   (Routes to available replica)     │
└────┬────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│   Gunicorn Master Process           │
│   ┌─────────────────────────────┐  │
│   │  Request Queue (backlog:200) │  │
│   └─────────────────────────────┘  │
│            │                         │
│   ┌────────┴────────┐                │
│   ▼                 ▼                │
│  Worker 1         Worker 2           │
│  ┌──────┐         ┌──────┐           │
│  │Thread│         │Thread│           │
│  │Thread│         │Thread│           │
│  └──────┘         └──────┘           │
└─────────────────────────────────────┘
```

### **Queue Behavior**

1. **Request Arrival**: HTTP request arrives at Gunicorn master
2. **Queue Check**: Master checks if any worker thread is available
3. **Immediate Processing**: If worker available → process immediately
4. **Queue Wait**: If all workers busy → add to queue (max 200)
5. **Queue Processing**: Workers pull from queue when available
6. **Queue Full**: If queue full (200) → HTTP 503 Service Unavailable

### **Queue Configuration**

```dockerfile
# In Dockerfile.fastapi
CMD ["gunicorn", "executor-service:app",
     "--workers", "4",           # 4 worker processes
     "--threads", "2",           # 2 threads per worker
     "--backlog", "200",         # Queue size
     "--timeout", "300"]         # Request timeout (5 minutes)
```

---

## 🔄 Load Distribution

### **1. Request Distribution**

#### **Azure Container Apps Load Balancer**
- **Round-Robin**: Distributes requests evenly across replicas
- **Health-Aware**: Routes to healthy replicas only
- **Auto-Scaling**: Creates new replicas when load increases

#### **Example: 20 Requests with 1 Replica**

```
Request Flow:
R1 → Replica 1 → Worker 1 → Thread 1 → Process
R2 → Replica 1 → Worker 1 → Thread 2 → Process
R3 → Replica 1 → Worker 2 → Thread 1 → Process
R4 → Replica 1 → Worker 2 → Thread 2 → Process
R5 → Replica 1 → Worker 3 → Thread 1 → Process
R6 → Replica 1 → Worker 3 → Thread 2 → Process
R7 → Replica 1 → Worker 4 → Thread 1 → Process
R8 → Replica 1 → Worker 4 → Thread 2 → Process
R9 → Replica 1 → Queue → Wait for available worker
R10 → Replica 1 → Queue → Wait for available worker
...
R20 → Replica 1 → Queue → Wait for available worker
```

**Timeline:**
- **R1-R8**: Processed immediately (8 concurrent)
- **R9-R20**: Queued, processed as workers become available
- **Total Time**: ~2-3 minutes for all 20 requests

### **2. Execution Time Distribution**

**Per Request (10 test cases):**
- Test case execution: ~2-3 seconds each
- Sequential execution: 10 × 2.5s = **~25 seconds per request**
- With overhead: **~30 seconds per request**

**With 8 Concurrent Workers:**
- First 8 requests: Start immediately
- Next 8 requests: Queue, start after ~30 seconds
- Remaining 4 requests: Queue, start after ~60 seconds

**Total Time for 20 Requests:**
```
Time 0s:    R1-R8 start (8 concurrent)
Time 30s:   R1-R8 finish, R9-R16 start
Time 60s:   R9-R16 finish, R17-R20 start
Time 90s:   R17-R20 finish
```

### **3. Replica Distribution (Multi-Replica Scenario)**

**With 3 Replicas:**

```
Replica 1: R1, R4, R7, R10, R13, R16, R19  (7 requests)
Replica 2: R2, R5, R8, R11, R14, R17, R20  (7 requests)
Replica 3: R3, R6, R9, R12, R15, R18       (6 requests)
```

**Load Balancing:**
- Azure automatically distributes requests
- Each replica handles ~6-7 requests
- All replicas process concurrently
- **Total Time**: ~30 seconds (all finish together)

---

## 📈 Performance Characteristics

### **1. Single Replica (Ready State = 1)**

**Capacity:**
- Concurrent: 8 requests
- Queue: 200 requests
- Total: 208 requests

**Performance:**
- **20 requests**: ~90 seconds (sequential queue processing)
- **50 requests**: ~3-4 minutes
- **200 requests**: ~12-15 minutes

**Use Case:**
- Cost-optimized for low traffic
- Suitable for testing and development
- Can handle bursts with queue

### **2. Multiple Replicas (Ready State = 3)**

**Capacity:**
- Concurrent: 24 requests (3 × 8)
- Queue: 200 requests per replica
- Total: 624 requests

**Performance:**
- **20 requests**: ~30 seconds (parallel processing)
- **50 requests**: ~60-90 seconds
- **200 requests**: ~3-4 minutes

**Use Case:**
- Production workloads
- High traffic scenarios
- Contest/assessment environments

---

## 🔍 Queue System Details

### **Queue States**

1. **Empty Queue**: All workers available, immediate processing
2. **Partial Queue**: Some workers busy, queue building
3. **Full Queue**: All workers busy, queue at capacity (200)
4. **Overflow**: Queue full + new requests → HTTP 503

### **Queue Processing**

```python
# Simplified queue behavior
while True:
    request = queue.get()  # Blocking wait
    worker = get_available_worker()
    if worker:
        process_request(request)
    else:
        queue.put(request)  # Re-queue if no worker
```

### **Queue Metrics**

- **Queue Length**: Number of requests waiting
- **Wait Time**: Time request spends in queue
- **Throughput**: Requests processed per second
- **Queue Utilization**: Queue length / Max queue size

---

## 🧪 Test Scenario: 20 Questions, 1 Replica

### **Test Configuration**
- **Questions**: 20 DSA questions
- **Test Cases per Question**: 10
- **Total Test Cases**: 200
- **Replicas**: 1 (ready state)
- **Concurrent Capacity**: 8 requests

### **Expected Behavior**

**Phase 1: Immediate Processing (0-30s)**
```
R1-R8: Start immediately, process in parallel
Status: 8 concurrent executions
Queue: Empty
```

**Phase 2: Queue Processing (30-60s)**
```
R1-R8: Complete
R9-R16: Start processing
Status: 8 concurrent executions
Queue: R17-R20 waiting
```

**Phase 3: Final Processing (60-90s)**
```
R9-R16: Complete
R17-R20: Start processing
Status: 4 concurrent executions
Queue: Empty
```

**Phase 4: Completion (90s)**
```
R17-R20: Complete
All requests finished
```

### **Metrics to Observe**

1. **Total Duration**: ~90 seconds
2. **Average Wait Time**: ~15-30 seconds
3. **Queue Utilization**: Peak at 12 requests (20 - 8)
4. **Throughput**: ~0.22 requests/second
5. **Replica Utilization**: 100% (all workers busy)

---

## 📊 Load Distribution Patterns

### **Pattern 1: Uniform Load**

```
Time: 0s    10s    20s    30s    40s    50s
R1:  [████████████████████████]
R2:  [████████████████████████]
R3:  [████████████████████████]
R4:  [████████████████████████]
R5:  [████████████████████████]
R6:  [████████████████████████]
R7:  [████████████████████████]
R8:  [████████████████████████]
R9:           [████████████████████████]
R10:          [████████████████████████]
```

### **Pattern 2: Burst Load**

```
Time: 0s    10s    20s    30s    40s    50s
R1-R20: [████████████████████████]
        All arrive at once
        R1-R8: Immediate
        R9-R20: Queue
```

### **Pattern 3: Staggered Load**

```
Time: 0s    10s    20s    30s    40s    50s
R1:  [████████████████████████]
R2:     [████████████████████████]
R3:        [████████████████████████]
R4:           [████████████████████████]
```

---

## 🎯 Optimization Strategies

### **1. Increase Workers**

```dockerfile
--workers 6  # Instead of 4
```
- **Capacity**: 6 × 2 = 12 concurrent per replica
- **Total**: 3 × 12 = 36 concurrent
- **Trade-off**: Higher memory usage

### **2. Increase Threads**

```dockerfile
--threads 4  # Instead of 2
```
- **Capacity**: 4 × 4 = 16 concurrent per replica
- **Total**: 3 × 16 = 48 concurrent
- **Trade-off**: Python GIL limitations

### **3. Increase Replicas**

```hcl
max_replicas = 5  # In terraform/variables.tf
```
- **Capacity**: 5 × 8 = 40 concurrent
- **Trade-off**: Higher cost

### **4. Increase Queue Size**

```dockerfile
--backlog 500  # Instead of 200
```
- **Capacity**: 500 requests in queue
- **Trade-off**: Higher memory usage, longer wait times

---

## 📈 Monitoring & Metrics

### **Key Metrics to Monitor**

1. **Queue Length**: Number of requests waiting
2. **Wait Time**: Average time in queue
3. **Throughput**: Requests/second
4. **Error Rate**: HTTP 503 errors
5. **Replica Count**: Active replicas
6. **CPU Usage**: Per replica
7. **Memory Usage**: Per replica

### **Azure Container Apps Metrics**

```bash
# View replica count
az containerapp show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --query "properties.template.scale"

# View logs
az containerapp logs show \
  --name ai-ta-ra-code-executor2 \
  --resource-group ai-ta-2 \
  --follow
```

---

## 🚨 Troubleshooting

### **Issue: High Queue Length**

**Symptoms:**
- Requests waiting > 30 seconds
- Queue length > 50

**Solutions:**
1. Increase replicas: `max_replicas = 5`
2. Increase workers: `--workers 6`
3. Optimize code execution time

### **Issue: HTTP 503 Errors**

**Symptoms:**
- Queue full (200 requests)
- All workers busy

**Solutions:**
1. Increase queue size: `--backlog 500`
2. Add more replicas
3. Implement client-side retry with backoff

### **Issue: Slow Processing**

**Symptoms:**
- Execution time > 60 seconds per request
- Low throughput

**Solutions:**
1. Check test case complexity
2. Optimize code execution
3. Increase workers/replicas
4. Check for resource limits (CPU/Memory)

---

## 📝 Summary

### **Queue System Benefits**

✅ **Handles Bursts**: Queue absorbs traffic spikes  
✅ **Prevents Overload**: Protects workers from overwhelming  
✅ **Graceful Degradation**: Queues instead of failing  
✅ **Auto-Scaling**: Replicas scale based on queue length  

### **Load Distribution Benefits**

✅ **High Availability**: Multiple replicas  
✅ **Load Balancing**: Even distribution  
✅ **Fault Tolerance**: One replica failure doesn't stop service  
✅ **Scalability**: Add replicas for more capacity  

### **Current Configuration (1 Replica)**

- **Concurrent**: 8 requests
- **Queue**: 200 requests
- **Suitable For**: Testing, low traffic, cost optimization
- **20 Questions**: ~90 seconds total

### **Recommended Configuration (3 Replicas)**

- **Concurrent**: 24 requests
- **Queue**: 600 requests (200 × 3)
- **Suitable For**: Production, contests, high traffic
- **20 Questions**: ~30 seconds total

---

**Last Updated**: December 2024  
**Version**: 3.0.0 (FastAPI)




