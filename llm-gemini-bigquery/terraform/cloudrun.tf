resource "google_cloud_run_v2_job" "slack_bot_gemini" {
  name                = "slack-bot-gemini"
  location            = "us-east1"
  deletion_protection = false

  template {
    template {
      containers {
        image = "us-east1-docker.pkg.dev/proj-puffin-83326/af-us-east1-docker/slackbotgemini:latest"

        env {
          name = "DATABASE_URI"
          value_source {
            secret_key_ref {
              secret  = data.google_secret_manager_secret.database_uri.id
              version = "1"
            }
          }
        }

        env {
          name = "SLACK_BOT_TOKEN"
          value_source {
            secret_key_ref {
              secret  = data.google_secret_manager_secret.slack_bot_token.id
              version = "1"
            }
          }
        }

        env {
          name = "SLACK_SIGNING_SECRET"
          value_source {
            secret_key_ref {
              secret  = data.google_secret_manager_secret.slack_signing_secret.id
              version = "1"
            }
          }
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