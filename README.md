# CS6620-Assignment3-CDK

## Demo steps

### 1. Clone and reset to the pre-deadline commit

```powershell
git clone https://github.com/QZGao/CS6620-Assignment3-CDK.git
cd CS6620-Assignment3-CDK
git reset --hard <COMMIT_BEFORE_DEADLINE>
```

### 2. Install dependencies

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Set the deployment environment

```powershell
$env:AWS_DEFAULT_REGION="us-west-1"
$env:CDK_DEFAULT_REGION="us-west-1"
$env:MATPLOTLIB_LAYER_ARN="arn:aws:lambda:us-west-1:595673261927:layer:matplotlib-layer:1"
```

### 4. Bootstrap if needed, then deploy

```powershell
cdk bootstrap
cdk deploy --all --require-approval never
```

### 5. Show the stacks in CloudFormation

Stacks to show:

* `DataStack`
* `ComputeStack`
* `ApiStack`
* `IntegrationStack`

TA checks:

* stack creation timestamps
* resources collectively include 3 Lambdas, 1 S3 bucket, 1 DynamoDB table, 1 REST API

### 6. Get the driver Lambda name

```powershell
aws cloudformation describe-stacks --stack-name IntegrationStack --query "Stacks[0].Outputs[?OutputKey=='DriverFunctionName'].OutputValue" --output text
```

### 7. Invoke the driver Lambda

```powershell
aws lambda invoke --function-name <DRIVER_FUNCTION_NAME> --cli-binary-format raw-in-base64-out --payload '{}' response.json

cat response.json
```

### 8. Get the bucket and table names

```powershell
aws cloudformation describe-stacks --stack-name DataStack --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text

aws cloudformation describe-stacks --stack-name DataStack --query "Stacks[0].Outputs[?OutputKey=='TableName'].OutputValue" --output text
```

### 9. Show the DynamoDB contents and generated plot

```powershell
aws dynamodb scan --table-name <TABLE_NAME>
aws s3 ls s3://<BUCKET_NAME>
aws s3 cp s3://<BUCKET_NAME>/plot ./plot.png
```

TA checks:

* DynamoDB table contains the size history records
* the plot object is generated in the bucket

### 0. Clean up before the demo

```powershell
cdk destroy --all --force
```