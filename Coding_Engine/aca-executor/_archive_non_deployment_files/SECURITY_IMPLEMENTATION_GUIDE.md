# Security Implementation Guide

## 🔒 Enhanced Security Features

This guide explains the security enhancements added to the executor service and how to use them.

---

## 📋 Security Features Overview

### 1. **Network Isolation** ✅
- Blocks all network access during code execution
- Prevents code from making HTTP requests, socket connections, etc.
- Uses Python's socket module blocking

**How it works**:
```python
# Before execution: Block socket creation
socket.socket = blocked_socket

# After execution: Restore socket
socket.socket = original_socket
```

**Blocks**:
- `import requests`
- `import urllib`
- `socket.socket()`
- `fetch()` in JavaScript
- Network operations in Java/C++

---

### 2. **Code Sanitization** ✅
- Validates code before execution
- Blocks dangerous patterns and imports
- Prevents file system access, subprocess spawning, etc.

**Blocked Patterns**:

**Python**:
- `import os`
- `import subprocess`
- `import sys`
- `eval()`, `exec()`, `compile()`
- File writes (`open(..., 'w')`)

**JavaScript**:
- `require('fs')`
- `require('child_process')`
- `require('os')`
- `eval()`, `Function()`
- `process.*`

**Java**:
- `java.io.File`
- `java.net.*`
- `Runtime.getRuntime()`
- `ProcessBuilder`, `Process`

**C++**:
- `#include <fstream>`
- `#include <sys/socket.h>`
- `system()`, `popen()`

---

### 3. **Rate Limiting** ✅
- Limits requests per IP address
- Prevents DoS attacks
- Configurable limits

**Current Limits**:
- General: 100 requests/minute
- Execute endpoint: 50 requests/minute

**Configuration**:
```python
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)
```

---

### 4. **Enhanced Resource Limits** ✅
- CPU: 10 seconds max
- Memory: 256MB max
- Processes: 10 max
- File size: 10MB max
- Code size: 100KB max
- Core dumps: Disabled

**Implementation**:
```python
resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
resource.setrlimit(resource.RLIMIT_AS, (256MB, 256MB))
resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
resource.setrlimit(resource.RLIMIT_FSIZE, (10MB, 10MB))
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))  # No core dumps
```

---

### 5. **Filesystem Sandboxing** ✅
- All executions run in `/tmp` directory
- Temporary directories are isolated
- Cleaned up after execution
- Restricted permissions (700)

**Implementation**:
```python
temp_dir = tempfile.mkdtemp(prefix='exec_', dir='/tmp')
os.chmod(temp_dir, 0o700)  # Only owner can access
```

---

### 6. **Input Validation** ✅
- Code length limits (100KB)
- Timeout limits (max 10 seconds)
- Language whitelist
- JSON validation

---

## 🚀 How to Use Enhanced Security

### Option 1: Use Secure Version (Recommended)

Replace `executor-service.py` with `executor-service-secure.py`:

```bash
cd aca-executor
cp executor-service-secure.py executor-service.py
```

### Option 2: Deploy Secure Version Separately

Deploy as a new container app:
- Name: `ai-ta-ra-code-executor2-secure`
- Use `executor-service-secure.py` as the service file

---

## 📦 Deployment Steps

### 1. Update Requirements
```bash
# requirements.txt already includes Flask-Limiter
pip install -r requirements.txt
```

### 2. Build Docker Image
```bash
cd aca-executor
docker buildx build --platform linux/amd64 -t executor-secure:v1 .
```

### 3. Push to ACR
```bash
az acr login --name aitaraacr1763805702
docker tag executor-secure:v1 aitaraacr1763805702.azurecr.io/executor-secure:v1
docker push aitaraacr1763805702.azurecr.io/executor-secure:v1
```

### 4. Update Terraform (Optional)
```terraform
variable "executor_image" {
  default = "aitaraacr1763805702.azurecr.io/executor-secure:v1"
}
```

### 5. Deploy
```bash
cd terraform
terraform apply
```

---

## 🧪 Testing Security Features

### Test 1: Network Isolation
```bash
curl -X POST "https://ai-ta-ra-code-executor2.../execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import requests; print(requests.get(\"https://google.com\"))",
    "test_cases": [{"input": "", "expected_output": ""}]
  }'
```

**Expected**: Error - "Network operations not allowed"

### Test 2: Code Sanitization
```bash
curl -X POST "https://ai-ta-ra-code-executor2.../execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import os; os.system(\"rm -rf /\")",
    "test_cases": [{"input": "", "expected_output": ""}]
  }'
```

**Expected**: Error - "Blocked pattern detected: import os"

### Test 3: Rate Limiting
```bash
# Send 60 requests quickly
for i in {1..60}; do
  curl -X POST "https://ai-ta-ra-code-executor2.../execute" ...
done
```

**Expected**: After 50 requests, HTTP 429 (Too Many Requests)

### Test 4: Resource Limits
```bash
curl -X POST "https://ai-ta-ra-code-executor2.../execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "while True: pass",
    "test_cases": [{"input": "", "expected_output": ""}]
  }'
```

**Expected**: Timeout after 5-10 seconds

---

## ⚠️ Security Considerations

### Current Limitations:

1. **No Syscall Filtering**: Can still call system functions (seccomp needed)
2. **No Process Isolation**: Can spawn child processes (namespaces needed)
3. **Soft Resource Limits**: Can be bypassed in some cases (cgroups needed)
4. **Pattern Matching**: May have false positives/negatives

### Recommended for Production:

1. **Add WAF** (Web Application Firewall) at Azure level
2. **Enable DDoS Protection** in Azure
3. **Implement Audit Logging** for all executions
4. **Add Monitoring** for suspicious patterns
5. **Regular Security Scanning** of container images

---

## 📊 Security Comparison

| Feature | Current | Enhanced | Production |
|---------|---------|----------|------------|
| Network Isolation | ❌ | ✅ | ✅ |
| Code Sanitization | ❌ | ✅ | ✅ |
| Rate Limiting | ❌ | ✅ | ✅ |
| Resource Limits | ⚠️ | ✅ | ✅ |
| Filesystem Sandbox | ⚠️ | ✅ | ✅ |
| Syscall Filtering | ❌ | ❌ | ✅ (seccomp) |
| Process Isolation | ⚠️ | ⚠️ | ✅ (namespaces) |
| WAF | ❌ | ❌ | ✅ |
| DDoS Protection | ❌ | ❌ | ✅ |

---

## 🎯 Next Steps

1. **Review security requirements** for your use case
2. **Test enhanced version** with malicious code samples
3. **Deploy enhanced version** to staging
4. **Monitor and audit** execution logs
5. **Implement Phase 2** security (seccomp, namespaces) if needed

---

**Note**: The enhanced version is suitable for **semi-trusted code execution** (e.g., authenticated users in educational platforms). For **fully untrusted code** (public code execution), consider additional security measures (seccomp, namespaces, WAF, etc.).


