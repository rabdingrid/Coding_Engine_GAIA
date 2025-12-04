# Manual C# Deployment Steps

## ⚠️ Docker Not Running

Docker daemon needs to be running to build the image.

## 🚀 Manual Deployment Steps

### Step 1: Start Docker Desktop

1. Open Docker Desktop application
2. Wait for it to fully start (whale icon in menu bar)
3. Verify: `docker ps` should work

### Step 2: Build and Push Image

Once Docker is running, execute:

```bash
cd Coding_Engine/aca-executor

# Build the image
docker build -t executor-secure:v17-csharp .

# Tag for ACR
docker tag executor-secure:v17-csharp aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp

# Login to Azure (if not already)
az login

# Login to ACR
az acr login --name aitaraacr1763805702

# Push to ACR
docker push aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp
```

### Step 3: Apply Terraform

```bash
cd terraform
terraform apply
```

Type `yes` when prompted.

### Step 4: Verify Deployment

Wait 2-3 minutes for containers to restart, then:

```bash
# Check health
curl https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Should show csharp in supported_languages
```

### Step 5: Test C# Execution

```bash
curl -X POST "https://ai-ta-ra-code-executor2--0000026.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "csharp",
    "code": "using System; class Program { static void Main() { Console.WriteLine(42); } }",
    "test_cases": [{"input": "", "expected_output": "42"}]
  }'
```

## 📋 Quick Command Sequence

```bash
# 1. Start Docker Desktop first, then:

cd Coding_Engine/aca-executor
docker build -t executor-secure:v17-csharp .
docker tag executor-secure:v17-csharp aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp
az acr login --name aitaraacr1763805702
docker push aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp
cd terraform
terraform apply
```

## ⏱️ Expected Time

- **Docker Build**: 3-5 minutes (first time, includes Mono installation)
- **Push**: 1-2 minutes
- **Terraform Apply**: 2-3 minutes
- **Container Restart**: 1-2 minutes
- **Total**: ~7-12 minutes

## ✅ What's Already Done

- ✅ Dockerfile updated with Mono
- ✅ C# code in executor-service-secure.py
- ✅ Terraform variables updated
- ✅ Deployment script created

Just need Docker running and execute the commands above!

