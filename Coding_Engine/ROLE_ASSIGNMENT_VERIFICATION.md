# Role Assignment Verification

## ✅ Verification Results

### Check 1: Resource Group Level
```bash
az role assignment list \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2" \
  --assignee "2c7931f3-5fc4-4925-a064-60db35d1d3db" \
  --role "Azure ContainerApps Session Executor"
```

**Expected**: Should show role assignment at resource group level (persists across pool deletions)

---

### Check 2: Session Pool Level
```bash
az role assignment list \
  --scope "/subscriptions/dab771f2-8670-4bf4-8067-ea813decb669/resourceGroups/ai-ta-2/providers/Microsoft.App/sessionPools/ai-ta-ra-session-pool" \
  --assignee "2c7931f3-5fc4-4925-a064-60db35d1d3db" \
  --role "Azure ContainerApps Session Executor"
```

**Expected**: May be empty (if only assigned at RG level) or may show assignment (if assigned at both levels)

---

### Check 3: All Assignments for Principal
```bash
az role assignment list \
  --assignee "2c7931f3-5fc4-4925-a064-60db35d1d3db" \
  --query "[?roleDefinitionName=='Azure ContainerApps Session Executor']"
```

**Expected**: Should show all executor role assignments for this principal

---

## 📊 Assignment Levels

| Level | Scope | Persists? | Use Case |
|-------|-------|-----------|----------|
| **Resource Group** | `/subscriptions/.../resourceGroups/ai-ta-2` | ✅ Yes | Survives pool deletion/recreation |
| **Session Pool** | `/subscriptions/.../sessionPools/ai-ta-ra-session-pool` | ❌ No | Deleted when pool is deleted |

---

## ✅ Expected Result

**Resource Group Level Assignment**:
- ✅ Scope: `/subscriptions/.../resourceGroups/ai-ta-2`
- ✅ Role: `Azure ContainerApps Session Executor`
- ✅ Principal: `2c7931f3-5fc4-4925-a064-60db35d1d3db`
- ✅ **This assignment will persist** even if session pool is deleted/recreated

---

## 🧪 Test After Verification

If role is assigned correctly, code execution should work:

```bash
curl -X POST https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute \
  -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'
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

**Last Checked**: Running verification now...


