import aws_cdk as core
import aws_cdk.assertions as assertions

from bigbrainjobs_cdk.bigbrainjobs_cdk_stack import BigbrainjobsCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in bigbrainjobs_cdk/bigbrainjobs_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BigbrainjobsCdkStack(app, "bigbrainjobs-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
