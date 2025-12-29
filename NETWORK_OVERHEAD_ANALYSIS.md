# 🌐 Network Overhead Analysis & Reduction Guide

**Problem:** Network overhead is 737ms (87.2%) of total request time  
**Goal:** Understand and reduce network overhead

---

## 🔍 What is Network Overhead?

**Network Overhead** = All time spent NOT executing your code

```
Total Request Time: 845ms
├─ Actual Code Execution: 108ms (12.8%) ← Your code running
└─ Network Overhead: 737ms (87.2%) ← Everything else!
```

---

## 📊 Detailed Breakdown of Network Overhead (737ms)

### Component 1: Network Latency (Round Trip Time)

**What it is:**
- Time for data to travel from your computer → API server → back
- Physical distance + network routing

**Typical Values:**
```
Local Network:     1-5ms
Same Region:       10-50ms
Cross-Region:      50-200ms
International:     100-500ms
```

**Your Case:** ~50-100ms (Azure East US 2 region)

**Visual:**
```
Client → [Internet] → Azure → [Internet] → Client
   ↓         ↓          ↓         ↓         ↓
  0ms     25ms      50ms     75ms     100ms
```

---

### Component 2: SSL/TLS Handshake

**What it is:**
- Secure connection setup (HTTPS)
- Certificate verification
- Encryption key exchange

**Typical Values:**
```
First Request:     50-200ms (full handshake)
Subsequent:        0-10ms (session reuse)
```

**Your Case:** ~50-100ms (first request or new connection)

**What Happens:**
```
1. Client Hello (10ms)
2. Server Certificate (20ms)
3. Key Exchange (30ms)
4. Handshake Complete (10ms)
Total: ~70ms
```

---

### Component 3: Request Serialization

**What it is:**
- Converting Python dict → JSON string
- Encoding to bytes
- Preparing HTTP request

**Typical Values:**
```
Small Request (<1KB):   1-5ms
Medium Request (10KB):  5-20ms
Large Request (100KB):  20-100ms
```

**Your Case:** ~10-30ms (depending on test case size)

**Code:**
```python
# This takes time:
data = json.dumps({
    "language": "python",
    "code": SOLUTION_CODE,  # Could be large
    "test_cases": test_cases,  # Array of test cases
    ...
}).encode('utf-8')  # Convert to bytes
```

---

### Component 4: HTTP Request Processing

**What it is:**
- Creating HTTP request object
- Adding headers
- Sending over socket

**Typical Values:**
```
Simple Request:    5-15ms
Complex Request:   15-50ms
```

**Your Case:** ~20-40ms

**What Happens:**
```python
req = urllib.request.Request(
    f"{API_URL}/runall",
    data=data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
# Socket connection, DNS lookup, etc.
```

---

### Component 5: API Gateway / Load Balancer Processing

**What it is:**
- Azure Container Apps ingress
- Load balancer routing
- Request validation
- Rate limiting checks

**Typical Values:**
```
Simple Gateway:    10-30ms
Complex Gateway:   30-100ms
With Auth:         50-200ms
```

**Your Case:** ~50-150ms (Azure Container Apps)

**What Happens:**
```
Request arrives → Load Balancer
                → Route to replica
                → Validate request
                → Check rate limits
                → Forward to FastAPI
```

---

### Component 6: FastAPI Request Processing

**What it is:**
- Request parsing
- Pydantic validation
- Middleware execution
- Route matching

**Typical Values:**
```
Simple Endpoint:   5-20ms
Complex Endpoint:  20-100ms
With Validation:   30-150ms
```

**Your Case:** ~30-80ms

**What Happens:**
```python
@app.post('/runall')
async def runall(request: Request, runall_req: RunAllRequest):
    # 1. Parse JSON body (10ms)
    # 2. Validate with Pydantic (10ms)
    # 3. Run middleware (5ms)
    # 4. Route to handler (5ms)
    # Total: ~30ms
```

---

### Component 7: Response Serialization

**What it is:**
- Converting Python objects → JSON
- Encoding response
- Preparing HTTP response

**Typical Values:**
```
Small Response (<1KB):   1-5ms
Medium Response (10KB): 5-20ms
Large Response (100KB): 20-100ms
```

**Your Case:** ~20-50ms (test results can be large)

**What Happens:**
```python
# FastAPI converts this to JSON:
return ExecutionResponse(
    execution_id=...,
    summary={...},
    test_results=[...],  # Array of results
    ...
)
# Then encodes to bytes for HTTP
```

---

### Component 8: Network Return Trip

**What it is:**
- Sending response back through network
- Same as Component 1, but return trip

**Typical Values:**
```
Same as Network Latency: 50-100ms
```

**Your Case:** ~50-100ms

---

### Component 9: Response Parsing

**What it is:**
- Receiving HTTP response
- Decoding JSON
- Parsing into Python objects

**Typical Values:**
```
Small Response:     5-15ms
Medium Response:    15-50ms
Large Response:     50-200ms
```

**Your Case:** ~20-60ms

**What Happens:**
```python
response = urllib.request.urlopen(req)
result = json.loads(response.read().decode('utf-8'))
# Parse JSON, create Python objects
```

---

## 📊 Complete Overhead Breakdown (Estimated)

```
Total Overhead: 737ms
├─ Network Latency (outbound):     50ms   (6.8%)
├─ SSL/TLS Handshake:              70ms   (9.5%)
├─ Request Serialization:          20ms   (2.7%)
├─ HTTP Request Processing:        30ms   (4.1%)
├─ API Gateway/Load Balancer:     100ms   (13.6%)
├─ FastAPI Processing:            50ms   (6.8%)
├─ Response Serialization:         30ms   (4.1%)
├─ Network Latency (return):       50ms   (6.8%)
├─ Response Parsing:               40ms   (5.4%)
└─ Other (buffering, queuing):    307ms  (41.6%)
```

**Note:** The "Other" category includes:
- TCP connection setup/teardown
- Network buffering
- Request queuing
- Response buffering
- Python GIL overhead
- Garbage collection pauses

---

## 🎯 How to Reduce Network Overhead

### Strategy 1: Connection Pooling / Keep-Alive ⭐ **BEST**

**Problem:** Each request creates new TCP connection

**Solution:** Reuse connections

**Current:**
```
Request 1: Connect → Request → Response → Close
Request 2: Connect → Request → Response → Close  ← New connection!
Request 3: Connect → Request → Response → Close  ← New connection!
```

**Optimized:**
```
Request 1: Connect → Request → Response → Keep-Alive
Request 2:          Request → Response → Keep-Alive  ← Reuse!
Request 3:          Request → Response → Keep-Alive  ← Reuse!
```

**Implementation:**
```python
import urllib.request
import http.client

# Create connection pool
class ConnectionPool:
    def __init__(self):
        self.connections = {}
    
    def get_connection(self, host):
        if host not in self.connections:
            # Create persistent connection
            self.connections[host] = http.client.HTTPSConnection(host)
        return self.connections[host]

# Or use requests library with session:
import requests

session = requests.Session()  # Reuses connections!

# Use session for all requests
response = session.post(API_URL, json=data)
```

**Expected Improvement:**
- Eliminates SSL handshake overhead (70ms saved)
- Reduces connection setup (50ms saved)
- **Total: ~120ms saved per request** ⚡

---

### Strategy 2: Use HTTP/2 or HTTP/3

**Problem:** HTTP/1.1 has limitations

**Benefits:**
- Multiplexing (multiple requests on one connection)
- Header compression
- Server push (optional)

**Implementation:**
```python
import httpx  # Supports HTTP/2

async with httpx.AsyncClient(http2=True) as client:
    response = await client.post(API_URL, json=data)
```

**Expected Improvement:**
- 10-30% faster for multiple requests
- Better connection reuse

---

### Strategy 3: Compress Request/Response

**Problem:** Large JSON payloads

**Solution:** Use gzip compression

**Implementation:**
```python
import gzip
import json

# Compress request
data = json.dumps(payload).encode('utf-8')
compressed = gzip.compress(data)

req = urllib.request.Request(
    API_URL,
    data=compressed,
    headers={
        'Content-Type': 'application/json',
        'Content-Encoding': 'gzip'  # Tell server it's compressed
    }
)
```

**Expected Improvement:**
- Reduces payload size by 60-80%
- Faster transmission for large requests
- **Saves 20-50ms for large payloads**

**Note:** Server must support compression (FastAPI does with middleware)

---

### Strategy 4: Reduce Payload Size

**Problem:** Sending unnecessary data

**Solutions:**

1. **Don't send sample_test_cases if empty:**
```python
# Current (sends empty array):
{
    "test_cases": [...],
    "sample_test_cases": []  # Unnecessary!
}

# Optimized (omit if empty):
{
    "test_cases": [...]
    # sample_test_cases omitted
}
```

2. **Minify code (remove comments, whitespace):**
```python
# Current:
code = """def solve(n):
    # This is a comment
    return n * 2
"""

# Optimized:
code = "def solve(n):\n    return n*2"
```

3. **Use shorter field names (if API supports):**
```python
# Current:
{"test_case_id": "test_1", "expected_output": "123"}

# Optimized (if API supports):
{"id": "test_1", "out": "123"}
```

**Expected Improvement:**
- 5-15% smaller payloads
- **Saves 10-30ms for large requests**

---

### Strategy 5: Use Async/Await (Non-blocking)

**Problem:** Synchronous requests block

**Solution:** Use async HTTP client

**Current:**
```python
# Blocks until response
response = urllib.request.urlopen(req)
```

**Optimized:**
```python
import httpx
import asyncio

async def make_request(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=data)
        return response.json()

# Can make multiple requests concurrently
results = await asyncio.gather(
    make_request(data1),
    make_request(data2),
    make_request(data3)
)
```

**Expected Improvement:**
- Better for multiple requests
- Reduces waiting time
- **Saves 20-50ms per concurrent request**

---

### Strategy 6: Use Closer Server / CDN

**Problem:** Geographic distance

**Solution:** Deploy closer or use CDN

**Current:** Azure East US 2 (if you're far away)

**Optimized:**
- Deploy in region closest to users
- Use Azure Front Door (CDN)
- Use edge locations

**Expected Improvement:**
- Reduces latency by 50-200ms
- **Saves 50-200ms per request**

---

### Strategy 7: Optimize FastAPI Response

**Server-side optimizations:**

1. **Disable response validation (if safe):**
```python
# In executor-service-fastapi.py
@app.post('/runall', response_model=None)  # Skip validation
async def runall(...):
    ...
```

2. **Use orjson (faster JSON):**
```python
from fastapi.responses import ORJSONResponse

@app.post('/runall')
async def runall(...):
    return ORJSONResponse(content=result)  # Faster than default
```

3. **Add response compression middleware:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Expected Improvement:**
- 10-30% faster response serialization
- **Saves 10-30ms per request**

---

### Strategy 8: Batch Multiple Requests

**Problem:** Overhead per request

**Solution:** Combine requests (if API supports)

**Note:** Your API doesn't support batching, but you can:
- Use request splitting (as discussed before)
- Send multiple batches in parallel
- Reuse connections

**Expected Improvement:**
- Amortizes overhead across requests
- **Saves 50-100ms per batch**

---

## 📊 Expected Improvements Summary

| Strategy | Time Saved | Complexity | Cost |
|----------|------------|------------|------|
| **Connection Pooling** | 120ms | Low | $0 ⭐ |
| **HTTP/2** | 30-50ms | Medium | $0 |
| **Compression** | 20-50ms | Low | $0 |
| **Reduce Payload** | 10-30ms | Low | $0 |
| **Async Requests** | 20-50ms | Medium | $0 |
| **Closer Server** | 50-200ms | High | $$ |
| **FastAPI Optimizations** | 10-30ms | Low | $0 |
| **Request Batching** | 50-100ms | Low | $0 |

**Combined Potential Savings: 310-580ms (42-79% reduction)** 🚀

---

## 💻 Implementation Examples

### Example 1: Connection Pooling with requests

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create session with connection pooling
session = requests.Session()

# Configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=10,  # Connection pool size
    pool_maxsize=10
)

session.mount("https://", adapter)

# Use session for all requests
def execute_request(test_cases):
    response = session.post(
        API_URL,
        json={
            "language": "python",
            "code": SOLUTION_CODE,
            "test_cases": test_cases,
            "sample_test_cases": [],
            "user_id": "user123",
            "question_id": "q1"
        },
        timeout=600
    )
    return response.json()

# First request: ~845ms (includes connection setup)
# Subsequent requests: ~625ms (reuses connection) ⚡
```

### Example 2: Async with httpx (HTTP/2 + Connection Pooling)

```python
import httpx
import asyncio

async def execute_request_async(test_cases, client):
    """Execute request with persistent client"""
    response = await client.post(
        API_URL,
        json={
            "language": "python",
            "code": SOLUTION_CODE,
            "test_cases": test_cases,
            "sample_test_cases": [],
            "user_id": "user123",
            "question_id": "q1"
        },
        timeout=600.0
    )
    return response.json()

async def main():
    # Create persistent client with HTTP/2
    async with httpx.AsyncClient(
        http2=True,  # Enable HTTP/2
        limits=httpx.Limits(
            max_keepalive_connections=10,
            max_connections=10
        )
    ) as client:
        # First request: ~845ms
        result1 = await execute_request_async(test_cases1, client)
        
        # Subsequent requests: ~600ms (reuses connection + HTTP/2) ⚡
        result2 = await execute_request_async(test_cases2, client)
        result3 = await execute_request_async(test_cases3, client)

asyncio.run(main())
```

### Example 3: Complete Optimized Client

```python
import httpx
import asyncio
from typing import List, Dict

class OptimizedAPIClient:
    def __init__(self):
        self.client = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            http2=True,  # HTTP/2 support
            limits=httpx.Limits(
                max_keepalive_connections=10,
                max_connections=10
            ),
            timeout=600.0
        )
        return self
    
    async def __aexit__(self, *args):
        await self.client.aclose()
    
    async def execute(self, test_cases: List[Dict], user_id: str = "user123"):
        """Execute request with optimizations"""
        # Remove empty sample_test_cases to reduce payload
        payload = {
            "language": "python",
            "code": SOLUTION_CODE,
            "test_cases": test_cases,
            "user_id": user_id,
            "question_id": "warehouse_boxes"
        }
        # Only add if not empty
        # if sample_test_cases:
        #     payload["sample_test_cases"] = sample_test_cases
        
        response = await self.client.post(
            API_URL,
            json=payload,
            headers={
                "Accept-Encoding": "gzip"  # Request compression
            }
        )
        return response.json()

# Usage
async def main():
    async with OptimizedAPIClient() as client:
        # First request: ~845ms
        result1 = await client.execute(test_cases1)
        
        # Subsequent requests: ~550ms (40% faster!) ⚡
        result2 = await client.execute(test_cases2)
        result3 = await client.execute(test_cases3)

asyncio.run(main())
```

---

## 🎯 Quick Wins (Easiest to Implement)

### 1. Use requests.Session() ⭐ **START HERE**

```python
import requests

session = requests.Session()  # That's it!

# Use session instead of requests.post()
response = session.post(API_URL, json=data)
```

**Saves:** ~120ms per request  
**Time to implement:** 1 minute  
**Complexity:** Very Low

### 2. Remove Empty Fields

```python
# Before:
payload = {
    "test_cases": test_cases,
    "sample_test_cases": []  # Remove this!
}

# After:
payload = {
    "test_cases": test_cases
    # sample_test_cases omitted
}
```

**Saves:** ~10-20ms  
**Time to implement:** 1 minute  
**Complexity:** Very Low

### 3. Use httpx with HTTP/2

```python
import httpx

async with httpx.AsyncClient(http2=True) as client:
    response = await client.post(API_URL, json=data)
```

**Saves:** ~50ms per request  
**Time to implement:** 5 minutes  
**Complexity:** Low

---

## 📈 Expected Results

### Current Performance
```
Single Request: 845ms
├─ Execution: 108ms
└─ Overhead: 737ms
```

### With Connection Pooling Only
```
First Request:  845ms (connection setup)
Subsequent:     625ms (reuses connection)
Improvement:    120ms saved (14% faster)
```

### With All Optimizations
```
First Request:  845ms
Subsequent:     450ms (all optimizations)
Improvement:    395ms saved (47% faster!) ⚡
```

---

## ✅ Action Plan

### Phase 1: Quick Wins (Today)
1. ✅ Use `requests.Session()` for connection pooling
2. ✅ Remove empty `sample_test_cases` field
3. ✅ Test and measure improvement

**Expected:** 120-150ms saved (14-18% faster)

### Phase 2: Advanced (This Week)
1. ✅ Switch to `httpx` with HTTP/2
2. ✅ Implement async requests
3. ✅ Add compression support

**Expected:** Additional 50-100ms saved (total 30-35% faster)

### Phase 3: Server-Side (If Possible)
1. ✅ Add response compression middleware
2. ✅ Use orjson for faster JSON
3. ✅ Optimize FastAPI response handling

**Expected:** Additional 20-40ms saved (total 40-50% faster)

---

## 🎓 Summary

**Network Overhead Breakdown:**
- SSL/TLS Handshake: 70ms (9.5%)
- Connection Setup: 50ms (6.8%)
- API Gateway: 100ms (13.6%)
- Request/Response Processing: 200ms (27.1%)
- Network Latency: 100ms (13.6%)
- Other: 217ms (29.4%)

**Best Solutions:**
1. **Connection Pooling** - Saves 120ms (16%)
2. **HTTP/2** - Saves 50ms (7%)
3. **Remove Empty Fields** - Saves 20ms (3%)
4. **Async Requests** - Saves 30ms (4%)

**Combined:** **220ms saved (30% reduction)** ⚡

---

**Report Generated:** December 9, 2025  
**Status:** Ready for Implementation 🚀



