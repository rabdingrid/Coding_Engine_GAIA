# Architecture & Security Analysis

## 🔍 How Code Execution Works

### Current Implementation (NOT using Piston)

**Base Image**: `python:3.11-slim` with additional runtimes installed:
- Python 3.11 (from base image)
- Node.js 18.x (installed via NodeSource)
- Java (default-jdk)
- C++ compiler (g++)

**Execution Method**: Direct `subprocess` calls to system interpreters/compilers

```python
# Python: subprocess.run(['python3', '-c', code])
# Node.js: subprocess.run(['node', '-e', code])
# Java: javac → java (compiled)
# C++: g++ → executable (compiled)
```

**Container Architecture**:
```
┌─────────────────────────────────────────┐
│  Azure Container App (ACA)              │
│  ┌───────────────────────────────────┐  │
│  │  Container Replica (1-10)          │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Flask App (executor-service)│  │  │
│  │  │  Port: 8000                  │  │  │
│  │  └─────────────────────────────┘  │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  System Runtimes:           │  │  │
│  │  │  - python3                  │  │  │
│  │  │  - node                      │  │  │
│  │  │  - javac/java                │  │  │
│  │  │  - g++                       │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
│                                          │
│  Request Flow:                           │
│  1. User → Backend → ACA Executor        │
│  2. Executor → subprocess → Runtime      │
│  3. Runtime executes code in container   │
│  4. Output captured and returned          │
└─────────────────────────────────────────┘
```

**Key Points**:
- ✅ All code runs **inside ACA containers** (isolated)
- ✅ Each request handled by a container replica
- ✅ Code executes via subprocess within the container
- ✅ No Piston API (direct system calls)
- ⚠️ **Security**: Basic limits, but needs enhancement

---

## 🔒 Current Security Measures

### Existing Protections:

1. **Resource Limits** (via `resource.setrlimit`):
   - CPU: 10 seconds max
   - Memory: 256MB max
   - Processes: 10 max
   - File size: 10MB max
   - Timeout: 5 seconds (subprocess)

2. **Container Isolation**:
   - Non-root user (`executor` UID 1000)
   - Container-level isolation (ACA)
   - Temporary directories cleaned up

3. **Input Validation**:
   - JSON validation
   - Language whitelist
   - Timeout enforcement

### ⚠️ Security Gaps:

1. **No network isolation** - code can make network calls
2. **No filesystem sandboxing** - can access container filesystem
3. **No syscall filtering** - can call any system function
4. **Resource limits may not work** - `setrlimit` can be bypassed
5. **No code sanitization** - malicious code can be injected
6. **No rate limiting** - vulnerable to DoS
7. **Environment variables exposed** - code can read env vars
8. **No process isolation** - can spawn child processes

---

## 🛡️ Enhanced Security Guardrails

### Recommended Security Enhancements:

#### 1. **Network Isolation**
```python
# Block network access during execution
import socket
socket.socket = None  # Disable socket creation
```

#### 2. **Filesystem Sandboxing**
```python
# Use chroot or restricted temp directories
# Only allow access to /tmp/execution_<uuid>/
```

#### 3. **Syscall Filtering** (seccomp)
```python
# Use seccomp to block dangerous syscalls
# Block: execve, fork, clone, mount, etc.
```

#### 4. **Code Sanitization**
```python
# Block dangerous imports/functions
BLOCKED_PATTERNS = [
    'import os', 'import subprocess', 'import sys',
    '__import__', 'eval', 'exec', 'compile'
]
```

#### 5. **Enhanced Resource Limits**
```python
# Use cgroups for hard limits
# Set via container resources (CPU/memory)
```

#### 6. **Process Isolation**
```python
# Use namespaces to isolate processes
# Prevent access to parent process
```

#### 7. **Rate Limiting**
```python
# Add Flask rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

#### 8. **Input Validation**
```python
# Validate code length, complexity
# Block suspicious patterns
```

---

## 🚀 Implementation Plan

### Phase 1: Critical Security (Immediate)
1. ✅ Network isolation
2. ✅ Enhanced filesystem sandboxing
3. ✅ Code sanitization
4. ✅ Rate limiting

### Phase 2: Advanced Security (Next)
1. ✅ Syscall filtering (seccomp)
2. ✅ Enhanced resource limits (cgroups)
3. ✅ Process isolation (namespaces)
4. ✅ Logging and monitoring

### Phase 3: Production Hardening
1. ✅ WAF (Web Application Firewall)
2. ✅ DDoS protection
3. ✅ Security scanning
4. ✅ Audit logging

---

## 📊 Comparison: Current vs. Enhanced

| Security Feature | Current | Enhanced |
|------------------|---------|----------|
| Network Isolation | ❌ | ✅ |
| Filesystem Sandbox | ⚠️ Basic | ✅ Strict |
| Syscall Filtering | ❌ | ✅ |
| Code Sanitization | ❌ | ✅ |
| Resource Limits | ⚠️ Soft | ✅ Hard |
| Rate Limiting | ❌ | ✅ |
| Process Isolation | ⚠️ Basic | ✅ Strict |
| Input Validation | ⚠️ Basic | ✅ Strict |

---

## 🎯 Next Steps

1. **Review security requirements** for your use case
2. **Implement Phase 1** security enhancements
3. **Test security** with malicious code samples
4. **Deploy enhanced version** to ACA
5. **Monitor and audit** execution logs

---

**Note**: The current implementation is suitable for **trusted code execution** (e.g., educational platforms with authenticated users). For **untrusted code** (e.g., public code execution), Phase 1+ enhancements are **strongly recommended**.


