#!/usr/bin/env python3
import os
import aws_cdk as cdk
from stacks import *

app = cdk.App()

data = DataStack(
    app,
    "DataStack",
)

compute = ComputeStack(
    app,
    "ComputeStack",
    bucket=data.bucket,
    table=data.table,
    matplotlib_layer_arn=os.getenv("MATPLOTLIB_LAYER_ARN")
)

api = ApiStack(
    app,
    "ApiStack",
    plotting_function=compute.plotting_function
)

integration = IntegrationStack(
    app,
    "IntegrationStack",
    bucket=data.bucket,
    plot_api_url=api.plot_url
)

app.synth()
