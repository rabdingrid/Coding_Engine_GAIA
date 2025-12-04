# Quick Answers to Your Questions

## ❓ Question 1: How is code executed if not using Piston?

**Answer**: Code is executed using **Python's `subprocess`** module, which directly calls system interpreters/compilers installed in the base image.

**How it works**:
- **Python**: `subprocess.run(['python3', '-c', code])`
- **JavaScript**: `subprocess.run(['node', '-e', code])`
- **Java**: `javac` to compile → `java` to run
- **C++**: `g++` to compile → execute binary

**No Piston API** - Direct system calls to installed runtimes.

---

## ❓ Question 2: Is it using a base image?

**Answer**: **YES** - Using `python:3.11-slim` as the base image, then installing additional runtimes:

```dockerfile
FROM python:3.11-slim

# Install Node.js, Java, C++ compiler
RUN apt-get install nodejs default-jdk g++ ...
```

**Base Image Stack**:
1. `python:3.11-slim` (Debian-based)
2. Node.js 18.x (via NodeSource)
3. Java (default-jdk)
4. C++ compiler (g++)

---

## ❓ Question 3: Can we add guardrails to secure it?

**Answer**: **YES** - I've created an enhanced secure version with:

### ✅ Security Guardrails Added:

1. **Network Isolation** - Blocks all network access
2. **Code Sanitization** - Blocks dangerous imports/patterns
3. **Rate Limiting** - Prevents DoS attacks
4. **Enhanced Filesystem Sandboxing** - Isolated temp directories
5. **Input Validation** - Code length, timeout limits
6. **Resource Limits** - CPU, memory, processes, file size

**Files Created**:
- `executor-service-secure.py` - Enhanced version
- `SECURITY_IMPLEMENTATION_GUIDE.md` - How to use it
- `ARCHITECTURE_AND_SECURITY.md` - Full details

---

## ❓ Question 4: Is all code running in containers inside ACA?

**Answer**: **YES** - Here's the architecture:

```
┌─────────────────────────────────────┐
│  Azure Container App (ACA)          │
│  ┌───────────────────────────────┐  │
│  │  Container Replica (1-10)      │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Flask App               │  │  │
│  │  │  (executor-service.py)  │  │  │
│  │  └─────────────────────────┘  │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  System Runtimes:        │  │  │
│  │  │  - python3               │  │  │
│  │  │  - node                  │  │  │
│  │  │  - javac/java            │  │  │
│  │  │  - g++                   │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Execution Flow**:
1. User sends code → Backend → ACA Executor
2. Executor receives request in **container replica**
3. Code executes via `subprocess` **inside the container**
4. Output captured and returned

**Key Points**:
- ✅ All code runs **inside ACA containers**
- ✅ Each request handled by a **container replica**
- ✅ Code executes via **subprocess within container**
- ✅ Containers are **isolated** from each other
- ✅ Non-root user (`executor` UID 1000)

---

## 📊 Current vs. Enhanced Security

| Feature | Current | Enhanced |
|---------|---------|----------|
| Network Isolation | ❌ | ✅ |
| Code Sanitization | ❌ | ✅ |
| Rate Limiting | ❌ | ✅ |
| Resource Limits | ⚠️ Basic | ✅ Enhanced |
| Filesystem Sandbox | ⚠️ Basic | ✅ Strict |

---

## 🚀 Next Steps

1. **Review** `ARCHITECTURE_AND_SECURITY.md` for full details
2. **Test** `executor-service-secure.py` locally
3. **Deploy** secure version if needed (see `SECURITY_IMPLEMENTATION_GUIDE.md`)

---

**Summary**: Code executes via subprocess in base image containers inside ACA. Enhanced security version available with network isolation, code sanitization, and rate limiting.


