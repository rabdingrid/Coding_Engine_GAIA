# Terraform Outputs
# These values are displayed after terraform apply

output "container_app_url" {
  description = "URL of the code executor"
  value       = azurerm_container_app.executor.latest_revision_fqdn
}

output "container_app_name" {
  description = "Name of the Container App"
  value       = azurerm_container_app.executor.name
}

output "container_app_id" {
  description = "ID of the Container App"
  value       = azurerm_container_app.executor.id
}

output "acr_login_server" {
  description = "ACR login server URL"
  value       = data.azurerm_container_registry.acr.login_server
}

