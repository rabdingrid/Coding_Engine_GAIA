# IT Ticket: Azure Role Assignment Request

## 📋 Ticket Details

**Subject**: Azure Role Assignment - ContainerApps Session Executor for Coding Engine

**Priority**: Medium

**Category**: Azure / Cloud Infrastructure / Permissions

**Requested By**: Reyanul Abdin (rabdin@griddynamics.com)

**Date**: November 24, 2025

---

## 🎯 Request Summary

I need an Azure role assignment to enable our Coding Engine application to execute user-submitted code securely using Azure Dynamic Sessions.

**What I need**: Assign the "Azure ContainerApps Session Executor" role to our Managed Identity on the Session Pool resource.

---

## 📝 Detailed Request

### **Action Required:**

Assign the following role:

| Field | Value |
|-------|-------|
| **Role** | Azure ContainerApps Session Executor |
| **Assignee Type** | Managed Identity |
| **Managed Identity Name** | `ai-ta-RA-identity` |
| **Scope** | Session Pool: `ai-ta-RA-session-pool` |
| **Resource Group** | `ai-ta-2` |
| **Subscription** | `gd-azure-tools-ai_powered_ta_screening_tool` |
| **Subscription ID** | `dab771f2-8670-4bf4-8067-ea813decb669` |

---

## 🔧 Step-by-Step Instructions

### **Option 1: Azure Portal (Recommended)**

1. Go to **Azure Portal** (https://portal.azure.com)
2. Navigate to **Resource Groups** → `ai-ta-2`
3. Click on **`ai-ta-RA-session-pool`** (Session Pool resource)
4. In the left menu, click **Access Control (IAM)**
5. Click **+ Add** → **Add role assignment**
6. In the **Role** tab:
   - Search for: `Azure ContainerApps Session Executor`
   - Select it and click **Next**
7. In the **Members** tab:
   - Select **Managed Identity**
   - Click **+ Select members**
   - Filter by: **User-assigned managed identity**
   - Search for and select: `ai-ta-RA-identity`
   - Click **Select**
   - Click **Next**
8. In the **Review + assign** tab:
   - Review the details
   - Click **Review + assign**

### **Option 2: Azure CLI**

```bash
az role assignment create \
  --assignee "b84aa8c6-8ade-47e6-9c8c-b8c9ac2264fa" \
  --role "Azure ContainerApps Session Executor" \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-RA-session-pool"
```

**Managed Identity Details:**
- **Name**: `ai-ta-RA-identity`
- **Client ID**: `b84aa8c6-8ade-47e6-9c8c-b8c9ac2264fa`
- **Principal ID**: `2c7931f3-5fc4-4925-a064-60db35d1d3db`

---

## 💡 Business Justification

### **Purpose:**
This role assignment is required for our Coding Engine application to function. The application allows users to submit code (Python, Java, C++) which is executed securely in isolated Azure Dynamic Sessions containers.

### **Why This Role is Needed:**
- The Backend Container App (`ai-ta-ra-coding-engine`) needs to authenticate and send code execution requests to the Session Pool (`ai-ta-RA-session-pool`)
- The "Azure ContainerApps Session Executor" role grants the minimum permissions required to execute code in sessions
- Without this role, all code execution requests will fail with a 403 Forbidden error

### **Security:**
- This is a **least-privilege** role assignment
- The Managed Identity can **only** execute code in the specific Session Pool
- It **cannot** modify, delete, or access other Azure resources
- All executions are logged and auditable

### **Use Case:**
- **Coding contests** for technical assessments (similar to HackerRank)
- **Interview screening** for software engineering candidates
- **Practice platform** for algorithm and data structure problems

---

## 🔒 Security & Compliance

### **Permissions Granted:**
The "Azure ContainerApps Session Executor" role allows:
- ✅ Execute code in the specified Session Pool
- ✅ Read session status and results
- ❌ **Does NOT allow**: Creating/deleting sessions, modifying pool configuration, accessing other resources

### **Audit Trail:**
- All role assignments are logged in Azure Activity Log
- All code executions are logged in Log Analytics
- Managed Identity authentication is tracked in Azure AD logs

### **Compliance:**
- Follows **principle of least privilege**
- Uses **Managed Identity** (no passwords/keys stored)
- Aligns with Azure security best practices

---

## 📊 Resources Involved

| Resource Type | Resource Name | Purpose |
|---------------|---------------|---------|
| **Session Pool** | `ai-ta-RA-session-pool` | Executes user code in isolated containers |
| **Managed Identity** | `ai-ta-RA-identity` | Authenticates backend to session pool |
| **Backend App** | `ai-ta-ra-coding-engine` | Public API that routes code execution requests |
| **Container Registry** | `aitaraacr1763805702` | Stores Docker images |
| **Environment** | `ai-ta-RA-env` | Container Apps hosting environment |

All resources are in:
- **Resource Group**: `ai-ta-2`
- **Subscription**: `gd-azure-tools-ai_powered_ta_screening_tool`
- **Region**: East US 2

---

## ✅ Verification Steps

After the role is assigned, I will verify it works by:

1. Starting the Backend Container App
2. Sending a test code execution request:
   ```bash
   curl -X POST https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute \
     -H "Content-Type: application/json" \
     -d '{"language": "python", "version": "3.10.0", "files": [{"name": "main.py", "content": "print(\"Hello\")"}]}'
   ```
3. Expected result: `{"run": {"stdout": "Hello\n", "stderr": "", "code": 0}}`

---

## 📞 Contact Information

**Requester**: Reyanul Abdin  
**Email**: rabdin@griddynamics.com  
**Team**: AI-Powered TA Screening Tool  

**For Questions**:
- Technical details about the application architecture
- Security concerns about the role assignment
- Alternative approaches if this role cannot be granted

---

## 🚨 Impact if Not Granted

**Without this role assignment:**
- ❌ Coding Engine application **will not work**
- ❌ All code execution requests will fail with 403 Forbidden
- ❌ Cannot conduct coding contests or technical assessments
- ❌ $39 already spent on infrastructure will be wasted

**Timeline:**
- Infrastructure is already deployed and running
- Role assignment is the **only remaining blocker**
- Once assigned, application will be immediately functional

---

## 📎 Additional Resources

**Documentation:**
- [Azure ContainerApps Session Executor Role](https://learn.microsoft.com/en-us/azure/container-apps/sessions)
- [Managed Identity Best Practices](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)

**Deployment Details:**
- See attached: `Day1Progress.md` (deployment summary)
- See attached: `RESOURCE_STATE.md` (current resource state)
- See attached: `Backend_Architecture.md` (technical architecture)

---

## ✍️ Approval

**Requested By**: Reyanul Abdin  
**Date**: November 24, 2025  
**Approved By**: ________________  
**Date**: ________________  

---

**Thank you for your assistance!**
