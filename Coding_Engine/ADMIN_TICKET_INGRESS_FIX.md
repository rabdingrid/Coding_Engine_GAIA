# Admin Ticket: Enable Ingress for Azure Session Pool

## 🎯 Issue Summary

**Problem**: 404 errors when backend calls Azure Session Pool  
**Root Cause**: Ingress not enabled / Target port not configured  
**Impact**: Code execution fails - cannot run code in session pool

---

## 📋 Resource Details

| Field | Value |
|-------|-------|
| **Resource Name** | `ai-ta-ra-session-pool` |
| **Resource Group** | `ai-ta-2` |
| **Subscription** | `dab771f2-8670-4bf4-8067-ea813decb669` |
| **Environment** | `ai-ta-RA-env` |
| **Pool Endpoint** | `https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io` |
| **Required Target Port** | `2000` |
| **Container Type** | `CustomContainer` |

---

## 🔍 Current Status

**Verification Command**:
```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.template.ingress.targetPort" \
  -o tsv
```

**Current Result**: `null` ❌  
**Required Result**: `2000` ✅

---

## ✅ Requested Action

### **Action 1: Enable Ingress with Target Port 2000**

The session pool needs ingress enabled with target port set to **2000**.

**Option A: Via Azure Portal** (Recommended)
1. Navigate to: **Resource Groups** → `ai-ta-2` → `ai-ta-ra-session-pool`
2. Go to **Configuration** or **Settings** section
3. Find **Ingress** or **Target Port** setting
4. Set **Target Port** to `2000`
5. Enable **Ingress** if not already enabled
6. Save changes

**Option B: Via Azure CLI**
```bash
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

**Note**: If CLI doesn't support `--target-port`, please use Portal method.

---

### **Action 2: Verify Container Configuration**

Please confirm:
- ✅ Container is listening on port `2000`
- ✅ Container exposes endpoint `/python/execute`
- ✅ Container has health endpoints `/health` and `/ready`

**Container Image**: `aitaraacr1763805702.azurecr.io/session-image:final-fix`

---

## 🧪 Testing After Fix

Once ingress is enabled, we will test:

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
  }
}
```

**Current Response** (404 error):
```json
{
  "run": {
    "stderr": "404 Client Error: Not Found for url: .../python/execute?identifier=test-session-1",
    "code": 1
  }
}
```

---

## 📊 Technical Details

### Why Target Port is Required

Azure Session Pool routes requests like this:
```
Backend → Session Pool Endpoint → Container at port <TARGET_PORT>
```

Without target-port:
- Azure doesn't know which port to forward to
- Requests get 404 "Not Found"
- Container never receives requests

With target-port=2000:
- Azure forwards to `0.0.0.0:2000/python/execute`
- Container receives requests ✅
- Code executes successfully ✅

---

## ✅ Verification Checklist

After fix is applied, please verify:

- [ ] Target port shows as `2000` (not `null`)
- [ ] Ingress is enabled
- [ ] Session pool status is "Succeeded"
- [ ] Ready sessions count >= 1

**Verification Command**:
```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "{targetPort:properties.template.ingress.targetPort, status:properties.provisioningState, readyCount:properties.templateUpdateStatus.activeTemplate.status.readyCount}" \
  -o json
```

---

## 📝 Additional Context

- **Backend Service**: `ai-ta-ra-coding-engine` (already configured correctly)
- **Role Assignment**: ✅ Already assigned at resource group level
- **Container Image**: ✅ Already deployed and correct
- **Backend Code**: ✅ Already fixed to use identifier-based flow
- **Only Missing**: Target port configuration

---

## 🎯 Priority

**High** - This is blocking code execution functionality.

---

## 📞 Contact

Please notify once ingress is enabled so we can retest.

**Thank you!**

---

**Ticket Created**: 2025-11-26  
**Status**: Awaiting admin action  
**Expected Resolution Time**: 15-30 minutes


