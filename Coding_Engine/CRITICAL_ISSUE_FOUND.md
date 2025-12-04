# Critical Issue Found: Target Port is NULL

## 🔴 Problem Identified

**Target Port**: `null` ❌  
**Impact**: Azure cannot route requests to the container

### What This Means

According to Azure docs:
- Azure forwards requests to: `0.0.0.0:<TARGET_PORT>/<path>`
- If `targetPort` is `null`, Azure doesn't know which port to forward to
- This causes **404 Not Found** errors

---

## ✅ What's Confirmed

1. ✅ **Role Assignment**: Managed identity has "Azure ContainerApps Session Executor" role
2. ✅ **Backend Code**: Correct token audience (`https://dynamicsessions.io/.default`)
3. ✅ **Adapter Service**: Route `/python/execute` is correct
4. ✅ **Session Pool**: Running with 1 ready session
5. ❌ **Target Port**: **NULL** (this is the blocker!)

---

## 🔧 Fix Applied

Setting target-port to 2000 (the port the adapter service listens on):

```bash
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

---

## 🎯 Why This Will Fix It

1. **Before**: `targetPort = null` → Azure doesn't know where to route → 404
2. **After**: `targetPort = 2000` → Azure routes to `0.0.0.0:2000/python/execute` → Adapter receives request → Code executes

---

## 📋 Verification Steps

After target-port is set:

1. Wait 30-60 seconds for update to propagate
2. Verify: `az containerapp sessionpool show ... --query "properties.template.ingress.targetPort"` should return `2000`
3. Test code execution
4. Should get successful response with code output

---

## ✅ Expected Result After Fix

```json
{
  "run": {
    "stdout": "42\n",
    "stderr": "",
    "code": 0
  }
}
```

---

**Status**: Target port being set - this should fix the 404 errors  
**Confidence**: 90% - This is the missing piece


