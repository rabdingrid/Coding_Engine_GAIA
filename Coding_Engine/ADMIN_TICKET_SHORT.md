# Quick Admin Request - Session Pool Ingress

## 🎯 Issue
404 errors when calling session pool - **ingress/target-port not configured**.

## 📋 Resource
- **Name**: `ai-ta-ra-session-pool`
- **Resource Group**: `ai-ta-2`
- **Required**: Enable ingress with **target-port = 2000**

## ✅ Action Needed
**Set target-port to 2000** in session pool configuration (Azure Portal or CLI).

**Portal Path**: Resource Groups → ai-ta-2 → ai-ta-ra-session-pool → Configuration → Target Port → Set to `2000`

**CLI Command**:
```bash
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

## 🧪 After Fix
Test: `curl -X POST "https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute" -H "Content-Type: application/json" -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'`

**Expected**: `{"run":{"stdout":"42\n","stderr":"","code":0}}`  
**Current**: `404 Not Found`

---

**Priority**: High  
**ETA**: 15-30 min


