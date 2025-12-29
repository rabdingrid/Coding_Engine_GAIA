# The Journey of Building GAIA: Engineering the Coding Executor

**Date:** December 16, 2025  
**Topic:** Technical Architecture & Deployment Strategy

---

## 🚀 The Core Challenge
Our mission was to build a secure, scalable code execution engine capable of handling high-concurrency coding contests. We started by evaluating existing solutions but quickly encountered roadblocks that necessitated a custom engineering approach.

### The Evolution of Our Thoughts
1.  **Phase 1: Piston Library**  
    We initially considered *Piston*, a popular open-source code execution engine.
    *   **Blocker:** Piston requires **privileged mode** to run, which is a major security risk and is often blocked in managed cloud environments like Azure Container Apps (ACA).
2.  **Phase 2: Kubernetes (AKS)**  
    To support privileged containers, we considered Azure Kubernetes Service (AKS).
    *   **Blocker:** **Cost & Complexity.** Managing a full K8s cluster for a simple execution microservice was overkill and prohibitively expensive for our use case.
3.  **Phase 3: Azure Dynamic Sessions**  
    We looked at Azure's native "safe sandbox" solution.
    *   **Blocker:** While secure, it is a proprietary "black box" that is **difficult to configure** and expensive to scale for thousands of short-lived executions.

## 🛠 Our Solution: The Custom GAIA Executor
We engineered a dedicated **Custom Coding Executor Engine** designed specifically for our workload.

### 1. Architecture & Security
*   **Base Images:** We built custom Docker images pre-loaded with compilers/runtimes for **C++, Python, Java, JavaScript, and C#**.
*   **Container-Level Sandboxing:** Instead of relying on privileged kernel features, we implemented security at the container level.
    *   **`ulimit` Enforcement:** Strict limits on CPU time, memory usage, and file descriptors are applied to every user process.
    *   **Error Handling:** Instant detection of TLE (Time Limit Exceeded), MLE (Memory Limit Exceeded), and Runtime Errors without crashing the container.

### 2. The "Compile Once" Optimization (30s → <2s)
The biggest performance win came from rethinking how we handle test cases, particularly for compiled languages like C++.
*   **Old Way:** Compile the code -> Run Test Case 1 -> Re-compile -> Run Test Case 2...
    *   *Result:* 10 test cases took **~30 seconds**.
*   **GAIA Way (for C++):** **Compile ONCE -> Run Binary against ALL Test Cases**.
    *   *Result:* Total execution time dropped to **under 2 seconds**. A 15x speedup.
    *   *Note:* Interpreted languages (Python, JS) also benefit from efficient sequential execution without process overhead.

### 3. Concurrency Design: Why Sequential?
We initially tried running user test cases in parallel using Python's `ThreadPoolExecutor`.
*   **The Problem:** Under load (50 users), this flooded the CPU, causing **HTTP 503 Service Unavailable** errors.
*   **The Fix:** We switched to **Sequential Test Case Execution** within a single request.
    *   Because our "Compile Once" optimization is so fast, executing 10 test cases sequentially takes milliseconds.
    *   This keeps CPU usage stable and predictable, allowing us to handle more *users* rather than more *threads*.

### 4. Queue System
To handle the "Contest Start" burst (where everyone submits at once), we implemented an internal **Request Queue**. This ensures that even if 100 requests arrive instantly, they are processed in an orderly fashion without dropping connections.

---

## 📊 Deployment Strategy Comparison

| Feature | **Piston** | **Azure Dynamic Sessions** | **GAIA Custom Executor** |
| :--- | :--- | :--- | :--- |
| **Security** | ❌ Unsafe (Privileged) | ✅ High (VM Level) | ✅ **High (Container + ulimit)** |
| **Cost** | 💲 Low (Self-hosted) | 💲💲💲 High | 💲 **Extremely Low** |
| **Complexity** | ⚠️ Medium | ⚠️ High (Config) | ✅ **Low (Standard Docker)** |
| **Performance** | ⚡ Fast | 🐢 Slower Cold Starts | ⚡ **Blazing Fast (<2s)** |

---

## 📈 Scaling & Cost Projection (500 Users Contest)

Based on our validated 200-user load tests, here is the projection for a **500-User Contest (3 Hours)**:

*   **Load Estimate:** 500 Users × 3 Questions = **1,500 Submissions** (plus test runs).
*   **Scaling Requirement:**
    *   **Ideal Replicas:** 5 - 8 Container Replicas (Auto-scaling enabled).
    *   **Capacity:** Each replica handles ~40 requests/minute. System total: ~300+ req/min.
*   **Performance:**
    *   **Ideal Execution Time:** **< 2 seconds** per submission.
    *   **Queue Wait Time:** < 5 seconds even at peak.
*   **Estimated Cost:**
    *   **Total Contest Cost:** **~$7.00 - $10.00**.
    *   *Why so cheap?* We use efficient Linux execution environments that consume resources only when running code.

**Conclusion:** The GAIA Executor is not just a workaround; it is a high-performance, cost-efficient engine superior to off-the-shelf alternatives for our specific needs.
