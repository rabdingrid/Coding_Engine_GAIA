# Recreate Session Pool with Target Port - Complete Guide

## ✅ Steps to Fix 404 Error

The 404 error is caused by `targetPort: null`. Azure can't route requests without knowing which port to use.

---

## 🔧 Solution: Recreate Pool with Target Port

### Step 1: Delete Existing Pool
```bash
az containerapp sessionpool delete \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --yes
```

Wait for deletion to complete (1-2 minutes).

---

### Step 2: Create Pool with Target Port 2000
```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name aitaraacr1763805702 --resource-group ai-ta-2 --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name aitaraacr1763805702 --resource-group ai-ta-2 --query 'passwords[0].value' -o tsv)

# Create pool with target-port
az containerapp sessionpool create \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --location eastus2 \
  --environment ai-ta-RA-env \
  --container-type CustomContainer \
  --image aitaraacr1763805702.azurecr.io/session-image:final-fix \
  --target-port 2000 \
  --max-sessions 5 \
  --ready-sessions 1 \
  --cooldown-period 300 \
  --registry-server aitaraacr1763805702.azurecr.io \
  --registry-username "$ACR_USERNAME" \
  --registry-password "$ACR_PASSWORD" \
  --cpu 0.5 \
  --memory 1.0Gi
```

**Key parameter**: `--target-port 2000` ✅

---

### Step 3: Verify Target Port is Set
```bash
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.template.ingress.targetPort" \
  -o tsv
```

**Expected**: Should return `2000` (not `null`)

---

### Step 4: Wait for Pool to be Ready
```bash
# Check status
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "{readyCount:properties.templateUpdateStatus.activeTemplate.status.readyCount, status:properties.provisioningState}" \
  -o json
```

Wait until:
- `status`: `"Succeeded"`
- `readyCount`: `>= 1`

---

### Step 5: Test Code Execution
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

## ✅ What This Fixes

| Before | After |
|--------|-------|
| `targetPort: null` | `targetPort: 2000` ✅ |
| 404 Not Found | Should work ✅ |
| Azure can't route | Azure routes to port 2000 ✅ |

---

## 📋 Complete Script

Save this as `recreate_pool.sh`:

```bash
#!/bin/bash
set -e

RESOURCE_GROUP="ai-ta-2"
SESSION_POOL_NAME="ai-ta-ra-session-pool"
ENV_NAME="ai-ta-RA-env"
ACR_NAME="aitaraacr1763805702"
IMAGE="aitaraacr1763805702.azurecr.io/session-image:final-fix"

echo "Step 1: Deleting existing pool..."
az containerapp sessionpool delete \
  --name "$SESSION_POOL_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --yes

echo "Waiting for deletion..."
while az containerapp sessionpool show --name "$SESSION_POOL_NAME" --resource-group "$RESOURCE_GROUP" --query "properties.provisioningState" -o tsv 2>/dev/null | grep -q "Deleting"; do
  sleep 10
done
echo "✅ Deletion complete"

echo "Step 2: Creating pool with target-port 2000..."
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --query 'passwords[0].value' -o tsv)

az containerapp sessionpool create \
  --name "$SESSION_POOL_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --location eastus2 \
  --environment "$ENV_NAME" \
  --container-type CustomContainer \
  --image "$IMAGE" \
  --target-port 2000 \
  --max-sessions 5 \
  --ready-sessions 1 \
  --cooldown-period 300 \
  --registry-server "${ACR_NAME}.azurecr.io" \
  --registry-username "$ACR_USERNAME" \
  --registry-password "$ACR_PASSWORD" \
  --cpu 0.5 \
  --memory 1.0Gi

echo "Step 3: Waiting for pool to be ready..."
sleep 90

echo "Step 4: Verifying target-port..."
TARGET_PORT=$(az containerapp sessionpool show --name "$SESSION_POOL_NAME" --resource-group "$RESOURCE_GROUP" --query "properties.template.ingress.targetPort" -o tsv)
echo "Target Port: $TARGET_PORT"

if [ "$TARGET_PORT" = "2000" ]; then
  echo "✅ Target port is correctly set to 2000!"
else
  echo "❌ Target port is not 2000 (got: $TARGET_PORT)"
fi

echo "✅ Pool recreation complete!"
```

Make executable:
```bash
chmod +x recreate_pool.sh
./recreate_pool.sh
```

---

**Status**: Script ready to run  
**Next**: Execute script to recreate pool with target-port set


