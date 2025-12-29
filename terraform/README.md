# Terraform Infrastructure Configuration

This directory contains Terraform configuration for managing the Code Executor infrastructure on Azure.

## 📋 Prerequisites

1. **Azure CLI** installed and configured
2. **Terraform** installed (>= 1.0)
3. **Azure credentials** configured

## 🚀 Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Review Changes

```bash
terraform plan
```

### 3. Apply Changes

```bash
terraform apply
```

### 4. Destroy Infrastructure (if needed)

```bash
terraform destroy
```

## 📁 Files

- `main.tf` - Main infrastructure configuration
- `variables.tf` - Variable definitions
- `outputs.tf` - Output values
- `terraform.tfvars` - Variable values (create this file, don't commit secrets)

## 🔧 Configuration

### Create `terraform.tfvars` (optional)

```hcl
resource_group_name      = "ai-ta-2"
container_app_name       = "executor-refactored-test"
container_app_env_name   = "ai-ta-RA-env-testing"
acr_name                 = "ait2codingengineacr"
min_replicas            = 1
max_replicas            = 3
cpu                     = 2.0
memory                  = "4.0Gi"
environment             = "testing"
```

## 📊 What Gets Created

- **Container App**: `executor-refactored-test`
- **Uses existing**: Resource Group, ACR, Container App Environment

## ⚠️ Important Notes

1. **State File**: Terraform creates a `terraform.tfstate` file. Don't commit this!
2. **Secrets**: Don't commit `terraform.tfvars` if it contains secrets
3. **Backend**: Consider using remote state (Azure Storage) for team collaboration

## 🔄 Workflow

1. **First Time**: `terraform apply` creates infrastructure
2. **Updates**: Modify `.tf` files, run `terraform plan`, then `terraform apply`
3. **Destroy**: `terraform destroy` removes all resources

## 📚 Resources

- [Terraform Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Container Apps Docs](https://learn.microsoft.com/en-us/azure/container-apps/)

