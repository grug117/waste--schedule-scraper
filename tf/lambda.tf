resource "aws_lambda_layer_version" "deps_layer" {
  filename   = "../dependencies.zip"
  layer_name = "${local.project_name}-scraper-dependencies-${var.environment}"

  compatible_runtimes = ["python3.8"]
}
