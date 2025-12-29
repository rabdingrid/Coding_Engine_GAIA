# 🔴 Azure Redis Cache Setup Guide

## 📋 Overview

Azure Redis Cache instance for the Coding Engine project.

**Resource Details:**
- **Name**: `ai-ta-ra-redis`
- **Resource Group**: `ai-ta-2`
- **Location**: `eastus2`
- **SKU**: Basic (C0 - 250MB)
- **TLS**: Required (minimum TLS 1.2)

---

## ⏱️ Creation Time

**Estimated Time**: 10-20 minutes

Azure Redis Cache creation typically takes:
- **Basic tier**: 10-15 minutes
- **Standard tier**: 15-20 minutes
- **Premium tier**: 20-30 minutes

The instance is currently being created. You can check status with:
```bash
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 --query provisioningState
```

---

## 🔗 Connection Details

Once created, you'll get:

### Hostname
```
ai-ta-ra-redis.redis.cache.windows.net
```

### Ports
- **SSL Port**: `6380` (default for Azure Redis)
- **Non-SSL Port**: Disabled (for security)

### Access Keys
Two access keys will be generated:
- **Primary Key**: (will be shown after creation)
- **Secondary Key**: (will be shown after creation)

---

## 🔐 Getting Connection Details

### Method 1: Azure CLI
```bash
# Get hostname and ports
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query "{hostname:hostName,port:port,sslPort:sslPort}" -o json

# Get primary access key
az redis list-keys --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query primaryKey -o tsv

# Get secondary access key
az redis list-keys --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query secondaryKey -o tsv
```

### Method 2: Azure Portal
1. Go to Azure Portal → Resource Groups → `ai-ta-2`
2. Click on `ai-ta-ra-redis`
3. Go to **Access keys** section
4. Copy the connection strings or keys

---

## 💻 How to Use Redis

### Python Example

```python
import redis
import ssl

# Connection details
REDIS_HOST = "ai-ta-ra-redis.redis.cache.windows.net"
REDIS_PORT = 6380
REDIS_PASSWORD = "YOUR_PRIMARY_KEY_HERE"
REDIS_SSL = True

# Create Redis connection
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=REDIS_SSL,
    ssl_cert_reqs=ssl.CERT_REQUIRED,
    decode_responses=True
)

# Test connection
try:
    redis_client.ping()
    print("✅ Connected to Redis!")
except Exception as e:
    print(f"❌ Connection failed: {e}")

# Basic operations
redis_client.set("key1", "value1")
value = redis_client.get("key1")
print(f"Value: {value}")

# Set with expiration (TTL)
redis_client.setex("session:user123", 3600, "active")  # Expires in 1 hour

# Get TTL
ttl = redis_client.ttl("session:user123")
print(f"TTL: {ttl} seconds")
```

### Node.js Example

```javascript
const redis = require('redis');

// Connection details
const REDIS_HOST = 'ai-ta-ra-redis.redis.cache.windows.net';
const REDIS_PORT = 6380;
const REDIS_PASSWORD = 'YOUR_PRIMARY_KEY_HERE';

// Create Redis client
const client = redis.createClient({
  socket: {
    host: REDIS_HOST,
    port: REDIS_PORT,
    tls: true
  },
  password: REDIS_PASSWORD
});

// Connect
client.on('error', (err) => console.log('Redis Client Error', err));
await client.connect();

// Test connection
await client.ping();
console.log('✅ Connected to Redis!');

// Basic operations
await client.set('key1', 'value1');
const value = await client.get('key1');
console.log(`Value: ${value}`);

// Set with expiration
await client.setEx('session:user123', 3600, 'active');  // Expires in 1 hour

// Get TTL
const ttl = await client.ttl('session:user123');
console.log(`TTL: ${ttl} seconds`);
```

### Connection String Format

**Redis Connection String:**
```
rediss://:YOUR_PRIMARY_KEY@ai-ta-ra-redis.redis.cache.windows.net:6380
```

**Note**: `rediss://` (with double 's') indicates SSL/TLS connection.

---

## 🔒 Security Best Practices

1. **Use SSL/TLS**: Always connect using port 6380 (SSL)
2. **Rotate Keys**: Regularly rotate access keys
3. **Use Secondary Key**: Keep primary key for production, use secondary for rotation
4. **Environment Variables**: Store keys in environment variables, never in code
5. **Firewall Rules**: Configure firewall rules to restrict access (if needed)

---

## 📦 Installation Requirements

### Python
```bash
pip install redis
```

### Node.js
```bash
npm install redis
```

### C# / .NET
```bash
dotnet add package StackExchange.Redis
```

---

## 🎯 Use Cases for Coding Engine

### 1. **Session Management**
```python
# Store user session
redis_client.setex(f"session:{user_id}", 3600, json.dumps(session_data))

# Get session
session = json.loads(redis_client.get(f"session:{user_id}"))
```

### 2. **Rate Limiting**
```python
# Check rate limit
key = f"ratelimit:{user_id}"
current = redis_client.incr(key)
if current == 1:
    redis_client.expire(key, 60)  # 1 minute window
if current > 100:  # Max 100 requests per minute
    raise RateLimitExceeded()
```

### 3. **Caching Question Data**
```python
# Cache question data
question_key = f"question:{question_id}"
redis_client.setex(question_key, 3600, json.dumps(question_data))

# Get cached question
cached = redis_client.get(question_key)
if cached:
    question = json.loads(cached)
```

### 4. **Queue Management**
```python
# Add to queue
redis_client.lpush("execution_queue", json.dumps(job_data))

# Process queue
job = redis_client.brpop("execution_queue", timeout=10)
if job:
    job_data = json.loads(job[1])
```

---

## 📊 Monitoring

### Check Redis Status
```bash
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query "{status:provisioningState,hostname:hostName,port:port,sslPort:sslPort}"
```

### View Metrics (Azure Portal)
1. Go to Redis instance in Azure Portal
2. Click on **Metrics**
3. Monitor:
   - **Cache Hits/Misses**
   - **Memory Usage**
   - **Connected Clients**
   - **Operations per Second**

---

## 💰 Cost Estimate

**Basic C0 (250MB)**:
- **Price**: ~$15-20/month
- **Storage**: 250MB
- **Suitable for**: Development, small production workloads

**Upgrade Options**:
- **C1 (1GB)**: ~$60/month
- **C2 (2.5GB)**: ~$120/month

---

## 🚨 Troubleshooting

### Connection Issues

**Error: "Connection refused"**
- Check if Redis is fully provisioned (wait 10-20 minutes)
- Verify firewall rules allow your IP

**Error: "Authentication failed"**
- Verify access key is correct
- Check if using primary or secondary key

**Error: "SSL/TLS required"**
- Ensure using port 6380 (SSL port)
- Set `ssl=True` in connection settings

### Check Redis Status
```bash
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query provisioningState
```

Expected: `"Succeeded"` (when ready)

---

## 📝 Next Steps

1. **Wait for provisioning** (10-20 minutes)
2. **Get connection details** using Azure CLI commands above
3. **Update your application** with Redis connection string
4. **Test connection** using the code examples above
5. **Configure firewall** (if needed) to restrict access

---

## 🔗 Quick Reference Commands

```bash
# Get all connection details
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 \
  --query "{hostname:hostName,port:port,sslPort:sslPort,primaryKey:accessKeys.primaryKey,secondaryKey:accessKeys.secondaryKey}" -o json

# Get primary key only
az redis list-keys --name ai-ta-ra-redis --resource-group ai-ta-2 --query primaryKey -o tsv

# Check provisioning status
az redis show --name ai-ta-ra-redis --resource-group ai-ta-2 --query provisioningState -o tsv

# Delete Redis (if needed)
az redis delete --name ai-ta-ra-redis --resource-group ai-ta-2 --yes
```

---

**Last Updated**: December 5, 2024
**Status**: ⏳ Creating (check status with commands above)




