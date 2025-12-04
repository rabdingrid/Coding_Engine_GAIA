# Queue System Issue - Root Cause & Fix

## 🐛 **Problem**

When 1 replica was running, only one code execution worked at a time. Other requests **hung** (didn't respond) and required Ctrl+C to stop.

## 🔍 **Root Cause**

The Flask application was running in **development mode** (single-threaded):

```dockerfile
CMD ["python3", "executor-service.py"]
```

**Why This Caused Hanging:**
1. Flask's development server is **single-threaded**
2. It can only handle **one request at a time**
3. When multiple requests arrive:
   - First request: Processes normally
   - Second request: **Waits in queue** (but Flask dev server doesn't handle queues properly)
   - Third request: **Also waits** (indefinitely)
4. Requests appear to "hang" because Flask dev server doesn't process the queue correctly

## ✅ **Solution**

Use **Gunicorn** (production WSGI server) with multiple workers and threads:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "60", "--worker-class", "sync", "executor-service:app"]
```

**What This Does:**
- **4 workers**: 4 separate processes handling requests
- **2 threads per worker**: Each worker can handle 2 concurrent requests
- **Total capacity**: 4 workers × 2 threads = **8 concurrent requests per replica**
- **Timeout**: 60 seconds (prevents hanging)

## 📊 **Before vs After**

### **Before (Flask Dev Server):**
- ❌ Single-threaded
- ❌ Only 1 request at a time
- ❌ Requests hang when queue builds up
- ❌ No proper queue handling

### **After (Gunicorn):**
- ✅ 4 workers × 2 threads = 8 concurrent requests
- ✅ Proper request queue handling
- ✅ No hanging - requests are processed in order
- ✅ Production-ready

## 🎯 **Impact**

### **With 1 Replica:**
- **Before**: 1 concurrent request (others hang)
- **After**: 8 concurrent requests (properly queued)

### **With 3 Replicas:**
- **Before**: 3 concurrent requests (others hang)
- **After**: 24 concurrent requests (3 × 8)

## 🔧 **Deployment Steps**

1. **Update Dockerfile** (already done)
2. **Rebuild Docker image:**
   ```bash
   cd aca-executor
   docker build -t executor-secure:v16 .
   ```

3. **Push to ACR:**
   ```bash
   az acr login --name aitaraacr1763805702
   docker tag executor-secure:v16 aitaraacr1763805702.azurecr.io/executor-secure:v16
   docker push aitaraacr1763805702.azurecr.io/executor-secure:v16
   ```

4. **Update Terraform:**
   ```terraform
   executor_image = "aitaraacr1763805702.azurecr.io/executor-secure:v16"
   ```

5. **Deploy:**
   ```bash
   cd terraform
   terraform apply
   ```

## ✅ **Testing**

After deployment, test with 3 concurrent requests to 1 replica:

```bash
# All 3 should complete successfully (no hanging)
curl -X POST "https://..." -d '...' &
curl -X POST "https://..." -d '...' &
curl -X POST "https://..." -d '...' &
wait
```

**Expected Result:**
- ✅ All 3 requests complete
- ✅ No hanging
- ✅ Proper queue handling
- ✅ Responses returned in order

---

## 📝 **Summary**

**Problem**: Flask dev server = single-threaded = requests hang  
**Solution**: Gunicorn with 4 workers × 2 threads = 8 concurrent requests  
**Result**: Proper queue handling, no more hanging! ✅


