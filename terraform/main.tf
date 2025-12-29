# Terraform configuration for Code Executor Infrastructure
# This creates the infrastructure (Container App, ACR, etc.)

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  # Optional: Store state remotely (recommended for team)
  # backend "azurerm" {
  #   resource_group_name  = "terraform-state-rg"
  #   storage_account_name = "terraformstate"
  #   container_name       = "tfstate"
  #   key                  = "executor.terraform.tfstate"
  # }
}

provider "azurerm" {
  features {}
}

# Data sources (existing resources)
data "azurerm_resource_group" "main" {
  name = "ai-ta-2"
}

data "azurerm_container_registry" "acr" {
  name                = "ait2codingengineacr"
  resource_group_name = data.azurerm_resource_group.main.name
}

data "azurerm_container_app_environment" "env" {
  name                = "ai-ta-RA-env-testing"
  resource_group_name = data.azurerm_resource_group.main.name
}

# Container App for Code Executor
resource "azurerm_container_app" "executor" {
  name                         = "executor-refactored-test"
  container_app_environment_id = data.azurerm_container_app_environment.env.id
  resource_group_name          = data.azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    min_replicas = 1
    max_replicas = 3

    container {
      name   = "executor"
      image  = "${data.azurerm_container_registry.acr.login_server}/executor-service-refactored:latest"
      cpu    = 2.0
      memory = "4.0Gi"

      env {
        name  = "PORT"
        value = "8000"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "http"
    
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  registry {
    server   = data.azurerm_container_registry.acr.login_server
    identity = null  # Using admin credentials
  }

  secret {
    name  = "acr-password"
    value = data.azurerm_container_registry.acr.admin_password
  }

  tags = {
    environment = "testing"
    purpose     = "code-execution"
    managed-by  = "terraform"
  }
}

# Outputs
output "container_app_url" {
  description = "URL of the code executor"
  value       = "https://${azurerm_container_app.executor.latest_revision_fqdn}"
}

output "container_app_name" {
  description = "Name of the Container App"
  value       = azurerm_container_app.executor.name
}

output "container_app_id" {
  description = "ID of the Container App"
  value       = azurerm_container_app.executor.id
}
