terraform {
  cloud {
    organization = "gregford117"

    workspaces {
      name = "waste-schedule-scraper"
    }
  }


  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.49.0"
    }
  }
}

provider "aws" {
  region                  = "eu-west-1"
  shared_config_file      = "./config"
  shared_credentials_file = "./credentials"
}
