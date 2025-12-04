# Your Access Roles

## 👤 Your Account
**Email**: `rabdin@griddynamics.com`

---

## ✅ Your Current Roles

### At Resource Group Level (`ai-ta-2`):
- **Contributor** ✅

**What this means**:
- ✅ Can modify all resources in the resource group
- ✅ Can set target-port on session pool
- ✅ Can create/update/delete resources
- ❌ Cannot manage access (role assignments)

---

## 🔍 Role Details

### **Contributor Role Permissions**:
- ✅ **Microsoft.App/sessionPools/write** - Can modify session pools
- ✅ **Microsoft.App/containerApps/write** - Can modify container apps
- ✅ **Microsoft.App/environments/write** - Can modify environments
- ✅ **Microsoft.ContainerRegistry/registries/write** - Can modify ACR
- ❌ **Microsoft.Authorization/roleAssignments/write** - Cannot assign roles

---

## ✅ What You CAN Do

1. ✅ **Set target-port on session pool** (via Portal or CLI)
2. ✅ **Modify session pool configuration**
3. ✅ **Create/update/delete resources** in resource group
4. ✅ **Deploy container apps**
5. ✅ **Update backend configurations**

---

## ❌ What You CANNOT Do

1. ❌ **Assign roles** to other users
2. ❌ **Remove role assignments**
3. ❌ **Change subscription-level settings**

---

## 🎯 For Setting Target Port

**You have sufficient permissions!** ✅

As a **Contributor**, you can:
- Set target-port via Azure Portal
- Update session pool configuration
- Modify ingress settings

**You don't need admin help** - you can do it yourself!

---

## 📋 How to Set Target Port (You Can Do This)

### Option 1: Azure Portal
1. Go to: Resource Groups → `ai-ta-2` → `ai-ta-ra-session-pool`
2. Navigate to **Configuration** or **Settings**
3. Find **Target Port** or **Ingress** section
4. Set to `2000`
5. Save

### Option 2: Azure CLI (If Supported)
```bash
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

---

## 📊 Role Comparison

| Action | Your Role (Contributor) | Owner | Reader |
|--------|------------------------|-------|--------|
| **Set target-port** | ✅ Yes | ✅ Yes | ❌ No |
| **Modify resources** | ✅ Yes | ✅ Yes | ❌ No |
| **Assign roles** | ❌ No | ✅ Yes | ❌ No |
| **View resources** | ✅ Yes | ✅ Yes | ✅ Yes |

---

**Status**: You have Contributor role - sufficient to set target-port  
**Action**: You can set target-port yourself via Portal or CLI


