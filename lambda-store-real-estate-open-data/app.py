import os
import botocore
import boto3
from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    core,
)


class LambdaCronStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFn = lambda_.Function(
            self, "Singleton",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
        )

        # Run every day at 6PM UTC
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-TUE',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))

        region_name = self.node.try_get_context("location_constraint")
        s3 = boto3.resource('s3', region_name=region_name)
        try:
            s3.meta.client.head_bucket(Bucket=os.environ.get('BUCKET_NAME'))
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                s3.create_bucket(Bucket=os.environ.get('BUCKET_NAME'),
                                 CreateBucketConfiguration={'LocationConstraint': region_name})


app = core.App()
LambdaCronStack(app, "LambdaCronExample")
app.synth()
