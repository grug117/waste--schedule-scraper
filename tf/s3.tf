resource "aws_s3_bucket" "scheule_repo" {
  bucket = "${local.project_name}-repo-${var.environment}"
}

resource "aws_s3_bucket_acl" "schedule_repo_acl" {
  bucket = aws_s3_bucket.scheule_repo.id
  acl    = "public-read"
}
