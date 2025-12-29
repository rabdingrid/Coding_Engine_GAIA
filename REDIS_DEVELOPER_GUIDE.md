# 🔴 Redis Cache - Developer Integration Guide

## 📋 Quick Start

This guide helps developers connect to and use the Azure Redis Cache for the Coding Engine project.

---

## 🔗 Connection Details

### Hostname & Port
```
Hostname: ai-ta-ra-redis.redis.cache.windows.net
SSL Port: 6380 (use this for secure connections)
```

[Will be provided separately - check with team lead]
```

**Secondary Key:**
```
[Will be provided separately - check with team lead]
```

**Connection String Format:**
```
rediss://:YOUR_ACCESS_KEY@ai-ta-ra-redis.redis.cache.windows.net:6380
```

---

## 🚀 Quick Setup

### Step 1: Install Redis Client Library

**Python:**
```bash
pip install redis
```

**Node.js:**
```bash
npm install redis
```

**C# / .NET:**
```bash
dotnet add package StackExchange.Redis
```

### Step 2: Connect to Redis

#### Python Example
```python
import redis
import ssl
import os

# Get connection details from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "ai-ta-ra-redis.redis.cache.windows.net")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6380"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")  # Set this in your environment

# Create Redis connection
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    decode_responses=True
)

# Test connection
try:
    redis_client.ping()
    print("✅ Connected to Redis!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

#### Node.js Example
```javascript
const redis = require('redis');

// Get connection details from environment variables
const REDIS_HOST = process.env.REDIS_HOST || 'ai-ta-ra-redis.redis.cache.windows.net';
const REDIS_PORT = parseInt(process.env.REDIS_PORT || '6380');
const REDIS_PASSWORD = process.env.REDIS_PASSWORD; // Set this in your environment

// Create Redis client
const client = redis.createClient({
  socket: {
    host: REDIS_HOST,
    port: REDIS_PORT,
    tls: true
  },
  password: REDIS_PASSWORD
});

// Connect and test
client.on('error', (err) => console.log('Redis Client Error', err));

(async () => {
  await client.connect();
  await client.ping();
  console.log('✅ Connected to Redis!');
})();
```

#### C# Example
```csharp
using StackExchange.Redis;

// Get connection details from environment variables
string redisHost = Environment.GetEnvironmentVariable("REDIS_HOST") 
    ?? "ai-ta-ra-redis.redis.cache.windows.net";
string redisPort = Environment.GetEnvironmentVariable("REDIS_PORT") ?? "6380";
string redisPassword = Environment.GetEnvironmentVariable("REDIS_PASSWORD");

// Create connection
var configuration = ConfigurationOptions.Parse($"{redisHost}:{redisPort}");
configuration.Password = redisPassword;
configuration.Ssl = true;

var connection = ConnectionMultiplexer.Connect(configuration);
var db = connection.GetDatabase();

// Test connection
if (connection.IsConnected)
{
    Console.WriteLine("✅ Connected to Redis!");
}
```

---

## 💻 Common Use Cases

### 1. Session Management

**Store user session:**
```python
import json
from datetime import timedelta

user_id = "user123"
session_data = {
    "user_id": user_id,
    "logged_in": True,
    "timestamp": "2024-12-05T10:00:00Z"
}

# Store session with 1 hour expiration
redis_client.setex(
    f"session:{user_id}",
    3600,  # TTL in seconds (1 hour)
    json.dumps(session_data)
)

# Retrieve session
session_json = redis_client.get(f"session:{user_id}")
if session_json:
    session = json.loads(session_json)
    print(f"User {session['user_id']} is logged in")
```

### 2. Rate Limiting

**Implement rate limiting:**
```python
def check_rate_limit(user_id, max_requests=100, window_seconds=60):
    key = f"ratelimit:{user_id}"
    
    # Increment counter
    current = redis_client.incr(key)
    
    # Set expiration on first request
    if current == 1:
        redis_client.expire(key, window_seconds)
    
    # Check if limit exceeded
    if current > max_requests:
        ttl = redis_client.ttl(key)
        raise Exception(f"Rate limit exceeded. Try again in {ttl} seconds.")
    
    return {
        "requests": current,
        "remaining": max_requests - current,
        "reset_in": redis_client.ttl(key)
    }

# Usage
try:
    limit_info = check_rate_limit("user123", max_requests=100)
    print(f"Requests: {limit_info['requests']}/{100}")
except Exception as e:
    print(f"Error: {e}")
```

### 3. Caching Question Data

**Cache frequently accessed data:**
```python
import json

def get_question(question_id):
    cache_key = f"question:{question_id}"
    
    # Try to get from cache
    cached = redis_client.get(cache_key)
    if cached:
        print("✅ Cache hit!")
        return json.loads(cached)
    
    # Cache miss - fetch from database
    print("❌ Cache miss - fetching from database")
    question_data = fetch_from_database(question_id)  # Your DB function
    
    # Store in cache for 1 hour
    redis_client.setex(
        cache_key,
        3600,
        json.dumps(question_data)
    )
    
    return question_data
```

### 4. Queue Management

**Simple job queue:**
```python
import json

def add_to_queue(job_data):
    """Add job to execution queue"""
    redis_client.lpush("execution_queue", json.dumps(job_data))
    print(f"✅ Job added to queue: {job_data['job_id']}")

def process_queue():
    """Process jobs from queue"""
    while True:
        # Blocking pop - waits up to 10 seconds
        result = redis_client.brpop("execution_queue", timeout=10)
        
        if result:
            job_data = json.loads(result[1])
            print(f"Processing job: {job_data['job_id']}")
            # Process the job...
            process_job(job_data)
        else:
            print("No jobs in queue, waiting...")
```

### 5. Distributed Locking

**Prevent concurrent execution:**
```python
import time
import uuid

def acquire_lock(lock_name, timeout=10):
    """Acquire a distributed lock"""
    lock_key = f"lock:{lock_name}"
    lock_value = str(uuid.uuid4())
    
    # Try to acquire lock (set if not exists)
    acquired = redis_client.set(
        lock_key,
        lock_value,
        ex=timeout,  # Auto-expire after timeout
        nx=True     # Only set if not exists
    )
    
    return lock_value if acquired else None

def release_lock(lock_name, lock_value):
    """Release a distributed lock"""
    lock_key = f"lock:{lock_name}"
    
    # Use Lua script to ensure we only delete our own lock
    lua_script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    
    redis_client.eval(lua_script, 1, lock_key, lock_value)

# Usage
lock_value = acquire_lock("process_user_123")
if lock_value:
    try:
        # Do critical work
        process_user_data("user_123")
    finally:
        release_lock("process_user_123", lock_value)
else:
    print("Could not acquire lock - another process is running")
```

---

## 🔐 Environment Variables Setup

**Never hardcode credentials!** Use environment variables:

### Python (.env file)
```bash
REDIS_HOST=ai-ta-ra-redis.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=your_primary_key_here
```

### Node.js (.env file)
```bash
REDIS_HOST=ai-ta-ra-redis.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=your_primary_key_here
```

### C# (appsettings.json)
```json
{
  "Redis": {
    "Host": "ai-ta-ra-redis.redis.cache.windows.net",
    "Port": "6380",
    "Password": "your_primary_key_here"
  }
}
```

---

## ✅ Testing Your Connection

### Quick Test Script (Python)
```python
import redis
import ssl
import os

REDIS_HOST = os.getenv("REDIS_HOST", "ai-ta-ra-redis.redis.cache.windows.net")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6380"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

try:
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_REQUIRED,
        decode_responses=True
    )
    
    # Test 1: Ping
    response = client.ping()
    print(f"✅ Ping: {response}")
    
    # Test 2: Set/Get
    client.set("test_key", "test_value", ex=60)
    value = client.get("test_key")
    print(f"✅ Set/Get: {value}")
    
    # Test 3: Info
    info = client.info("server")
    print(f"✅ Redis version: {info.get('redis_version', 'unknown')}")
    
    print("\n🎉 All tests passed! Redis is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 🚨 Troubleshooting

### Connection Issues

**Error: "Connection refused"**
- ✅ Check if Redis is fully provisioned (status should be "Succeeded")
- ✅ Verify you're using port 6380 (SSL port)
- ✅ Check firewall rules (if configured)

**Error: "Authentication failed"**
- ✅ Verify access key is correct
- ✅ Check if key has expired (rotate if needed)
- ✅ Ensure no extra spaces in password

**Error: "SSL/TLS required"**
- ✅ Ensure using port 6380 (not 6379)
- ✅ Set `ssl=True` in connection settings
- ✅ Use `rediss://` (double 's') in connection string

### Check Redis Status
```bash
# Using Azure CLI
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query provisioningState

# Should return: "Succeeded"
```

---

## 📊 Best Practices

1. **Always use SSL/TLS** (port 6380)
2. **Store credentials in environment variables** (never in code)
3. **Use connection pooling** for better performance
4. **Set appropriate TTL** for cached data
5. **Handle connection errors gracefully**
6. **Monitor memory usage** (250MB limit for Basic tier)
7. **Use secondary key for rotation** without downtime

---

## 🔄 Key Rotation

If you need to rotate keys:

1. Update application to use **secondary key**
2. Regenerate **primary key** in Azure Portal
3. Update application to use new **primary key**
4. Regenerate **secondary key** for next rotation

This ensures zero downtime during key rotation.

---

## 📝 What to Share with Developers

Share this document along with:

1. **Connection Details:**
   - Hostname: `ai-ta-ra-redis.redis.cache.windows.net`
   - Port: `6380`
   - Access Key: (Share securely via password manager or encrypted channel)

2. **This Guide:** `REDIS_DEVELOPER_GUIDE.md`

3. **Environment Variables Template:**
   ```bash
   REDIS_HOST=ai-ta-ra-redis.redis.cache.windows.net
   REDIS_PORT=6380
   REDIS_PASSWORD=<share_access_key_securely>
   ```

---

## 🔗 Additional Resources

- [Azure Redis Cache Documentation](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/)
- [Redis Commands Reference](https://redis.io/commands)
- [Python Redis Client Docs](https://redis-py.readthedocs.io/)
- [Node.js Redis Client Docs](https://github.com/redis/node-redis)

---

**Last Updated**: December 5, 2024
**Maintained By**: Coding Engine Team




