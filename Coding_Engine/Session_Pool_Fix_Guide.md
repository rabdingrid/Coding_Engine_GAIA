# Session Pool Code Execution Fix Guide

## 🔍 Problem Analysis

### Current Issue: HTTP 404 "Not Found"

**Symptoms:**
- Backend successfully connects to session pool (HTTP 200 auth)
- But execution requests return HTTP 404
- Error: `{"message":"Not Found"}`

**Root Cause Investigation:**

1. **Backend Request Format:**
   ```python
   url = f"{POOL_MANAGEMENT_ENDPOINT}/python/execute?api-version=2024-02-02-preview&identifier={session_id}"
   ```

2. **Adapter Service Route Matching:**
   ```javascript
   const executeMatch = pathname.match(/^\/(\w+)\/execute$/);
   // Should match: /python/execute
   ```

3. **Possible Issues:**
   - ✅ Route matching should work (pathname strips query params)
   - ❌ Adapter service might not be running in v1 image
   - ❌ Piston might not be starting, causing adapter to fail
   - ❌ Image might not have correct adapter-service.js file

---

## 🔧 How Azure Dynamic Sessions Executes Code

### Execution Flow:

```
1. Backend → Azure AD Auth → Get Token
2. Backend → Session Pool Endpoint → POST /python/execute
3. Session Pool → Allocates/Reuses Session Container
4. Session Container → Adapter Service (port 2000)
5. Adapter Service → Piston API (localhost:2001)
6. Piston → Executes Code in Sandbox
7. Piston → Returns stdout/stderr
8. Adapter → Translates to Azure Format
9. Adapter → Returns to Session Pool
10. Session Pool → Returns to Backend
```

### Key Components in Session Container:

1. **Piston API** (port 2000, forwarded to 2001)
   - Runs: `node /piston_api/src/index.js`
   - Handles actual code execution

2. **Adapter Service** (port 2000, Azure endpoint)
   - Runs: `node /app/adapter-service.js`
   - Translates Azure format ↔ Piston format
   - Routes: `/python/execute`, `/cpp/execute`, etc.

3. **Startup Script** (`/app/start.sh`)
   - Starts Piston
   - Waits for Piston to be ready
   - Sets up port forwarding (socat)
   - Starts adapter service

---

## 🛠️ Fix Steps

### Step 1: Verify Image Contents

Check if `session-image:v1` has the correct files:

```bash
# The image should contain:
# - /app/adapter-service.js (full version, not minimal)
# - /app/start.sh (startup script)
# - /piston_api/ (Piston installation)
```

### Step 2: Check Session Container Logs

```bash
# Get session pool logs (if available)
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.templateUpdateStatus.activeTemplate.status"
```

### Step 3: Test Adapter Service Directly

The adapter should respond to:
- `GET /` → Status info
- `GET /health` → "ok"
- `POST /python/execute` → Execute code

### Step 4: Verify Piston is Running

The adapter calls Piston at `localhost:2001`. If Piston isn't running:
- Adapter will fail with connection error
- Should return 500, not 404

**404 suggests**: Route not matching or adapter not running at all

---

## 🔍 Debugging Steps

### 1. Check Which Image is Actually Deployed

```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.template.containers[0].image" -o tsv
```

### 2. Test Session Pool Endpoint Directly

```bash
# This should return 403 (auth required) or 404 (if adapter not running)
curl -X POST https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io/python/execute \
  -H "Content-Type: application/json" \
  -d '{"properties":{"code":"print(1)"}}'
```

### 3. Check Backend Logs for Full Error

```bash
az containerapp logs show \
  --name ai-ta-ra-coding-engine \
  --resource-group ai-ta-2 \
  --tail 50 \
  | grep -E "(404|Not Found|EXECUTE)"
```

### 4. Verify Adapter Service Route Matching

The adapter uses:
```javascript
const parsedUrl = url.parse(req.url, true);
const pathname = parsedUrl.pathname;  // Should be "/python/execute"
const executeMatch = pathname.match(/^\/(\w+)\/execute$/);
```

This should match `/python/execute` even with query params.

---

## 🎯 Recommended Fix

### Option 1: Use Working Image Tag

Try a different image tag that's known to work:
- `session-image:working`
- `session-image:fixed`
- `session-image:final-fix`

### Option 2: Rebuild and Redeploy

1. **Verify Dockerfile.session** has correct adapter:
   ```dockerfile
   COPY adapter-service.js /app/adapter-service.js  # NOT minimal
   ```

2. **Build new image:**
   ```bash
   docker build -f Dockerfile.session -t session-image:test-fix .
   ```

3. **Push to ACR:**
   ```bash
   az acr login --name aitaraacr1763805702
   docker tag session-image:test-fix aitaraacr1763805702.azurecr.io/session-image:test-fix
   docker push aitaraacr1763805702.azurecr.io/session-image:test-fix
   ```

4. **Update session pool:**
   ```bash
   az containerapp sessionpool update \
     --name ai-ta-ra-session-pool \
     --resource-group ai-ta-2 \
     --image aitaraacr1763805702.azurecr.io/session-image:test-fix
   ```

### Option 3: Add Debug Logging

Modify adapter-service.js to log all requests:
```javascript
console.log(`[${new Date().toISOString()}] ${req.method} ${pathname} - Full URL: ${req.url}`);
```

---

## 📋 Testing After Fix

1. **Wait for sessions to initialize** (30-60 seconds)
2. **Test simple execution:**
   ```bash
   curl -X POST https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute \
     -H "Content-Type: application/json" \
     -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'
   ```

3. **Expected response:**
   ```json
   {
     "run": {
       "stdout": "42\n",
       "stderr": "",
       "code": 0
     }
   }
   ```

4. **Run full test suite:**
   ```bash
   python test_session_pool.py --endpoint https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io
   ```

---

## 💡 Quick Fix: Try Different Image

Since we have multiple image tags, try the "working" tag:

```bash
ACR_USERNAME=$(az acr credential show --name aitaraacr1763805702 --resource-group ai-ta-2 --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name aitaraacr1763805702 --resource-group ai-ta-2 --query 'passwords[0].value' -o tsv)

az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --image aitaraacr1763805702.azurecr.io/session-image:working \
  --max-sessions 5 \
  --ready-sessions 1 \
  --registry-server aitaraacr1763805702.azurecr.io \
  --registry-username "$ACR_USERNAME" \
  --registry-password "$ACR_PASSWORD"
```

---

**Status**: Investigation in progress  
**Next Step**: Try "working" image tag or rebuild with verified adapter service


