# Code Execution Service - FastAPI

Production-ready code execution service supporting Python, C++, Java, JavaScript, and C#.

## 🚀 Quick Start

See [QUICK_START.md](QUICK_START.md) for 3-step quick start guide.

## 📚 Documentation

- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Complete API documentation with examples
- **[QUICK_START.md](QUICK_START.md)** - Quick reference guide

## 🏗️ Architecture

- **Framework:** FastAPI
- **Server:** Gunicorn + Uvicorn workers
- **Deployment:** Azure Container Apps
- **Languages Supported:** Python, C++, Java, JavaScript, C#

## 📦 Deployment Files

### Essential Files
- `executor-service-fastapi.py` - Main FastAPI service
- `Dockerfile.fastapi` - Docker image definition
- `requirements-fastapi.txt` - Python dependencies
- `terraform/` - Infrastructure as Code (Azure resources)

### Configuration
- **Min Replicas:** 0 (scales to zero for cost savings)
- **Max Replicas:** 3 (auto-scales under load)
- **Concurrent Capacity:** 8 requests per replica (4 workers × 2 threads)

## 🔧 Deployment

### Using Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Using Azure CLI
```bash
# Build and push image
docker buildx build --platform linux/amd64 \
  -t <registry>/executor-fastapi:latest \
  -f Dockerfile.fastapi . --push

# Deploy to Container Apps
az containerapp update \
  --name <app-name> \
  --resource-group <resource-group> \
  --image <registry>/executor-fastapi:latest
```

## 📡 API Endpoint

```
https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io
```

### Endpoints
- `POST /runall` - Execute code with all test cases
- `POST /run` - Execute code with sample test cases
- `POST /submit` - Submit code and save to database
- `GET /health` - Health check

## 🔒 Security

- Code runs in isolated sandbox
- Network access blocked
- Resource limits enforced
- Timeout protection

## 📊 Performance

- **Average Execution Time:** 50-200ms (interpreted languages)
- **Compilation Time:** 1-4s (compiled languages)
- **Concurrent Capacity:** 8 requests per replica
- **Queue System:** Handles 200+ requests in backlog

## 🛠️ Development

### Local Testing
```bash
# Install dependencies
pip install -r requirements-fastapi.txt

# Run locally
uvicorn executor-service-fastapi:app --reload --port 8000
```

### Testing
```bash
# Health check
curl http://localhost:8000/health

# Test execution
curl -X POST http://localhost:8000/runall \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "code": "print(42)", "test_cases": [...]}'
```

## 📝 License

See repository license file.

---

**Branch:** `readyfastapi`  
**Status:** Production Ready  
**Last Updated:** December 5, 2025
