# ACA Code Executor - Simple Deployable Solution

## 🎯 Purpose

Simple, deployable solution for Azure Container Apps that executes user code for **100-500 users** (200-1,000 executions) with **minimal pre-warmed pool** (cost-optimized).

---

## 📁 Project Structure

```
aca-executor/
├── Dockerfile                 # Container image definition
├── executor-service.py        # Code execution service
├── requirements.txt           # Python dependencies
├── terraform/                 # Infrastructure as Code
│   ├── main.tf               # Main Terraform config
│   └── variables.tf          # Variables
├── backend-integration.py     # Backend integration code
├── DEPLOYMENT_GUIDE.md        # Step-by-step deployment
└── README.md                  # This file
```

---

## ✨ Features

- ✅ **Multi-language Support**: Python, JavaScript, Java, C++
- ✅ **Cost-Optimized**: Minimal pre-warmed pool (5 containers)
- ✅ **Auto-Scaling**: Scales up to 1,000 containers during peak
- ✅ **Security**: Resource limits, non-root user, timeout protection
- ✅ **Simple**: Easy to deploy and manage
- ✅ **Fast**: Pre-warmed containers for instant execution

---

## 🚀 Quick Start

### 1. Build and Push Image

```bash
cd aca-executor
az acr login --name aitaraacr1763805702
docker build -t aitaraacr1763805702.azurecr.io/executor-image:v1 .
docker push aitaraacr1763805702.azurecr.io/executor-image:v1
```

### 2. Deploy with Terraform

```bash
cd terraform
terraform init
terraform apply
```

### 3. Test

```bash
curl https://code-executor.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

---

## 📊 Configuration

### Default (Cost-Optimized)

- **Min Replicas**: 5 (pre-warmed)
- **Max Replicas**: 1,000 (peak capacity)
- **Cost**: ~$2-5/day idle, ~$50-100 per contest

### Adjust for Your Needs

Edit `terraform/variables.tf` or pass via command line:

```bash
terraform apply -var="min_replicas=2" -var="max_replicas=200"
```

---

## 💰 Cost

- **Idle (5 containers)**: ~$2-5/day
- **Contest (500 users)**: ~$50-100 for 2 hours
- **Idle (0 containers)**: $0/day (cold start: 5-10 seconds)

---

## 🔧 Supported Languages

- ✅ Python 3.11
- ✅ JavaScript (Node.js)
- ✅ Java 17
- ✅ C++ (GCC)

---

## 📖 Documentation

- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
- **Backend Integration**: See `backend-integration.py`
- **Terraform Config**: See `terraform/main.tf`

---

## ✅ Status

Ready to deploy! Follow `DEPLOYMENT_GUIDE.md` for step-by-step instructions.


