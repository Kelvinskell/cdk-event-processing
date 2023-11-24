from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources,
    aws_dynamodb as dynamodb,
    aws_apigateway as api_gateway
)


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create SQS queue
        queue = sqs.Queue(
            self, "CdkQueue",
            queue_name="info-queue",
            visibility_timeout=Duration.seconds(300),
        )

        # Create Dynaodb table
        table = dynamodb.Table(self, "Table",
                               table_name="employee-info",
                               partition_key=dynamodb.Attribute(name="workId", type=dynamodb.AttributeType.STRING),
                               sort_key=dynamodb.Attribute(name="secretId", type=dynamodb.AttributeType.STRING)
                               )

        # Create lambda function
        sqs_lambda = lambda_.Function(self, 'APISQSLambda',
                                      handler='lambda_handler.handler',
                                      runtime=lambda_.Runtime.PYTHON_3_10,
                                      code=lambda_.Code.from_asset('lambda'),
                                      function_name='APISQSLambda'
                                      )
        
        # Create SQS event source
        sqs_event_source = lambda_event_sources.SqsEventSource(queue)

        # Add SQS event source to lambda
        sqs_lambda.add_event_source(sqs_event_source)

        # Create API Gateway
        api = api_gateway.LambdaRestApi(self, 'Endpoint', handler=sqs_lambda)
        
