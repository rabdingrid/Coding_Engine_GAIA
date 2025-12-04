# Container-Level Isolation Analysis

## 🎯 Your Question: "If anything goes wrong, will it be container-level?"

**Short Answer: YES, but with important caveats.**

---

## ✅ **Container-Level Isolation (Azure Container Apps)**

### **What Azure Provides:**

1. **Container Isolation** ✅
   - Each container runs in its own isolated environment
   - Containers cannot directly access other containers
   - Network isolation between containers
   - Resource limits enforced per container

2. **Host Protection** ✅
   - Containers cannot access the host system
   - No direct access to host filesystem
   - No access to host processes
   - Azure manages container lifecycle

3. **Resource Limits** ✅
   - CPU: 1.0 vCPU per container (enforced by Azure)
   - Memory: 2.0 GiB per container (enforced by Azure)
   - Network: Isolated network namespace

---

## ⚠️ **Within-Container Risks**

### **The Problem:**

If malicious code **breaks out of the subprocess sandbox** within a container, it could:

1. **Access other processes in the same container**
   - See other executions running in the same container
   - Potentially interfere with other executions
   - Access shared container filesystem

2. **Access container filesystem**
   - Read/write files in `/tmp` (other executions' temp dirs)
   - Access `/app` directory (application code)
   - Access environment variables

3. **Resource exhaustion**
   - Consume all CPU/memory in the container
   - Affect other executions in the same container
   - Cause container to be killed by Azure (if limits exceeded)

---

## 🛡️ **Current Protections (Defense in Depth)**

### **Layer 1: Code Sanitization** ✅
- Blocks dangerous imports (`os`, `subprocess`, `sys`)
- AST-based analysis detects obfuscated code
- Prevents most dangerous operations **before execution**

### **Layer 2: Subprocess Isolation** ✅
- Each execution runs in separate subprocess
- Resource limits per subprocess (CPU, memory, processes)
- Isolated temporary directories (`/tmp/exec_*`)
- Cleanup after execution

### **Layer 3: Network Isolation** ✅
- Socket creation blocked
- No outbound network access
- Prevents data exfiltration

### **Layer 4: Resource Limits** ✅
- CPU: 10 seconds max per execution
- Memory: 256MB max per execution
- Processes: 5 max per execution
- File size: 10MB max

### **Layer 5: Container-Level Limits** ✅
- CPU: 1.0 vCPU per container (Azure enforced)
- Memory: 2.0 GiB per container (Azure enforced)
- If container exceeds limits, Azure kills it

### **Layer 6: Rate Limiting** ✅
- 30 requests/minute per IP
- Prevents abuse and DoS attacks

---

## 🔍 **Attack Scenarios & Mitigations**

### **Scenario 1: Code tries to break out of subprocess**
```python
# Malicious code
import os  # BLOCKED by code sanitization
os.system("rm -rf /")  # BLOCKED (can't even reach here)
```

**Mitigation:**
- ✅ Code sanitization blocks `import os` before execution
- ✅ Even if it runs, subprocess has resource limits
- ✅ Container-level limits prevent host access

**Risk Level: LOW** (blocked at Layer 1)

---

### **Scenario 2: Code tries to access other processes**
```python
# Malicious code
import psutil  # Not blocked, but limited
for proc in psutil.process_iter():
    proc.kill()  # Could kill other executions
```

**Mitigation:**
- ⚠️ `psutil` is not blocked (needed for monitoring)
- ✅ Resource limits: Max 5 processes per execution
- ✅ Container-level limits: Max 1.0 vCPU, 2.0 GiB
- ✅ Rate limiting: 30 requests/minute

**Risk Level: MEDIUM** (limited by resource constraints)

---

### **Scenario 3: Code tries to exhaust container resources**
```python
# Malicious code
while True:
    data = "x" * 1000000  # Memory exhaustion
```

**Mitigation:**
- ✅ Subprocess limit: 256MB max per execution
- ✅ Container limit: 2.0 GiB max (Azure enforced)
- ✅ Timeout: 5-10 seconds max per execution
- ✅ If container exceeds limits, Azure kills it

**Risk Level: LOW** (multiple limits prevent this)

---

### **Scenario 4: Code tries to access other executions' files**
```python
# Malicious code
import os
files = os.listdir("/tmp")  # Could see other executions' temp dirs
```

**Mitigation:**
- ⚠️ `import os` is blocked by code sanitization
- ✅ Even if it runs, temp dirs have restricted permissions (700)
- ✅ Cleanup after execution removes temp dirs
- ✅ No access to `/app` directory (application code)

**Risk Level: LOW-MEDIUM** (blocked by code sanitization, limited by permissions)

---

## 📊 **Isolation Guarantees**

### **✅ What IS Isolated:**

1. **Container-to-Container** ✅
   - Containers cannot access each other
   - Network isolation between containers
   - Resource limits per container

2. **Container-to-Host** ✅
   - Containers cannot access host system
   - No host filesystem access
   - No host process access

3. **Execution-to-Execution (within container)** ⚠️
   - Each execution in separate subprocess
   - Isolated temp directories
   - Resource limits per execution
   - **BUT**: If code breaks out, could affect other executions in same container

---

## 🎯 **Risk Assessment**

### **For Educational Contests (200-300 students):**

| Risk | Severity | Likelihood | Mitigation | Status |
|------|----------|------------|------------|--------|
| **Container compromise** | High | Low | Code sanitization + resource limits | ✅ Mitigated |
| **Host compromise** | Critical | Very Low | Container isolation (Azure) | ✅ Mitigated |
| **Other containers affected** | High | Very Low | Container isolation (Azure) | ✅ Mitigated |
| **Other executions in same container** | Medium | Low-Medium | Subprocess isolation + limits | ⚠️ Partially mitigated |
| **Resource exhaustion** | Medium | Low | Multiple limits (subprocess + container) | ✅ Mitigated |

---

## 💡 **Recommendations**

### **Current State: GOOD for Educational Use** ✅

**For 200-300 students:**
- ✅ **Container-level isolation** protects host and other containers
- ✅ **Subprocess isolation** protects most executions within container
- ✅ **Multiple security layers** provide defense in depth
- ⚠️ **Within-container risk** exists but is low for authenticated users

### **If You Need Stronger Isolation:**

1. **Container-per-execution** (Not Recommended)
   - ✅ Maximum isolation
   - ❌ Very expensive (200-300 containers)
   - ❌ Slow startup time
   - ❌ Not scalable

2. **Azure Dynamic Sessions** (Alternative)
   - ✅ Hyper-V isolation (hardware-level)
   - ✅ Maximum security
   - ⚠️ More complex setup
   - ⚠️ Higher cost

3. **Current Solution** (Recommended)
   - ✅ Good balance of security and cost
   - ✅ Scalable for 200-300 students
   - ✅ Multiple security layers
   - ⚠️ Within-container risk (acceptable for educational use)

---

## ✅ **Final Answer**

### **"If anything goes wrong, will it be container-level?"**

**YES, with important caveats:**

1. **✅ Container-to-Container**: Fully isolated
   - If one container is compromised, others are safe
   - Host system is safe

2. **✅ Container-to-Host**: Fully isolated
   - Containers cannot access host
   - Azure enforces this isolation

3. **⚠️ Within-Container**: Partially isolated
   - Each execution in separate subprocess
   - If code breaks out of subprocess, could affect other executions in same container
   - **BUT**: Multiple security layers make this very unlikely

### **Risk Level: LOW-MEDIUM for Educational Use**

**For authenticated students in educational contests:**
- ✅ **Safe enough** with current security measures
- ✅ **Container-level isolation** protects host and other containers
- ✅ **Subprocess isolation** protects most executions
- ⚠️ **Within-container risk** is acceptable for educational use

**For fully untrusted code:**
- ⚠️ **Consider stronger isolation** (container-per-execution or Azure Dynamic Sessions)

---

## 🎯 **Bottom Line**

**Your system is container-level isolated, but within a container, executions share the same environment.**

**For educational contests with authenticated students, this is SAFE ENOUGH.**

**The multiple security layers (code sanitization, subprocess isolation, resource limits, network isolation) make it very difficult for malicious code to break out and affect other executions.**

**If you need maximum isolation, consider container-per-execution (expensive) or Azure Dynamic Sessions (more complex).**

---

**Your current setup provides a good balance of security, cost, and scalability!** 🎉


