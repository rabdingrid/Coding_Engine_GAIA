# Variables for PostgreSQL deployment

variable "postgres_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
  # Generate a secure password: openssl rand -base64 32
  # Or set via: export TF_VAR_postgres_password="your-password"
}

