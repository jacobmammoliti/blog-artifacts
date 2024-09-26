data "google_secret_manager_secret" "database_uri" {
  secret_id = "database_uri"
}

data "google_secret_manager_secret" "slack_bot_token" {
  secret_id = "slack_bot_token"
}

data "google_secret_manager_secret" "slack_signing_secret" {
  secret_id = "slack_signing_secret"
}