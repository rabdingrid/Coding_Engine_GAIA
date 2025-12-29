# Azure Redis Cache
resource "azurerm_redis_cache" "main" {
  name                = "ai-ta-ra-redis"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  capacity            = 0  # Basic tier (C0 - 250MB)
  family              = "C"
  sku_name            = "Basic"
  non_ssl_port_enabled = false
  minimum_tls_version  = "1.2"

  redis_configuration {
    maxmemory_reserved = 2
    maxmemory_delta    = 2
    maxmemory_policy   = "allkeys-lru"
  }

  tags = {
    environment = "production"
    purpose     = "coding-engine-cache"
    managed-by  = "terraform"
  }

  depends_on = [data.azurerm_resource_group.main]
}

# Output Redis connection details
output "redis_hostname" {
  value       = azurerm_redis_cache.main.hostname
  description = "Redis cache hostname"
}

output "redis_port" {
  value       = azurerm_redis_cache.main.port
  description = "Redis cache port"
}

output "redis_ssl_port" {
  value       = azurerm_redis_cache.main.ssl_port
  description = "Redis cache SSL port"
}

output "redis_primary_access_key" {
  value       = azurerm_redis_cache.main.primary_access_key
  sensitive   = true
  description = "Redis primary access key"
}

output "redis_secondary_access_key" {
  value       = azurerm_redis_cache.main.secondary_access_key
  sensitive   = true
  description = "Redis secondary access key"
}

