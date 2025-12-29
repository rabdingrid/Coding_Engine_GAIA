# Deployment Guide: CI/CD vs Terraform

## 🎯 Quick Reference

| Task | Use CI/CD | Use Terraform |
|------|-----------|---------------|
| Deploy code updates | ✅ Yes | ❌ No |
| Create infrastructure | ❌ No | ✅ Yes |
| Update application | ✅ Yes | ❌ No |
| Change scaling | ❌ No | ✅ Yes |
| Daily deployments | ✅ Yes | ❌ No |

---

## 🚀 CI/CD Pipeline Setup

### Step 1: Create Azure Service Principal

```bash
# Login to Azure
az login

# Create service principal
az ad sp create-for-rbac --name "github-actions-executor" \
  --role contributor \
  --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/ai-ta-2 \
  --sdk-auth
```

**Copy the JSON output** - you'll need it for GitHub secrets.

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

**Secret 1: `AZURE_CREDENTIALS`**
```
Paste the entire JSON from step 1
```

**Secret 2: `AZURE_CLIENT_ID`**
```
Extract "clientId" from the JSON
```

**Secret 3: `AZURE_CLIENT_SECRET`**
```
Extract "clientSecret" from the JSON
```

**Secret 4: `AZURE_TENANT_ID`**
```
Extract "tenantId" from the JSON
```

### Step 3: Push Code

```bash
git add .github/workflows/deploy.yml
git commit -m "Add CI/CD pipeline"
git push origin readyfastapi
```

The workflow will automatically:
1. ✅ Run security scans
2. ✅ Build Docker image
3. ✅ Deploy to Azure

### Step 4: Monitor Deployment

1. Go to **Actions** tab in GitHub
2. Click on the running workflow
3. Watch the deployment progress

---

## 🏗️ Terraform Setup

### Step 1: Install Terraform

**macOS:**
```bash
brew install terraform
```

**Linux:**
```bash
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

**Windows:**
Download from: https://www.terraform.io/downloads

### Step 2: Login to Azure

```bash
az login
az account set --subscription YOUR_SUBSCRIPTION_ID
```

### Step 3: Initialize Terraform

```bash
cd terraform
terraform init
```

### Step 4: Review Changes

```bash
terraform plan
```

This shows what will be created/modified.

### Step 5: Apply Changes

```bash
terraform apply
```

Type `yes` when prompted.

### Step 6: Verify

```bash
terraform output
```

Shows the Container App URL.

---

## 📋 Typical Workflow

### Initial Setup (One-time)

```bash
# 1. Create infrastructure with Terraform
cd terraform
terraform init
terraform plan
terraform apply

# 2. Set up CI/CD (one-time)
# Add GitHub secrets (see CI/CD setup above)
# Push workflow file
```

### Daily Development

```bash
# 1. Make code changes
vim executor-service/main.py

# 2. Commit and push
git add .
git commit -m "Fix bug"
git push origin readyfastapi

# 3. CI/CD automatically deploys!
# Check GitHub Actions for status
```

### Infrastructure Changes

```bash
# 1. Modify Terraform config
vim terraform/main.tf

# 2. Review changes
cd terraform
terraform plan

# 3. Apply changes
terraform apply
```

---

## 🔄 When to Use What

### Use CI/CD When:
- ✅ You changed code in `executor-service/`
- ✅ You updated `Dockerfile.fastapi`
- ✅ You want to deploy a new version
- ✅ You pushed code to GitHub

**Example:**
```bash
# Changed code
vim executor-service/main.py
git push origin main
# → CI/CD automatically deploys
```

### Use Terraform When:
- ✅ You want to change scaling (min/max replicas)
- ✅ You need to change CPU/memory allocation
- ✅ You want to create a new environment
- ✅ You need to modify infrastructure

**Example:**
```bash
# Change scaling
vim terraform/main.tf  # Change max_replicas: 3 → 5
terraform apply
# → Infrastructure updated
```

---

## 🎯 Best Practices

### CI/CD Best Practices

1. ✅ **Protect main branch** - Require PR reviews
2. ✅ **Run tests before deploy** - Security scans included
3. ✅ **Use tags for versions** - Tag releases
4. ✅ **Monitor deployments** - Check health checks

### Terraform Best Practices

1. ✅ **Version control** - Commit `.tf` files
2. ✅ **Don't commit state** - Add `*.tfstate` to `.gitignore`
3. ✅ **Use remote state** - For team collaboration
4. ✅ **Review before apply** - Always run `terraform plan`

---

## 🆘 Troubleshooting

### CI/CD Issues

**Problem**: Workflow fails at "Login to Azure"
- **Solution**: Check `AZURE_CREDENTIALS` secret is correct

**Problem**: Image push fails
- **Solution**: Verify ACR name matches `AZURE_CONTAINER_REGISTRY`

**Problem**: Deployment fails
- **Solution**: Check Container App name matches workflow config

### Terraform Issues

**Problem**: `terraform init` fails
- **Solution**: Check Azure credentials: `az account show`

**Problem**: `terraform apply` fails
- **Solution**: Verify resource names exist (ACR, Resource Group)

**Problem**: State file conflicts
- **Solution**: Use remote state backend (Azure Storage)

---

## 📚 Additional Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Container Apps Docs](https://learn.microsoft.com/en-us/azure/container-apps/)

---

## ✅ Checklist

### CI/CD Setup
- [ ] Azure service principal created
- [ ] GitHub secrets added
- [ ] Workflow file pushed
- [ ] First deployment successful

### Terraform Setup
- [ ] Terraform installed
- [ ] Azure CLI configured
- [ ] `terraform init` successful
- [ ] `terraform plan` reviewed
- [ ] `terraform apply` successful

---

**Ready to deploy!** 🚀

