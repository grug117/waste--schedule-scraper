variable "environment" {
  type    = string
  default = "dev"
}

variable "deploy_role_arn" {
  type    = string
  default = "arn:aws:iam::703775540847:role/waste-schedule-scraper-deploy-rol"
}

variable "session_name" {
  type    = string
  default = "deploy-waste-session"
}
