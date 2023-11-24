from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_event_sources
)


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "CdkQueue",
            visibility_timeout=Duration.seconds(300),
        )

        
