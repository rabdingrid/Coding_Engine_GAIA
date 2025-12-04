# Enable External Ingress - Complete Guide

## ✅ You CAN Do This!

**Your Role**: Contributor ✅  
**Action**: Enable external ingress via Azure Portal

---

## 🎯 The Issue

- **Target Port**: Already set to 2000 ✅
- **External Ingress**: **NOT ENABLED** ❌
- **Result**: Backend cannot reach session pool → 404 errors

---

## 🔧 Step-by-Step: Enable External Ingress

### Step 1: Navigate to Session Pool
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Resource Groups** → `ai-ta-2`
3. Click on: **`ai-ta-ra-session-pool`**

### Step 2: Find Ingress/Networking Settings
Look for one of these sections (varies by Portal version):
- **"Configuration"** → **"Ingress"**
- **"Settings"** → **"Networking"** → **"Ingress"**
- **"Networking"** → **"Ingress"**
- **"Overview"** → **"Ingress"** (if visible)

### Step 3: Enable External Ingress
1. Find **"Ingress"** or **"External Ingress"** toggle/setting
2. Set to **"Enabled"** or **"External"**
3. Ensure **"Target Port"** shows **2000** (should already be set)
4. **Save** the changes

### Step 4: Wait for Propagation
- Wait **2-3 minutes** for changes to apply
- Check status shows **"Succeeded"**

---

## 📋 Verification

After enabling ingress, verify:

```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "{targetPort:properties.template.ingress.targetPort, ingressExternal:properties.template.ingress.external, status:properties.provisioningState}" \
  -o json
```

**Expected**:
```json
{
  "ingressExternal": true,
  "status": "Succeeded",
  "targetPort": 2000
}
```

---

## 🧪 Test After Fix

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

---

## ⚠️ If You Can't Find Ingress Settings in Portal

**Option 1: Check Different Portal Views**
- Try **"JSON View"** or **"Export template"**
- Look for `"ingress": { "external": false }` and change to `true`

**Option 2: Use REST API**
- More complex but guaranteed to work
- Requires authentication token

**Option 3: Ask Admin**
- If Portal doesn't show the option
- Admin with Owner role can do it

---

## ✅ Container Verification (Already Done)

- ✅ Container listens on port 2000
- ✅ Endpoint `/python/execute` exists
- ✅ Health endpoints `/health` and `/ready` exist
- ✅ Adapter service is running

**No container changes needed!**

---

## 📝 JIRA Ticket Response

**You can respond to the JIRA ticket**:

```
I have Contributor role and can enable ingress via Azure Portal.

Steps I'll take:
1. Navigate to session pool in Azure Portal
2. Enable External Ingress
3. Verify target-port = 2000
4. Save and test

If Portal doesn't show the ingress option, I'll need admin assistance.
```

---

**Status**: You can do this via Portal (Contributor role)  
**Action**: Enable external ingress in Azure Portal  
**If blocked**: Ask admin if Portal doesn't show the option


