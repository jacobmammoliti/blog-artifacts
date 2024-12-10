resource "google_cloud_scheduler_job" "books_to_scrape_daily_job" {
  name             = "books-to-scrape-daily"
  region           = var.location
  description      = "Trigger Cloud Run job every day at 03:00 AM EST."
  schedule         = "0 3 * * *"
  time_zone        = "America/Toronto"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.books_to_scrape.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.books_to_scrape.name}:run"

    oauth_token {
      service_account_email = google_service_account.scheduler_sa.email
    }
  }
}