# Deploy C# Support - Step by Step

## ✅ What's Done

1. ✅ **Dockerfile Updated** - Added `mono-devel` and `mono-mcs` for C# compilation
2. ✅ **Code Ready** - `execute_csharp()` function already in `executor-service-secure.py`
3. ✅ **Terraform Updated** - Image version set to `v17-csharp`

## 🚀 Deployment Steps

### Step 1: Build and Push Docker Image

```bash
cd Coding_Engine/aca-executor

# Option A: Use the deployment script
./deploy-csharp.sh

# Option B: Manual steps
docker build -t executor-secure:v17-csharp .
docker tag executor-secure:v17-csharp aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp
az acr login --name aitaraacr1763805702
docker push aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp
```

### Step 2: Apply Terraform

```bash
cd terraform
terraform apply
```

This will:
- Update the Container App to use the new image
- Restart containers with C# support
- Take ~2-3 minutes

### Step 3: Verify C# Support

```bash
# Check health endpoint
curl https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Should show:
# "supported_languages": ["python", "javascript", "java", "cpp", "csharp"]
```

### Step 4: Test C# Execution

```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "csharp",
    "code": "using System; class Program { static void Main() { Console.WriteLine(42); } }",
    "test_cases": [{"input": "", "expected_output": "42"}]
  }'
```

## 📋 Quick Deploy Command

```bash
cd Coding_Engine/aca-executor
./deploy-csharp.sh && cd terraform && terraform apply
```

## ⏱️ Expected Time

- **Build**: 2-3 minutes
- **Push**: 1-2 minutes
- **Terraform Apply**: 2-3 minutes
- **Total**: ~5-8 minutes

## ✅ After Deployment

C# will work for all 50 DSA questions! Users can:
- Select C# as language in the UI
- Use C# boilerplates from questions
- Execute C# code against test cases
- Get TLE/MLE errors if needed

## 🔍 Troubleshooting

If C# doesn't work after deployment:

1. **Check image version**:
   ```bash
   az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query "properties.template.containers[0].image"
   ```

2. **Check logs**:
   ```bash
   az containerapp logs show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --tail 50
   ```

3. **Verify Mono installed**:
   ```bash
   # In container logs, should see mono/mcs available
   ```

