# Terraform Configuration: Pre-Warmed ACA Container Pool
# This creates a pool of containers that are always running, ready to execute code

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

# Variables
variable "resource_group_name" {
  description = "Resource group name"
  default     = "ai-ta-2"
}

variable "location" {
  description = "Azure region"
  default     = "eastus2"
}

variable "container_app_env_name" {
  description = "Container Apps Environment name"
  default     = "ai-ta-RA-env"
}

variable "acr_name" {
  description = "Azure Container Registry name"
  default     = "aitaraacr1763805702"
}

variable "executor_image" {
  description = "Container image for code execution"
  default     = "aitaraacr1763805702.azurecr.io/executor-image:v1"
}

variable "min_replicas" {
  description = "Minimum number of pre-warmed containers"
  default     = 5
}

variable "max_replicas" {
  description = "Maximum number of containers (for scaling)"
  default     = 50
}

# Get existing resource group
data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

# Get existing Container Apps Environment
data "azurerm_container_app_environment" "main" {
  name                = var.container_app_env_name
  resource_group_name = var.resource_group_name
}

# Get ACR credentials
data "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = var.resource_group_name
}

# Container App for Code Execution Pool
resource "azurerm_container_app" "code_executor_pool" {
  name                         = "code-executor-pool"
  container_app_environment_id = data.azurerm_container_app_environment.main.id
  resource_group_name          = data.azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    # Pre-warmed pool: Keep min_replicas containers always running
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    container {
      name   = "executor"
      image  = var.executor_image
      cpu    = 0.5
      memory = "1.0Gi"

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

  # Registry configuration
  registry {
    server   = data.azurerm_container_registry.acr.login_server
    identity = data.azurerm_container_registry.acr.id
  }

  # Scale configuration
  scale {
    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
  }

  tags = {
    environment = "production"
    purpose      = "code-execution"
  }
}

# Output: Container App URL
output "container_app_url" {
  description = "URL of the code executor pool"
  value       = "https://${azurerm_container_app.code_executor_pool.latest_revision_fqdn}"
}

# Output: Container App ID
output "container_app_id" {
  description = "ID of the code executor pool"
  value       = azurerm_container_app.code_executor_pool.id
}


