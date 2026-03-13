import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_notifications as s3n
import aws_cdk.aws_lambda as lambda_
from constructs import Construct

class DataStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.bucket = s3.Bucket(
            self,
            "Bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        self.table = dynamodb.Table(
            self,
            "Table",
            partition_key=dynamodb.Attribute(
                name="bucket_name",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp_epoch_ms",
                type=dynamodb.AttributeType.NUMBER,
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        self.table.add_global_secondary_index(
            index_name="global_max_size_index",
            partition_key=dynamodb.Attribute(
                name="gsi1pk",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="total_size_bytes",
                type=dynamodb.AttributeType.NUMBER,
            ),
        )

        cdk.CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        cdk.CfnOutput(self, "TableName", value=self.table.table_name)

        self.size_tracking_function = lambda_.Function(
            self,
            'SizeTrackingFunction',
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler='handler.lambda_handler',
            code=lambda_.Code.from_asset('lambdas/size_tracking'),
            timeout=cdk.Duration.seconds(30),
            environment={
                'BUCKET_NAME': self.bucket.bucket_name,
                'TABLE_NAME': self.table.table_name,
            }
        )

        self.bucket.grant_read(self.size_tracking_function)
        self.table.grant_write_data(self.size_tracking_function)

        self.bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(self.size_tracking_function),
        )
        self.bucket.add_event_notification(
            s3.EventType.OBJECT_REMOVED,
            s3n.LambdaDestination(self.size_tracking_function),
        )
