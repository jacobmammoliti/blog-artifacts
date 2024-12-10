variable "project_id" {
  type        = string
  description = "(Required) The ID of the GCP project to deploy into."
}

variable "location" {
  type        = string
  description = "(Optional) The region to deploy the artfiact registry into."
  default     = "us-east1"
}

variable "artifact_registry_admins" {
  type        = list(string)
  description = "(Required) A list of users, groups, or service accounts that are granted roles/artifactregistry.admin."
}