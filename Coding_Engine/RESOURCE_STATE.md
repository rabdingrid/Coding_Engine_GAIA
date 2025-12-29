# Resource State Snapshot - November 24, 2025

## 🎯 Current State: ALL RESOURCES STOPPED

### **Resources Status:**

| Resource | Status | Cost (when stopped) |
|----------|--------|---------------------|
| Container Registry (ACR) | ✅ RUNNING | $0.17/day |
| Container Apps Environment | ✅ RUNNING | $0.10/day |
| Managed Identity | ✅ EXISTS | $0.00/day |
| Session Pool | ❌ DELETED | $0.00/day |
| Backend Container App | ❌ DELETED | $0.00/day |
| **TOTAL** | | **$0.27/day** |

---

## 📝 Resource Details

### **1. Container Registry**
- **Name**: `aitaraacr1763805702`
- **Login Server**: `aitaraacr1763805702.azurecr.io`
- **Images Stored**:
  - `session-image:v1` (1.2 GB) - Python, Java pre-installed
  - `backend-image:v1` (150 MB) - FastAPI application
- **Status**: RUNNING (keep running - minimal cost)

### **2. Container Apps Environment**
- **Name**: `ai-ta-RA-env`
- **Location**: East US 2
- **Log Analytics**: `workspace-aita221pA`
- **Status**: RUNNING (keep running - no cost)

### **3. Managed Identity**
- **Name**: `ai-ta-RA-identity`
- **Client ID**: `b84aa8c6-8ade-47e6-9c8c-b8c9ac2264fa`
- **Principal ID**: `2c7931f3-5fc4-4925-a064-60db35d1d3db`
- **Status**: EXISTS (no cost)

### **4. Session Pool**
- **Name**: `ai-ta-RA-session-pool`
- **Status**: ❌ DELETED (Nov 24, 2025 - to save costs)
- **Reason**: Was costing $36 for 48 hours due to `ready-sessions: 1`
- **Recreation**: Use `./manage_resources.sh start-session-pool`

### **5. Backend Container App**
- **Name**: `ai-ta-ra-coding-engine`
- **Status**: ❌ DELETED (Nov 24, 2025 - to save costs)
- **Previous URL**: `https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Recreation**: Use `./manage_resources.sh start-backend`

---

## 🚀 How to Restart Everything

### **Quick Start (Development/Testing):**
```bash
./manage_resources.sh start-all
```
This will:
1. Create Session Pool (cost-optimized: `ready-sessions: 0`)
2. Create Backend Container App (1-3 replicas)
3. **Cost**: ~$1.57/day when idle

### **Contest Mode (200 users):**
```bash
./manage_resources.sh contest-start
```
This will:
1. Create Session Pool with 50 max sessions, 5 ready sessions
2. Scale Backend to 2-10 replicas
3. **Cost**: ~$10-15 for 2-hour contest

### **Stop Everything:**
```bash
./manage_resources.sh stop-all
```

---

## 💰 Cost History

### **Nov 22-24 (48 hours):**
- **Session Pool**: $36 (due to `ready-sessions: 1` running 24/7)
- **Backend App**: ~$2.59
- **ACR**: ~$0.33
- **Environment**: ~$0.20
- **Total**: ~$39.12

### **Lessons Learned:**
1. ❌ **Never use `ready-sessions > 0` unless actively needed**
2. ✅ **Use `ready-sessions: 0` for cost-optimized idle state**
3. ✅ **Scale up only before contests, scale down immediately after**
4. ✅ **Delete resources when not in use for extended periods**

---

## 📋 Deployment Commands Reference

### **Create Session Pool (Cost-Optimized):**
```bash
az containerapp sessionpool create \
  --name ai-ta-RA-session-pool \
  --resource-group ai-ta-2 \
  --environment ai-ta-RA-env \
  --container-type CustomContainer \
  --image aitaraacr1763805702.azurecr.io/session-image:v1 \
  --target-port 2000 \
  --max-sessions 10 \
  --ready-sessions 0 \
  --cooldown-period 60 \
  --registry-server aitaraacr1763805702.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD> \
  --cpu 0.5 --memory 1.0Gi
```

### **Create Backend Container App:**
```bash
# Get Pool Endpoint first
POOL_ENDPOINT=$(az containerapp sessionpool show \
  --name ai-ta-RA-session-pool \
  --resource-group ai-ta-2 \
  --query properties.poolManagementEndpoint -o tsv)

# Create Backend
az containerapp create \
  --name ai-ta-ra-coding-engine \
  --resource-group ai-ta-2 \
  --environment ai-ta-RA-env \
  --image aitaraacr1763805702.azurecr.io/backend-image:v1 \
  --target-port 8000 \
  --ingress external \
  --user-assigned /subscriptions/.../ai-ta-RA-identity \
  --registry-server aitaraacr1763805702.azurecr.io \
  --registry-username <ACR_USERNAME> \
  --registry-password <ACR_PASSWORD> \
  --env-vars "POOL_MANAGEMENT_ENDPOINT=$POOL_ENDPOINT" "AZURE_CLIENT_ID=b84aa8c6-8ade-47e6-9c8c-b8c9ac2264fa" \
  --min-replicas 1 \
  --max-replicas 3
```

---

## ⚠️ Important Notes

### **Role Assignment Still Pending:**
The Managed Identity needs the "Azure ContainerApps Session Executor" role. Ask your admin to run:
```bash
az role assignment create \
  --assignee "b84aa8c6-8ade-47e6-9c8c-b8c9ac2264fa" \
  --role "Azure ContainerApps Session Executor" \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-RA-session-pool"
```

### **PostgreSQL Mystery ($37):**
A PostgreSQL database is consuming $37 but was NOT created by our deployment. Check with your team to identify this resource.

---

## 📁 Related Files

- **`manage_resources.sh`**: Main resource management script
- **`SessionPool_Architecture.md`**: Detailed architecture explanation
- **`Day1Progress.md`**: Initial deployment summary
- **`deploy_org.sh`**: Original deployment script (for reference)

---

**Last Updated**: November 24, 2025, 4:08 PM IST  
**Status**: All resources stopped to minimize costs  
**Daily Cost**: $0.27/day ($8/month)
