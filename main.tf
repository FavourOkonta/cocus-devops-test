
resource "aws_lambda_function" "cocus_lambda" {
  filename         = "cocus.zip" # Change to the appropriate python script to be deployed
  function_name    = "cocus-test"
  role             = aws_iam_role.cocus_lambda_role.arn
  handler          = "cocus.lambda_handler"
  runtime          = "python3.11"  # Change to the appropriate runtime
}

resource "aws_iam_role" "cocus_lambda_role" {
  name = "cocus_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cocus-attachment" {
  role       = "${aws_iam_role.cocus_lambda_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}
