# ✅ CORRECTED Admin Message for JIRA Ticket

## ⚠️ Important Correction

The information you received is **PARTIALLY CORRECT**, but the **CLI command is WRONG**.

---

## ✅ What's CORRECT:

1. ✅ **Session Pool UI doesn't show ingress** - This is TRUE
2. ✅ **Contributor cannot modify ingress** - This is TRUE  
3. ✅ **Admin must use CLI/REST API** - This is TRUE

---

## ❌ What's WRONG:

The CLI command provided is **incorrect**:

**WRONG** (from the message):
```bash
az containerapp update \  # ❌ This is for regular Container Apps, not Session Pools!
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --ingress external \
  --target-port 2000 \
  --transport auto
```

**CORRECT** (for Session Pools):
```bash
az containerapp sessionpool update \  # ✅ Correct command for Session Pools
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000
```

**Note**: Session pools use `--target-port` parameter, but there's **NO `--ingress external` parameter** in the CLI. The ingress is automatically enabled when `--target-port` is set.

---

## 📋 CORRECTED JIRA Ticket Message

Copy this to your JIRA ticket:

---

```
Ingress settings are not visible in the Azure Portal for Session Pools because the Session Pool resource type hides ingress configuration in the UI.

As a Contributor, I cannot modify ingress or networking settings for Session Pools.

Please run the following command to set target-port=2000 (this will enable ingress):

az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --target-port 2000

This will expose the session pool so that our backend can call the /python/execute endpoint. Without this, we get 404 errors.

Verification:
After running the command, please verify:
az containerapp sessionpool show \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --query "properties.template.ingress.targetPort" \
  -o tsv

Should return: 2000 (not null)
```

---

## 🔍 Why This Matters

- `az containerapp update` is for **regular Container Apps** (different resource type)
- `az containerapp sessionpool update` is for **Session Pools** (what we need)
- Session pools don't have `--ingress external` parameter
- Setting `--target-port` automatically enables ingress for session pools

---

## ✅ Summary

**Your understanding is correct** about:
- Portal not showing ingress ✅
- Contributor limitations ✅  
- Need for admin ✅

**But the command needs to be corrected** to:
- Use `az containerapp sessionpool update` (not `az containerapp update`)
- Use `--target-port 2000` (no `--ingress external` needed)

---

**Status**: Use the corrected message above for your JIRA ticket ✅


