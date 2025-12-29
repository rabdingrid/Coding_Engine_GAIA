# ⚡ Quick Reference - C++ Optimization Deployment

## 🚀 Deploy

```bash
# 1. Test locally (recommended)
uvicorn executor-service-fastapi:app --host 0.0.0.0 --port 8000

# 2. Deploy to Azure (see DEPLOYMENT_INSTRUCTIONS.md)
az containerapp update --name code-executor --resource-group <rg> --image <image>
```

## 🔄 Revert (Emergency)

```bash
# Quick revert
cp executor-service-fastapi.py.backup executor-service-fastapi.py

# Redeploy
# (Follow deployment steps)
```

## ✅ Verify

```bash
# Health check
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Test C++ batch (should be ~5s for 17 tests)
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall" \
  -H "Content-Type: application/json" \
  -d @your_test.json \
  -w "\n⏱️ Time: %{time_total}s\n"
```

## 📁 Files

- **Modified:** `executor-service-fastapi.py` (69KB)
- **Backup:** `executor-service-fastapi.py.backup` (59KB) ✅
- **Revert Plan:** `REVERT_PLAN.md`
- **Deploy Guide:** `DEPLOYMENT_INSTRUCTIONS.md`

## 🎯 Expected Results

- **Before:** 24s for 17 C++ tests
- **After:** ~5s for 17 C++ tests
- **Improvement:** 80% faster ✅

## 🆘 Emergency

**If something breaks:**
1. Check `REVERT_PLAN.md`
2. Restore backup: `cp executor-service-fastapi.py.backup executor-service-fastapi.py`
3. Redeploy

**Backup MD5:** `6d9576b14679c8bbf855b6f862fd24ca`


