# Admin Role Requirements - Session Pool Configuration

## 🎯 Required Role to Set Target Port

To enable ingress and set target-port on the session pool, the admin needs one of these roles:

### **Option 1: Owner** (Recommended)
- **Scope**: Resource Group or Subscription
- **Permissions**: Full access, can modify all resources
- **Can do**: Everything including setting target-port

### **Option 2: Contributor**
- **Scope**: Resource Group or Subscription
- **Permissions**: Can modify resources (but not manage access)
- **Can do**: Set target-port, modify session pool configuration

### **Option 3: Azure Container Apps Contributor**
- **Scope**: Resource Group or Subscription
- **Permissions**: Specific to Container Apps resources
- **Can do**: Set target-port, modify Container Apps and Session Pools

---

## 📋 Specific Permission Needed

**Action**: `Microsoft.App/sessionPools/write`  
**Resource**: `/subscriptions/.../resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-ra-session-pool`

---

## ✅ How to Check Admin's Current Role

```bash
# Check roles at resource group level
az role assignment list \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2" \
  --query "[].{Principal:principalName, Role:roleDefinitionName}" \
  -o table
```

---

## 🔧 If Admin Doesn't Have Required Role

**Request to Subscription/Resource Group Owner**:

```
Please assign one of these roles to [admin-email]:
- Owner
- Contributor  
- Azure Container Apps Contributor

Scope: /subscriptions/.../resourceGroups/ai-ta-2

This is needed to configure the session pool target-port.
```

---

## 📝 Quick Reference

| Role | Can Set Target-Port? | Can Manage Access? |
|------|---------------------|-------------------|
| **Owner** | ✅ Yes | ✅ Yes |
| **Contributor** | ✅ Yes | ❌ No |
| **Azure Container Apps Contributor** | ✅ Yes | ❌ No |
| **Reader** | ❌ No | ❌ No |

---

**Resource**: `ai-ta-ra-session-pool` in resource group `ai-ta-2`  
**Action Needed**: Set target-port to 2000  
**Required Permission**: `Microsoft.App/sessionPools/write`


