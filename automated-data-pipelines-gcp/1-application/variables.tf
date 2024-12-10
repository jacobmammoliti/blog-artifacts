variable "project_id" {
  type        = string
  description = "(Required) The ID of the GCP project to deploy into."
}

variable "location" {
  type        = string
  description = "(Optional) The region to deploy the artfiact registry into."
  default     = "us-east1"
}