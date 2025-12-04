# 📦 Deployment Files - FastAPI Version

## Essential Files for Deployment

### Core Service Files
```
Coding_Engine/aca-executor/
├── executor-service-fastapi.py    # Main FastAPI service (REQUIRED)
├── Dockerfile.fastapi              # Docker configuration (REQUIRED)
└── requirements-fastapi.txt       # Python dependencies (REQUIRED)
```

### Infrastructure (Terraform)
```
Coding_Engine/aca-executor/terraform/
├── main.tf                        # Main Terraform config (REQUIRED)
├── variables.tf                   # Variables (REQUIRED)
├── container-app.tf               # Container App config (REQUIRED)
├── container-registry.tf          # ACR config (REQUIRED)
└── postgresql.tf                  # PostgreSQL config (OPTIONAL - if using Azure DB)
```

## File Descriptions

### 1. `executor-service-fastapi.py`
- **Purpose**: Main FastAPI application
- **Size**: ~1,500 lines
- **Contains**: 
  - All 3 endpoints (/run, /runall, /submit)
  - Code execution logic for all 5 languages
  - Security guardrails
  - Database integration

### 2. `Dockerfile.fastapi`
- **Purpose**: Docker image build configuration
- **Base Image**: `python:3.11-slim`
- **Installs**: Node.js, Java, C++ compilers, Mono (C#)
- **Runs**: Uvicorn with 4 workers

### 3. `requirements-fastapi.txt`
- **Purpose**: Python package dependencies
- **Packages**:
  - `fastapi==0.104.1`
  - `uvicorn[standard]==0.24.0`
  - `pydantic==2.5.0`
  - `slowapi==0.1.9`
  - `asyncpg==0.29.0`
  - `psutil==5.9.8`

### 4. Terraform Files
- **main.tf**: Resource group, providers
- **variables.tf**: Input variables
- **container-app.tf**: Azure Container App configuration
- **container-registry.tf**: Azure Container Registry
- **postgresql.tf**: PostgreSQL Flexible Server (if needed)

## Deployment Steps

### 1. Build Docker Image
```bash
cd Coding_Engine/aca-executor
docker build -f Dockerfile.fastapi -t your-registry/executor-fastapi:v3.0.0 .
```

### 2. Push to Container Registry
```bash
docker push your-registry/executor-fastapi:v3.0.0
```

### 3. Deploy with Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Files NOT Required for Deployment

❌ Test files (`test-ui/`)
❌ Documentation (`.md` files)
❌ Old Flask version (`executor-service-secure.py`)
❌ Old Dockerfile (`Dockerfile` - Flask version)
❌ Old requirements (`requirements.txt` - Flask version)
❌ Frontend files
❌ Node.js files (except what's in Dockerfile)

## Minimal Deployment Set

**Absolute minimum files needed:**
1. `executor-service-fastapi.py`
2. `Dockerfile.fastapi`
3. `requirements-fastapi.txt`

**For infrastructure deployment:**
+ All Terraform files in `terraform/` directory

## File Sizes (Approximate)

- `executor-service-fastapi.py`: ~55 KB
- `Dockerfile.fastapi`: ~1 KB
- `requirements-fastapi.txt`: ~200 bytes
- Terraform files: ~5-10 KB total

## Quick Check

To verify you have all required files:
```bash
cd Coding_Engine/aca-executor
ls -lh executor-service-fastapi.py Dockerfile.fastapi requirements-fastapi.txt
ls -lh terraform/*.tf
```

