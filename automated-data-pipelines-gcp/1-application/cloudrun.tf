resource "google_cloud_run_v2_job" "books_to_scrape" {
  name     = "books-to-scrape"
  location = var.location

  template {
    template {
      containers {
        image = "${var.location}-docker.pkg.dev/${var.project_id}/${var.location}-docker-registry/bookstoscrape:1.0"

        env {
          name  = "SPREADSHEET_NAME"
          value = "BooksToScrape"
        }

        env {
          name  = "WORKSHEET_NAME"
          value = "Books"
        }

        resources {
          limits = {
            cpu    = "1"
            memory = "512Mi"
          }
        }
      }
      service_account = google_service_account.cloudrun_sa.email
    }
  }
}