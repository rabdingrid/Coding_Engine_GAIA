# Variables can be overridden via terraform.tfvars or command line

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "ai-ta-2"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus2"
}

variable "container_app_env_name" {
  description = "Container Apps Environment name"
  type        = string
  default     = "ai-ta-RA-env"
}

variable "acr_name" {
  description = "Azure Container Registry name"
  type        = string
  default     = "aitaraacr1763805702"
}

variable "executor_image" {
  description = "Container image for code execution"
  type        = string
  default     = "aitaraacr1763805702.azurecr.io/executor-secure:v17-csharp"
}

variable "min_replicas" {
  description = "Minimum number of pre-warmed containers (for contest start)"
  type        = number
  default     = 1  # Scale to zero when idle (cost optimization)
}

variable "max_replicas" {
  description = "Maximum number of containers (for 200 students × 2 questions = 400 executions)"
  type        = number
  default     = 3  # Limited to 3 for testing
}

