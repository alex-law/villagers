# Which AWS account
$accountNumber = "590184003877"
$accountName = "dev"

# Get AWS ECR password
aws ecr get-login-password --region eu-west-2 --profile $accountName | docker login --username AWS --password-stdin "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com"

# Update version number tag
$VersionContent = Get-Content .\version_number.txt
$VersionNumber = [int]$VersionContent
$VersionNumber += 1
$BuildNumber = "0.0.$VersionNumber"
$VersionNumber | Out-File .\version_number.txt

# Build docker image
docker compose build

# Tag with latest for ECR
docker tag villagersflaskapp:latest "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/flask:latest"
docker tag mongo:latest "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/mongo:latest"

# Now push to ECR
docker push "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/flask:latest"
docker push "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/mongo:latest"

# Now add version number for ECR
docker tag villagersflaskapp:latest "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/flask:$BuildNumber"
docker tag mongo:latest "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/mongo:$BuildNumber"

# Finally push these to ECR too
docker push "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/flask:$BuildNumber"
docker push "$accountNumber.dkr.ecr.eu-west-2.amazonaws.com/villagers/mongo:$BuildNumber"