# Deployment Plan - Refactored Code Executor (Testing)

## 🎯 Deployment Strategy

### Separate Environment for Testing
To avoid confusion with production services, we're using a **dedicated testing environment**:

**Testing Environment**: `ai-ta-RA-env-testing` (Already exists!)
- **Purpose**: Testing refactored code executor
- **Isolation**: Separate from production environments
- **No Conflicts**: Won't interfere with existing services

### Current Environment Usage

| Service | Environment | Purpose |
|---------|-------------|---------|
| `gaia-backend` | `cae-gaia-dev` | GAIA backend (dev) |
| `ai-ta-ra-code-executor2` | `ai-ta-RA-env` | Production executor |
| `ai-ta-ra-code-executor2.1-testing` | `ai-ta-RA-env-testing` | **Testing executor** ✅ |

## 📋 Deployment Details

### Container App
- **Name**: `ai-ta-ra-code-executor2.1-testing`
- **Environment**: `ai-ta-RA-env-testing` (Already exists!)
- **Resource Group**: `ai-ta-2`
- **Location**: `eastus2`

### Container Registry
- **ACR Name**: `ait2codingengineacr`
- **ACR URL**: `ait2codingengineacr.azurecr.io`
- **Image**: `executor-service-refactored:v4.0.0-refactored`

### Configuration
- **CPU**: 2.0 vCPU
- **Memory**: 4.0Gi
- **Min Replicas**: 1
- **Max Replicas**: 3
- **Port**: 8000
- **Ingress**: External (public HTTPS)

## 🚀 Deployment Steps

1. **Check Environment** (already exists: `ai-ta-RA-env-testing`)
   - Environment will be created automatically if it doesn't exist
   - Script handles this automatically

2. **Build & Push Image**
   ```bash
   docker build --platform linux/amd64 -f Dockerfile.fastapi \
     -t ait2codingengineacr.azurecr.io/executor-service-refactored:v4.0.0-refactored .
   docker push ait2codingengineacr.azurecr.io/executor-service-refactored:v4.0.0-refactored
   ```

3. **Create Container App**
   ```bash
   az containerapp create \
     --name ai-ta-ra-code-executor2.1-testing \
     --resource-group ai-ta-2 \
     --environment cae-executor-testing \
     --image ait2codingengineacr.azurecr.io/executor-service-refactored:v4.0.0-refactored \
     --target-port 8000 \
     --ingress external \
     --min-replicas 1 \
     --max-replicas 3 \
     --cpu 2.0 \
     --memory 4.0Gi
   ```

## ✅ Benefits of Separate Environment

1. **No Confusion**: Clear separation from production
2. **Easy Cleanup**: Can delete entire environment for testing
3. **Isolation**: Won't affect production services
4. **Testing**: Safe to experiment without risk
5. **Cost Control**: Can stop/delete when not needed

## 🧪 Testing Plan

After deployment:
1. Test `/health` endpoint
2. Test `/run` with sample test cases
3. Test `/runall` with multiple test cases
4. Test C++ batch optimization
5. Compare performance with production version
6. Monitor logs for errors

## 🔄 Migration Plan

Once testing is successful:
1. Update production `ai-ta-ra-code-executor2` with new image
2. OR create new production Container App
3. Switch traffic gradually
4. Monitor for 24-48 hours
5. Delete testing environment if not needed

