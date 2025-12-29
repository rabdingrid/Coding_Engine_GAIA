# How to Enable Ingress - Step by Step Guide

## ✅ You CAN Do This!

**Your Role**: Contributor ✅  
**Method**: Azure Portal (most reliable)

---

## 🔧 Step-by-Step: Enable Ingress via Azure Portal

### Step 1: Navigate to Session Pool
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Resource Groups** → `ai-ta-2`
3. Click on: **`ai-ta-ra-session-pool`**

### Step 2: Find Configuration/Settings
Look for one of these sections:
- **Configuration** (most likely)
- **Settings** → **Configuration**
- **Ingress** (if visible directly)
- **Networking** → **Ingress**

### Step 3: Enable Ingress and Set Target Port
1. Find **"Ingress"** or **"External Ingress"** toggle
   - Enable it (set to **"Enabled"** or **"External"**)
2. Find **"Target Port"** field
   - Set to **`2000`**
3. **Save** the changes

### Step 4: Wait for Update
- Wait 1-2 minutes for changes to apply
- Check status shows "Succeeded"

---

## 🔍 Alternative: Check Template/JSON View

If you can't find the UI settings:

1. In the session pool resource, look for:
   - **"JSON View"** or **"Export template"**
   - Or go to **"Overview"** → **"JSON View"**

2. Look for this section:
   ```json
   "template": {
     "ingress": {
       "external": true,
       "targetPort": 2000
     }
   }
   ```

3. If it's missing or `null`, you may need to use **ARM template** or **REST API**

---

## 📋 Verification After Fix

Run this to verify:
```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "{targetPort:properties.template.ingress.targetPort, ingressExternal:properties.template.ingress.external}" \
  -o json
```

**Expected**:
```json
{
  "ingressExternal": true,
  "targetPort": 2000
}
```

---

## 🧪 Test After Fix

```bash
curl -X POST "https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'
```

**Expected**: `{"run":{"stdout":"42\n","stderr":"","code":0}}`

---

## ⚠️ If Portal Doesn't Show These Options

**Option 1: Use ARM Template**
- Export current template
- Modify `ingress` section
- Deploy updated template

**Option 2: Use REST API**
- Direct API call to update session pool
- More complex but guaranteed to work

**Option 3: Recreate Pool**
- Delete and recreate with ingress enabled during creation
- Most reliable method

---

## ✅ Container Verification (Already Done)

- ✅ Container listens on port 2000
- ✅ Endpoint `/python/execute` exists
- ✅ Health endpoints `/health` and `/ready` exist
- ✅ Adapter service is running

**No changes needed to container** - it's already correct!

---

**Status**: You have permissions, use Azure Portal to enable ingress  
**Priority**: High - This will fix the 404 errors


