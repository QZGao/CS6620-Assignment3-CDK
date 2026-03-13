# CS6620-Assignment3-CDK

## Demo steps

### 1. During the demo, git clone the CDK and code repo.

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

### 5. Go to the Cloudformation console and show the stacks.

TA - please check the stack creation timestamp.

TA - please check that under the resources tab of the stacks, it collectively shows three lambdas, one S3 bucket, one DynamoDB table, one REST API.

### 6. Manually invoke the newly created driver lambda in AWS console. 

TA - please check the contents of the DDB table, also check the newly generated plot.

### 0. Clean up before the demo

```powershell
cdk destroy --all --force
```