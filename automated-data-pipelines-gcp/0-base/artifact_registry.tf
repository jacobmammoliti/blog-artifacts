module "docker_artifact_registry" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric.git//modules/artifact-registry?ref=v35.0.0"
  project_id = var.project_id
  location   = var.location
  name       = format("%s-docker-registry", var.location)
  format     = { docker = { standard = {} } }
  iam = {
    "roles/artifactregistry.admin" = var.artifact_registry_admins
  }
}