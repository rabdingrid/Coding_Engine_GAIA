# Root Cause: 404 Error - Target Port Not Persisting

## 🔴 Problem

**Target Port**: Shows as `null` even after update  
**Error**: 404 "Not Found"  
**Cause**: Azure cannot route requests because target-port is not set

---

## ✅ What's Confirmed

1. ✅ Role assignment: Managed identity has executor role
2. ✅ Backend identity: UserAssigned managed identity configured
3. ✅ Backend code: Correct token audience
4. ✅ Adapter service: Route `/python/execute` correct
5. ❌ **Target Port**: Update command succeeded but query shows `null`

---

## 🔍 Why Target Port Matters

According to Azure docs:
- Azure forwards: `<POOL_ENDPOINT>/python/execute` → `0.0.0.0:<TARGET_PORT>/python/execute`
- If `targetPort` is `null`, Azure doesn't know where to forward
- Result: **404 Not Found**

---

## 🔧 Attempted Fix

```bash
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

**Result**: Command succeeded, but query still shows `null`

---

## 💡 Possible Causes

1. **Update didn't apply to active template**
   - Session pool might have active vs pending template
   - Need to check `templateUpdateStatus`

2. **Target port needs to be set during creation**
   - Update might not work for CustomContainer
   - Might need to recreate session pool

3. **Template structure issue**
   - Target port might be in different location
   - Need to check full template structure

---

## 🎯 Next Steps

### Option 1: Recreate Session Pool with Target Port
```bash
# Delete existing
az containerapp sessionpool delete --name ai-ta-ra-session-pool --resource-group ai-ta-2

# Create new with target-port
az containerapp sessionpool create \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --location eastus2 \
  --environment ai-ta-RA-env \
  --container-type CustomContainer \
  --image <IMAGE> \
  --target-port 2000 \
  --max-sessions 5 \
  --ready-sessions 1 \
  --cooldown-period 300
```

### Option 2: Check Template Update Status
```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.templateUpdateStatus" -o json
```

### Option 3: Use Azure Portal
- Check session pool configuration in portal
- Manually set target port to 2000
- Verify it persists

---

## 📋 Verification

After fixing target port:
1. Query should show: `"targetPort": 2000`
2. Test code execution
3. Should get successful response (not 404)

---

**Status**: Target port update not persisting - need to investigate why  
**Action**: Check template update status or recreate session pool with target-port


