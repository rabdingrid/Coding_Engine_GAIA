# Terraform Configuration for ACA Code Executor
# Handles 100-500 users (200-1,000 executions) with minimal pre-warmed pool

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Variables are defined in variables.tf

# Get existing resource group
data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

# Get existing Container Apps Environment
data "azurerm_container_app_environment" "main" {
  name                = var.container_app_env_name
  resource_group_name = var.resource_group_name
}

# Get ACR
data "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = var.resource_group_name
}

# Container App for Code Execution
resource "azurerm_container_app" "code_executor" {
  name                         = "ai-ta-ra-code-executor2"
  container_app_environment_id = data.azurerm_container_app_environment.main.id
  resource_group_name          = data.azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    # Minimal pre-warmed pool (1 container) - cost optimized for 5 users
    # Auto-scales up to 10 during peak (5 users × 2 questions = 10 executions)
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    container {
      name   = "executor"
      image  = var.executor_image
      cpu    = 2.0      # 2 vCPU required for 4Gi memory (Azure requirement)
      memory = "4.0Gi"  # Increased to 4Gi to support Node.js CodeRange and Java heap

      env {
        name  = "PORT"
        value = "8000"
      }
    }
  }

  # Ingress configuration (allows external access)
  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "http"
    
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  # Registry configuration (use username/password)
  registry {
    server   = data.azurerm_container_registry.acr.login_server
    username = data.azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }
  
  # Store ACR password as secret (must be defined before registry block)
  secret {
    name  = "acr-password"
    value = data.azurerm_container_registry.acr.admin_password
  }

  tags = {
    environment = "production"
    purpose     = "code-execution"
    capacity    = "200-students-contest"
  }
}

# Output: Container App URL
output "container_app_url" {
  description = "URL of the code executor"
  value       = "https://${azurerm_container_app.code_executor.latest_revision_fqdn}"
}

# Output: Container App ID
output "container_app_id" {
  description = "ID of the code executor"
  value       = azurerm_container_app.code_executor.id
}

# Output: Container App Name
output "container_app_name" {
  description = "Name of the code executor"
  value       = azurerm_container_app.code_executor.name
}

