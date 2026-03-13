import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_s3 as s3
from constructs import Construct

class ComputeStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, *, bucket: s3.Bucket, table: dynamodb.Table, matplotlib_layer_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        matplotlib_layer = lambda_.LayerVersion.from_layer_version_arn(
            self,
            'MatplotlibLayer',
            matplotlib_layer_arn,
        )

        self.size_tracking_function = lambda_.Function(
            self,
            'SizeTrackingFunction',
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler='handler.lambda_handler',
            code=lambda_.Code.from_asset('lambdas/size_tracking'),
            timeout=cdk.Duration.seconds(30),
            environment={
                'BUCKET_NAME': bucket.bucket_name,
                'TABLE_NAME': table.table_name,
            }
        )

        self.plotting_function = lambda_.Function(
            self,
            'PlottingFunction',
            runtime=lambda_.Runtime.PYTHON_3_12,
            architecture=lambda_.Architecture.X86_64,
            handler='handler.lambda_handler',
            code=lambda_.Code.from_asset('lambdas/plotting'),
            timeout=cdk.Duration.seconds(60),
            memory_size=1024,
            ephemeral_storage_size=cdk.Size.mebibytes(512),
            layers=[matplotlib_layer],
            environment={
                'BUCKET_NAME': bucket.bucket_name,
                'TABLE_NAME': table.table_name,
            }
        )

        bucket.grant_read(self.size_tracking_function)
        table.grant_write_data(self.size_tracking_function)
        table.grant_read_data(self.plotting_function)
        bucket.grant_put(self.plotting_function)
