# Scalability & Security Analysis for 200 Students Contest

## 📊 Current Configuration

### Container Resources (Per Replica)
- **CPU**: 1.0 core
- **Memory**: 2.0 GiB
- **Min Replicas**: 1 (always running)
- **Max Replicas**: 10 (current limit for 5 users)

### Execution Characteristics
- **Average execution time**: 2-5 seconds per test case
- **Concurrent capacity**: ~2-5 executions per container (depending on language)
- **Total capacity (10 replicas)**: ~20-50 concurrent executions

---

## 🎯 Contest Requirements: 200 Students × 2 Questions = 400 Executions

### Load Analysis

**Scenario 1: Sequential Execution (Worst Case)**
- 400 executions × 3 seconds average = 1,200 seconds = **20 minutes**
- With 10 replicas: **2 minutes** (if perfectly distributed)

**Scenario 2: Concurrent Execution (Realistic)**
- Students submit within 5-minute window
- Peak concurrent requests: ~50-100 students
- Required replicas: **20-50 containers**

**Scenario 3: Burst Traffic (Contest Start)**
- All 200 students start simultaneously
- Required replicas: **50-100 containers** (for 2-4 seconds per execution)

---

## ✅ Scalability Answer: **YES, BUT NEEDS CONFIGURATION UPDATE**

### Required Changes for 200 Students:

```terraform
min_replicas = 5      # Pre-warmed pool for contest start
max_replicas = 100    # Scale up to handle burst traffic
```

### Cost Estimate (200 Students Contest):
- **Pre-warmed (5 replicas)**: 5 × $0.000012/vCPU-sec × 3600 = $0.216/hour
- **Peak (100 replicas)**: 100 × $0.000012/vCPU-sec × 3600 = $4.32/hour
- **Average (50 replicas)**: 50 × $0.000012/vCPU-sec × 3600 = $2.16/hour
- **Contest duration (2 hours)**: ~$4-8 total

---

## 🔄 Container Allocation Model

### **Containers are REUSED, NOT one per user**

**How Azure Container Apps Works:**
1. **Shared Pool**: Containers are shared across all requests
2. **Load Balancing**: Requests are distributed across available replicas
3. **Auto-scaling**: Replicas scale up/down based on demand
4. **Request Isolation**: Each execution runs in a **separate subprocess** with:
   - Isolated temporary directory (`/tmp/exec_*`)
   - Resource limits (CPU, memory, processes)
   - Network isolation
   - Code sanitization

### Execution Flow:
```
User Request → Load Balancer → Available Container → Subprocess Execution → Response
                ↓
         (Container Reused for Next Request)
```

### Isolation Guarantees:
✅ **Code Isolation**: Each execution runs in separate subprocess  
✅ **Filesystem Isolation**: Temporary directories cleaned after execution  
✅ **Resource Limits**: CPU, memory, processes limited per execution  
✅ **Network Isolation**: No outbound network access  
✅ **Time Limits**: 5-10 second timeout per execution  

---

## 🔒 Security Analysis for Contest

### ✅ **SAFE ENOUGH** - Multiple Layers of Protection

#### 1. **Code Sanitization** ✅
- Blocks dangerous imports (`os`, `subprocess`, `sys`)
- Blocks `eval()`, `exec()`, `compile()`
- Blocks file write operations
- Blocks network operations

#### 2. **Network Isolation** ✅
- Socket creation blocked during execution
- No outbound HTTP/HTTPS requests
- No DNS resolution

#### 3. **Resource Limits** ✅
- CPU: 10 seconds max per execution
- Memory: 256MB max per execution
- Processes: 10 max per execution
- File size: 10MB max
- Execution timeout: 5-10 seconds

#### 4. **Filesystem Sandboxing** ✅
- Temporary directories with restricted permissions (700)
- Cleanup after execution
- No access to host filesystem

#### 5. **Rate Limiting** ✅
- 50 requests per minute per IP
- Prevents abuse and DoS attacks

#### 6. **Container-Level Isolation** ✅
- Non-root user execution
- Container resource limits
- Azure Container Apps security

---

## ⚠️ Security Considerations

### **Potential Risks & Mitigations:**

| Risk | Severity | Mitigation | Status |
|------|----------|------------|--------|
| Code injection | Medium | Code sanitization + subprocess isolation | ✅ Mitigated |
| Resource exhaustion | Medium | Resource limits + rate limiting | ✅ Mitigated |
| Data leakage | Low | Temporary directories cleaned | ✅ Mitigated |
| Network attacks | Low | Network isolation | ✅ Mitigated |
| Container escape | Very Low | Non-root user + ACA isolation | ✅ Mitigated |
| Concurrent execution conflicts | Low | Subprocess isolation | ✅ Mitigated |

### **Additional Recommendations for Contest:**

1. **User Authentication**: Add user ID validation
2. **Question Locking**: Prevent multiple submissions per question
3. **Submission Tracking**: Log all executions for audit
4. **Enhanced Rate Limiting**: Per-user limits (not just IP)
5. **Monitoring**: Set up alerts for resource usage

---

## 📈 Recommended Configuration for 200 Students

### Terraform Variables:
```hcl
min_replicas = 10      # Pre-warmed for contest start
max_replicas = 100    # Handle burst traffic
```

### Execution Service:
- Current security: ✅ **Sufficient**
- Rate limiting: ✅ **Active** (50/min per IP)
- Resource limits: ✅ **Active**

### Monitoring:
- Set up Azure Monitor alerts
- Track execution times
- Monitor error rates
- Watch for resource exhaustion

---

## ✅ Final Verdict

### **Scalability**: ✅ **YES** (with configuration update)
- Can handle 200 students × 2 questions = 400 executions
- Requires `max_replicas = 100`
- Auto-scaling handles traffic spikes

### **Container Model**: ✅ **REUSED** (efficient)
- Containers shared across requests
- Each execution isolated in subprocess
- No one-container-per-user needed

### **Security**: ✅ **SAFE ENOUGH** for contest
- Multiple layers of protection
- Code sanitization + isolation
- Resource limits + rate limiting
- Network isolation

### **Recommendation**: ✅ **APPROVED** for contest
- Update `max_replicas` to 100
- Add user authentication
- Set up monitoring
- Test with 50 students first

---

## 🚀 Next Steps

1. **Update Terraform** for 200 students
2. **Add user authentication** (optional but recommended)
3. **Set up monitoring** and alerts
4. **Load test** with 50 students first
5. **Deploy** for contest


