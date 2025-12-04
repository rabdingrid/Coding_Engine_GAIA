# Quick Start: Deploy C# Support

## 🚀 One Command Deployment

**After starting Docker Desktop**, run:

```bash
cd Coding_Engine/aca-executor
./deploy-and-test.sh
```

This script will:
1. ✅ Check Docker is running
2. ✅ Build Docker image with C# support
3. ✅ Push to Azure Container Registry
4. ✅ Apply Terraform changes
5. ✅ Wait for deployment
6. ✅ Test C# execution
7. ✅ Test with Two Sum question

**Total time**: ~10-15 minutes

## 📋 What It Does

### Deployment Steps:
1. Builds `executor-secure:v17-csharp` image
2. Tags and pushes to ACR
3. Updates Container App via Terraform
4. Waits for containers to restart

### Testing Steps:
1. Checks health endpoint for C# support
2. Tests simple C# "Hello World"
3. Tests C# with Two Sum question (Q001)

## ⚠️ Prerequisites

1. **Docker Desktop** must be running
2. **Azure CLI** logged in (`az login`)
3. **Terraform** installed

## 🎯 After Deployment

All 50 DSA questions will support C#! Users can:
- Select C# language in UI
- Use C# boilerplates
- Execute C# code
- Get TLE/MLE errors

## 🔍 Manual Testing (After Deployment)

```bash
# Test health
curl https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Test C# execution
curl -X POST "https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "csharp",
    "code": "using System; class Program { static void Main() { Console.WriteLine(42); } }",
    "test_cases": [{"input": "", "expected_output": "42"}]
  }'
```

