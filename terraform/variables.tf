# Terraform Variables
# These can be overridden via terraform.tfvars or environment variables

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "ai-ta-2"
}

variable "container_app_name" {
  description = "Name of the Container App"
  type        = string
  default     = "executor-refactored-test"
}

variable "container_app_env_name" {
  description = "Name of the Container App Environment"
  type        = string
  default     = "ai-ta-RA-env-testing"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry"
  type        = string
  default     = "ait2codingengineacr"
}

variable "image_name" {
  description = "Name of the Docker image"
  type        = string
  default     = "executor-service-refactored"
}

variable "image_tag" {
  description = "Tag of the Docker image"
  type        = string
  default     = "latest"
}

variable "min_replicas" {
  description = "Minimum number of replicas"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum number of replicas"
  type        = number
  default     = 3
}

variable "cpu" {
  description = "CPU allocation per container"
  type        = number
  default     = 2.0
}

variable "memory" {
  description = "Memory allocation per container"
  type        = string
  default     = "4.0Gi"
}

variable "environment" {
  description = "Environment name (testing, staging, production)"
  type        = string
  default     = "testing"
}
