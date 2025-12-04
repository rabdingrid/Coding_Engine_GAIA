# Role Assignment Fix - Azure Session Pool 403 Error

## 🔍 Problem: HTTP 403 "Unauthenticated"

**Status**: Request reaches Azure correctly, but authentication fails.

### Root Cause
The managed identity `ai-ta-RA-identity` (Principal ID: `2c7931f3-5fc4-4925-a064-60db35d1d3db`) does **NOT** have the **"Azure ContainerApps Session Executor"** role assigned to the session pool.

---

## ✅ Backend Code is CORRECT

The backend is already using the correct token format:

```python
def get_auth_token():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://dynamicsessions.io/.default")
    return token.token
```

✅ **Correct audience**: `https://dynamicsessions.io/.default`  
✅ **Correct method**: Using `DefaultAzureCredential()` for Managed Identity  
✅ **Token included**: In `Authorization: Bearer <token>` header

---

## 🔧 Fix Required: Assign Role

### Step 1: Assign Role to Managed Identity

**Run this command** (requires User Access Administrator or Owner permissions):

```bash
az role assignment create \
  --assignee "2c7931f3-5fc4-4925-a064-60db35d1d3db" \
  --role "Azure ContainerApps Session Executor" \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-ra-session-pool"
```

**Important**: 
- The scope must be the **session pool resource**, not the resource group
- The assignee is the **Principal ID** of the managed identity

### Step 2: Verify Role Assignment

```bash
az role assignment list \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-ra-session-pool" \
  --query "[?roleDefinitionName=='Azure ContainerApps Session Executor']" \
  -o table
```

### Step 3: Wait for Propagation

Role assignments can take 1-5 minutes to propagate. Wait a few minutes after assignment.

### Step 4: Test

```bash
curl -X POST https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute \
  -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'
```

**Expected**: Should return `{"run":{"stdout":"42\n","stderr":"","code":0}}`

---

## 📋 Current Configuration

### Managed Identity
- **Name**: `ai-ta-RA-identity`
- **Principal ID**: `2c7931f3-5fc4-4925-a064-60db35d1d3db`
- **Status**: ✅ Assigned to backend container app

### Session Pool
- **Name**: `ai-ta-ra-session-pool`
- **Resource ID**: `/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-ra-session-pool`
- **Status**: ✅ Running (1 ready session)

### Backend
- **Name**: `ai-ta-ra-coding-engine`
- **Token Audience**: ✅ `https://dynamicsessions.io/.default` (correct)
- **Status**: ✅ Running

---

## ✅ What's Already Fixed

1. ✅ **Backend code**: Correct token generation
2. ✅ **Payload format**: Matches adapter service
3. ✅ **URL format**: Correct per Azure docs
4. ✅ **Session pool**: Created with target-port 2000
5. ✅ **Container image**: Using `session-image:final-fix` with adapter service

---

## ❌ What's Missing

1. ❌ **Role Assignment**: Managed identity needs "Azure ContainerApps Session Executor" role

---

## 🎯 After Role Assignment

Once the role is assigned, code execution should work:

1. Backend gets token with correct audience ✅
2. Backend sends request with Authorization header ✅
3. Azure validates token and role ✅ (will work after assignment)
4. Azure routes to session container ✅
5. Container adapter service receives request ✅
6. Adapter forwards to Piston ✅
7. Code executes ✅
8. Results returned ✅

---

## 📝 Quick Fix Command

**Copy and run this** (requires admin permissions):

```bash
az role assignment create \
  --assignee "2c7931f3-5fc4-4925-a064-60db35d1d3db" \
  --role "Azure ContainerApps Session Executor" \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-ra-session-pool"
```

Then wait 2-3 minutes and test again.

---

**Status**: Backend code correct, role assignment needed  
**Action Required**: Assign role (requires admin permissions)  
**After Fix**: Code execution should work immediately


