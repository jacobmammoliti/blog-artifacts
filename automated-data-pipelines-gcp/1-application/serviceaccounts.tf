resource "google_service_account" "scheduler_sa" {
  account_id   = "scheduler-sa"
  description  = "Cloud Scheduler service account; used to trigger scheduled Cloud Run jobs."
  display_name = "scheduler-sa"
}

resource "google_service_account" "cloudrun_sa" {
  account_id   = "cloudrun-sa"
  description  = "Cloud Run service account; used to authenticate to Google Sheets."
  display_name = "cloudrun-sa"
}

resource "google_cloud_run_v2_job_iam_member" "scheduler_sa" {
  location = google_cloud_run_v2_job.books_to_scrape.location
  name     = google_cloud_run_v2_job.books_to_scrape.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler_sa.email}"
}