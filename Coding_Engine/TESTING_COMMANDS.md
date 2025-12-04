# Testing Commands - Correct URLs

## ✅ Actual Endpoints

### Session Pool Endpoint:
```
https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io
```

### Backend Endpoint:
```
https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io
```

---

## 🧪 Test Commands

### Option 1: Test via Backend API (Recommended)

This is the easiest way - the backend handles authentication:

```bash
curl -X POST "https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "version": "3.11",
    "files": [{"content": "print(42)"}],
    "stdin": "",
    "args": []
  }'
```

**Expected Response**:
```json
{
  "run": {
    "stdout": "42\n",
    "stderr": "",
    "code": 0
  },
  "language": "python",
  "version": "3.11"
}
```

---

### Option 2: Test Direct Session Pool (Requires Auth Token)

First, get a token:
```bash
TOKEN=$(az account get-access-token --resource https://dynamicsessions.io --query accessToken -o tsv)
```

Then call the session pool:
```bash
curl -X POST "https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io/python/execute?identifier=test-session-1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "code": "print(42)",
      "stdin": ""
    }
  }'
```

---

## ❌ Common Mistakes

### Wrong (Placeholder URLs):
```bash
# DON'T USE - These are placeholders:
curl ... "https://ai-ta-ra-session-pool.<region>.azurecontainerapps.io/..."
curl ... "http://<your-backend-url>/execute"
```

### Correct (Actual URLs):
```bash
# USE - These are real endpoints:
curl ... "https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io/..."
curl ... "https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute"
```

---

## 📋 Quick Test Script

Save this as `test_execution.sh`:

```bash
#!/bin/bash

BACKEND_URL="https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io"

echo "Testing code execution..."
curl -X POST "${BACKEND_URL}/api/v2/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "version": "3.11",
    "files": [{"content": "print(\"Hello from Azure Session Pool!\")"}],
    "stdin": "",
    "args": []
  }' | python3 -m json.tool
```

Make it executable:
```bash
chmod +x test_execution.sh
./test_execution.sh
```

---

## 🔧 Current Issue: 404 Error

If you're getting 404, it's because:
- Target port is not set (shows as `null`)
- Azure can't route to the container

**Fix**: Set target-port to 2000 in Azure Portal or recreate pool with target-port.

---

**Last Updated**: After stable identifier fix  
**Status**: Commands ready, need to fix target-port for 404


