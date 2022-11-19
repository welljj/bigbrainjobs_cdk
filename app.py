#!/usr/bin/env python3
import os

import aws_cdk as cdk

from bigbrainjobs_cdk.bigbrainjobs_cdk_stack import BigbrainjobsCdkStack


app = cdk.App()
BigbrainjobsCdkStack(
    app,
    "BigbrainjobsCdkStack",
    cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
