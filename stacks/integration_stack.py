import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_notifications as s3n
from constructs import Construct

class IntegrationStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, *, bucket: s3.Bucket, size_tracking_function: lambda_.Function, plot_api_url: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.driver_function = lambda_.Function(
            self,
            "DriverFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_asset("lambdas/driver"),
            timeout=cdk.Duration.seconds(60),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "PLOT_API_URL": plot_api_url,
            }
        )

        bucket.grant_read_write(self.driver_function)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(size_tracking_function),
        )
        bucket.add_event_notification(
            s3.EventType.OBJECT_REMOVED,
            s3n.LambdaDestination(size_tracking_function),
        )

        cdk.CfnOutput(self, "DriverFunctionName", value=self.driver_function.function_name)
