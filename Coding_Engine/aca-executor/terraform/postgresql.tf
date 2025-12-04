# Azure PostgreSQL Flexible Server
# Cost-optimized configuration for development/testing

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Get existing resource group
data "azurerm_resource_group" "main" {
  name = "ai-ta-2"
}

# PostgreSQL Flexible Server (cheaper option)
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "ai-ta-ra-postgre"
  resource_group_name    = data.azurerm_resource_group.main.name
  location               = data.azurerm_resource_group.main.location
  version                = "14"  # PostgreSQL 14
  delegated_subnet_id    = null  # Public access for simplicity
  private_dns_zone_id    = null
  administrator_login    = "postgresadmin"
  administrator_password  = var.postgres_password  # Set via variable or generate
  zone                   = "1"
  
  # Cost-optimized SKU (Burstable, minimal resources)
  sku_name = "B_Standard_B1ms"  # Burstable, 1 vCore, 2GB RAM - ~$12/month
  
  storage_mb = 32768  # 32GB storage (minimum)
  
  # Backup settings
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false  # Disable for cost savings
  
  # High availability (disabled for cost savings)
  high_availability {
    mode = "Disabled"
  }
  
  # Maintenance window
  maintenance_window {
    day_of_week  = 0
    start_hour   = 2
    start_minute = 0
  }
  
  # Firewall rules - allow Azure services
  public_network_access_enabled = true
  
  tags = {
    environment = "production"
    purpose     = "coding-engine-database"
    managed-by  = "terraform"
  }
  
  depends_on = [data.azurerm_resource_group.main]
}

# Firewall rule to allow Azure services
resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"  # Allows all Azure services
}

# Firewall rule to allow your current IP (optional - for migration)
# Uncomment and set your IP if needed
# resource "azurerm_postgresql_flexible_server_firewall_rule" "my_ip" {
#   name             = "AllowMyIP"
#   server_id        = azurerm_postgresql_flexible_server.main.id
#   start_ip_address = "YOUR_IP_ADDRESS"
#   end_ip_address   = "YOUR_IP_ADDRESS"
# }

# Database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "railway"  # Same name as Railway database
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Outputs
output "postgresql_server_name" {
  description = "PostgreSQL server name"
  value       = azurerm_postgresql_flexible_server.main.name
}

output "postgresql_fqdn" {
  description = "PostgreSQL server FQDN"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "postgresql_connection_string" {
  description = "PostgreSQL connection string"
  value       = "postgresql://${azurerm_postgresql_flexible_server.main.administrator_login}:${var.postgres_password}@${azurerm_postgresql_flexible_server.main.fqdn}:5432/${azurerm_postgresql_flexible_server_database.main.name}"
  sensitive   = true
}

output "postgresql_admin_login" {
  description = "PostgreSQL administrator login"
  value       = azurerm_postgresql_flexible_server.main.administrator_login
}

