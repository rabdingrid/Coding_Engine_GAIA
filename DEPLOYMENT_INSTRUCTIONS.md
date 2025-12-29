# 🚀 Deployment Instructions - C++ Batch Optimization

## 📋 Pre-Deployment Checklist

- [x] Backup created: `executor-service-fastapi.py.backup`
- [x] Code changes implemented
- [x] Revert plan documented: `REVERT_PLAN.md`
- [ ] Local testing completed
- [ ] Code review completed

---

## 🧪 Step 1: Local Testing

### Test 1: Verify Syntax

```bash
cd /Users/rabdin/Documents/AGCodingEngine

# Check Python syntax
python3 -m py_compile executor-service-fastapi.py

# Should output nothing if successful
```

### Test 2: Test Batch Function

```bash
# Run the test script
python3 cpp-batch-optimization.py

# Expected output: Should complete in ~1-2 seconds for 5 test cases
```

### Test 3: Test with Real API (Local)

```bash
# Start service locally
uvicorn executor-service-fastapi:app --host 0.0.0.0 --port 8000

# In another terminal, test C++ batch execution
curl -X POST "http://localhost:8000/runall" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main(){int a,b;std::cin>>a>>b;std::cout<<a+b;}",
    "test_cases": [
      {"id": "test1", "input": "5\n3", "expected_output": "8"},
      {"id": "test2", "input": "10\n20", "expected_output": "30"},
      {"id": "test3", "input": "1\n1", "expected_output": "2"}
    ],
    "sample_test_cases": []
  }' \
  -w "\n⏱️ Time: %{time_total}s\n"
```

**Expected:** Should complete in ~2-3 seconds (much faster than before)

---

## 📦 Step 2: Build Docker Image (if using Docker)

```bash
# Build image
docker build -t code-executor:optimized .

# Tag for registry
docker tag code-executor:optimized <registry>/code-executor:optimized-v1

# Push to registry
docker push <registry>/code-executor:optimized-v1
```

---

## ☁️ Step 3: Deploy to Azure Container Apps

### Option A: Using Azure CLI

```bash
# Update container app with new image
az containerapp update \
  --name code-executor \
  --resource-group <your-resource-group> \
  --image <registry>/code-executor:optimized-v1

# Or update from source (if using GitHub Actions)
az containerapp update \
  --name code-executor \
  --resource-group <your-resource-group> \
  --source <path-to-source>
```

### Option B: Using GitHub Actions (if configured)

```bash
# Commit changes
git add executor-service-fastapi.py
git commit -m "feat: Optimize C++ batch execution - compile once, run multiple times"
git push origin main

# GitHub Actions will automatically build and deploy
```

### Option C: Manual File Upload (if using file-based deployment)

```bash
# Upload file to Azure
az storage blob upload \
  --account-name <storage-account> \
  --container-name <container> \
  --name executor-service-fastapi.py \
  --file executor-service-fastapi.py \
  --overwrite

# Restart container app
az containerapp revision restart \
  --name code-executor \
  --resource-group <your-resource-group>
```

---

## ✅ Step 4: Post-Deployment Verification

### Test 1: Health Check

```bash
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Expected: {"status": "healthy", ...}
```

### Test 2: Python (Should work as before)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(1+1)",
    "sample_test_cases": [{"id": "test1", "input": "", "expected_output": "2"}]
  }'
```

### Test 3: C++ Single Test (Should work as before)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main(){int a,b;std::cin>>a>>b;std::cout<<a+b;}",
    "sample_test_cases": [{"id": "test1", "input": "5\n3", "expected_output": "8"}]
  }'
```

### Test 4: C++ Multiple Tests (NEW - Should be faster!)

```bash
# Test with 17 test cases (your original test)
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall" \
  -H "Content-Type: application/json" \
  -d @your_cpp_test_with_17_cases.json \
  -w "\n⏱️ Total Time: %{time_total}s\n"
```

**Expected Performance:**
- **Before:** ~24 seconds
- **After:** ~5 seconds
- **Improvement:** 80% faster ✅

---

## 📊 Step 5: Monitor Performance

### Check Logs

```bash
# Azure Container Apps logs
az containerapp logs show \
  --name code-executor \
  --resource-group <your-resource-group> \
  --follow

# Look for:
# - "⚡ Using optimized batch execution for C++"
# - Execution times
# - Any errors
```

### Monitor Metrics

```bash
# Check response times
az monitor metrics list \
  --resource <container-app-resource-id> \
  --metric "ResponseTime"

# Check for errors
az monitor metrics list \
  --resource <container-app-resource-id> \
  --metric "Http5xx"
```

---

## 🐛 Step 6: Rollback (If Needed)

If issues occur, follow `REVERT_PLAN.md`:

```bash
# Quick revert
cp executor-service-fastapi.py.backup executor-service-fastapi.py

# Redeploy
# (Follow Azure deployment steps above)
```

---

## 📝 Deployment Checklist

- [ ] Local testing passed
- [ ] Docker image built (if applicable)
- [ ] Deployed to Azure Container Apps
- [ ] Health check passed
- [ ] Python execution works
- [ ] C++ single test works
- [ ] C++ multiple tests work (and faster!)
- [ ] Logs checked - no errors
- [ ] Performance verified (~5s for 17 tests)
- [ ] Revert plan ready if needed

---

## 🎯 Success Criteria

Deployment is successful if:

1. ✅ All existing functionality works (no regressions)
2. ✅ C++ batch execution is faster (~5s vs 24s for 17 tests)
3. ✅ No new errors in logs
4. ✅ Health endpoint responds correctly
5. ✅ All test cases execute correctly

---

## 📞 Support

If deployment fails:

1. Check `REVERT_PLAN.md` for rollback steps
2. Review logs for specific errors
3. Verify backup file exists: `executor-service-fastapi.py.backup`
4. Test locally before redeploying

---

**Deployment Date:** December 10, 2024  
**Version:** Optimized C++ Batch Execution v1.0  
**Status:** Ready for deployment ✅


