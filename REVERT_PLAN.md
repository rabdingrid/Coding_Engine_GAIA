# 🔄 REVERT PLAN - C++ Batch Optimization

## ⚠️ Emergency Revert Instructions

If the new C++ batch optimization causes issues, follow these steps to revert to the working state.

---

## 📋 Pre-Deployment Checklist

**Backup Status:**
- ✅ Backup file created: `executor-service-fastapi.py.backup`
- ✅ Original working version saved
- ✅ Date: December 10, 2024

---

## 🚨 Quick Revert (5 minutes)

### Step 1: Stop the Service (if running locally)

```bash
# If running with uvicorn
pkill -f uvicorn

# Or if running in Docker
docker stop <container_name>
```

### Step 2: Restore Backup File

```bash
cd /Users/rabdin/Documents/AGCodingEngine

# Restore from backup
cp executor-service-fastapi.py.backup executor-service-fastapi.py

# Verify backup exists
ls -lh executor-service-fastapi.py.backup
```

### Step 3: Restart Service

```bash
# Local development
uvicorn executor-service-fastapi:app --host 0.0.0.0 --port 8000

# Or Docker
docker-compose up -d

# Or Azure Container Apps (see deployment section)
```

### Step 4: Verify Service is Working

```bash
# Health check
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Test with simple request
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(1+1)",
    "sample_test_cases": [{"id": "test1", "input": "", "expected_output": "2"}]
  }'
```

---

## 🔍 What Changed (For Reference)

### Files Modified
1. **`executor-service-fastapi.py`**
   - Added: `execute_cpp_batch()` function (lines ~845-1000)
   - Modified: `/runall` endpoint (lines ~1251-1308)

### Changes Summary
- **Added:** Batch execution function for C++ (compile once, run multiple times)
- **Modified:** `/runall` endpoint to use batch execution for C++ with multiple test cases
- **Impact:** Only affects C++ code with 2+ test cases in `/runall` endpoint

### What Stays the Same
- ✅ `/run` endpoint unchanged
- ✅ Python/JavaScript/Java/C# unchanged
- ✅ Single test case execution unchanged
- ✅ API contract unchanged (backward compatible)

---

## 🐛 Troubleshooting

### Issue: Service won't start

**Symptoms:**
- Import errors
- Syntax errors
- Module not found

**Solution:**
```bash
# Check Python syntax
python3 -m py_compile executor-service-fastapi.py

# Check imports
python3 -c "import executor-service-fastapi"

# Restore backup if errors found
cp executor-service-fastapi.py.backup executor-service-fastapi.py
```

### Issue: C++ execution fails

**Symptoms:**
- All C++ test cases fail
- Compilation errors
- Runtime errors

**Solution:**
1. Check logs for specific error
2. If batch execution is the issue, revert immediately
3. Test with single test case (should still work)

### Issue: Performance worse than before

**Symptoms:**
- Execution time increased
- Timeouts

**Solution:**
- Revert to backup
- Check if batch execution is causing issues
- May need to adjust timeout settings

---

## 📊 Rollback Verification

After reverting, verify these scenarios work:

### ✅ Test 1: Python (should work)
```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(1+1)",
    "sample_test_cases": [{"id": "test1", "input": "", "expected_output": "2"}]
  }'
```

### ✅ Test 2: C++ Single Test (should work)
```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main(){int a,b;std::cin>>a>>b;std::cout<<a+b;}",
    "sample_test_cases": [{"id": "test1", "input": "5\n3", "expected_output": "8"}]
  }'
```

### ✅ Test 3: C++ Multiple Tests (should work, but slower)
```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main(){int a,b;std::cin>>a>>b;std::cout<<a+b;}",
    "test_cases": [
      {"id": "test1", "input": "5\n3", "expected_output": "8"},
      {"id": "test2", "input": "10\n20", "expected_output": "30"}
    ]
  }'
```

**Expected:** Should work but take ~2.8s (1.4s × 2) instead of ~1.6s with optimization

---

## 🔄 Azure Container Apps Revert

If deployed to Azure, revert using:

### Option 1: Redeploy Previous Version

```bash
# If using GitHub Actions/CI/CD
# Revert the commit and push
git revert <commit-hash>
git push

# Or manually redeploy
az containerapp update \
  --name code-executor \
  --resource-group <resource-group> \
  --image <previous-image-tag>
```

### Option 2: Update Container Image

```bash
# Build and push previous version
docker build -t <registry>/code-executor:previous .
docker push <registry>/code-executor:previous

# Update container app to use previous image
az containerapp update \
  --name code-executor \
  --resource-group <resource-group> \
  --image <registry>/code-executor:previous
```

### Option 3: Direct File Update (if using file-based deployment)

```bash
# SSH into container or use Azure CLI
az containerapp exec \
  --name code-executor \
  --resource-group <resource-group> \
  --command "cp /app/executor-service-fastapi.py.backup /app/executor-service-fastapi.py"

# Restart container
az containerapp revision restart \
  --name code-executor \
  --resource-group <resource-group>
```

---

## 📝 Post-Revert Checklist

After reverting, verify:

- [ ] Service starts without errors
- [ ] Health endpoint responds: `/health`
- [ ] Python code execution works: `/run`
- [ ] C++ single test works: `/run`
- [ ] C++ multiple tests work: `/runall` (may be slower)
- [ ] No error logs in service
- [ ] All endpoints respond correctly

---

## 🆘 Emergency Contacts

If issues persist after revert:

1. **Check logs:**
   ```bash
   # Local
   tail -f logs/app.log
   
   # Azure
   az containerapp logs show --name code-executor --resource-group <rg>
   ```

2. **Verify backup file:**
   ```bash
   md5sum executor-service-fastapi.py.backup
   md5sum executor-service-fastapi.py
   # Should match if revert successful
   ```

3. **Git revert (if using version control):**
   ```bash
   git log --oneline
   git revert <commit-hash>
   ```

---

## 📦 Backup File Information

**File:** `executor-service-fastapi.py.backup`  
**Created:** December 10, 2024  
**Size:** Check with `ls -lh executor-service-fastapi.py.backup`  
**MD5:** Run `md5sum executor-service-fastapi.py.backup` to verify integrity

---

## ✅ Revert Confirmation

After successful revert, you should see:

- ✅ Service running normally
- ✅ All endpoints working
- ✅ C++ execution working (but slower for multiple tests)
- ✅ No new errors in logs
- ✅ Performance back to baseline (~1.4s per C++ test case)

---

## 🔄 Re-apply Optimization (If Needed)

If you want to try the optimization again after fixing issues:

1. Review error logs
2. Fix the issue in `executor-service-fastapi.py`
3. Test locally first
4. Create new backup: `cp executor-service-fastapi.py executor-service-fastapi.py.backup.v2`
5. Deploy again

---

**Last Updated:** December 10, 2024  
**Status:** Ready for deployment with revert plan in place ✅


