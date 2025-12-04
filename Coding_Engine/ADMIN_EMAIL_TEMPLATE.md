# Email Template for Admin

---

**Subject**: Action Required: Enable Ingress for Azure Session Pool (ai-ta-ra-session-pool)

---

Hi [Admin Name],

We're experiencing **404 errors** when our backend service calls the Azure Container App session pool. After investigation, the root cause is that **ingress is not enabled** or **target-port is not set**, so Azure cannot route requests to the container.

**Resource Details:**
- **Resource Name**: `ai-ta-ra-session-pool`
- **Resource Group**: `ai-ta-2`
- **Environment**: `ai-ta-RA-env`
- **Pool Endpoint**: `https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Required Target Port**: `2000`

**Requested Action:**

Please enable ingress and set **target-port to 2000** for the session pool.

**Option 1: Azure Portal** (Recommended)
1. Navigate to: Resource Groups → `ai-ta-2` → `ai-ta-ra-session-pool`
2. Go to **Configuration** section
3. Find **Target Port** or **Ingress** setting
4. Set **Target Port** to `2000`
5. Enable **Ingress** if not already enabled
6. Save changes

**Option 2: Azure CLI**
```bash
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

**Verification:**
After the change, please verify target-port is set:
```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.template.ingress.targetPort" \
  -o tsv
```
Should return: `2000` (not `null`)

**Testing:**
Once ingress is enabled, we will test:
```bash
curl -X POST "https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'
```

**Expected Result**: `{"run":{"stdout":"42\n","stderr":"","code":0}}`  
**Current Result**: `404 Not Found` error

**Priority**: High - This is blocking code execution functionality.

Please let me know once ingress is enabled so we can retest.

Thanks,  
[Your Name]

---


