import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_apigateway as apigw
from constructs import Construct

class ApiStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, *, plotting_function: lambda_.Function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = apigw.LambdaRestApi(
            self,
            "PlotApi",
            handler=plotting_function,
            proxy=False
        )

        plot_response = self.api.root.add_resource("plot")
        plot_response.add_method("GET")
        self.plot_url = f"{self.api.url}plot"

        cdk.CfnOutput(self, "PlotApiUrl", value=self.plot_url)
