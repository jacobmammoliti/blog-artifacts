locals {
  cloudrun_iam_roles = [
    "roles/run.invoker",
    "roles/bigquery.dataViewer",
  ]
}

resource "google_service_account" "cloudrun_sa" {
  account_id   = "cloudrun-sa"
  description  = "Cloud Run service account."
  display_name = "cloudrun-sa"
}

resource "google_cloud_run_v2_job_iam_member" "couldrun_sa" {
  for_each = toset(local.cloudrun_iam_roles)
  location = google_cloud_run_v2_job.get_job_postings.location
  name     = google_cloud_run_v2_job.get_job_postings.name
  role     = each.value
  member   = "serviceAccount:${google_service_account.cloudrun_sa.email}"
}