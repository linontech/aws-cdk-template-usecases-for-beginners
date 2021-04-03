
Hi, there! This is my tutorial CDK templates from [aws-cdk-smaples](https://github.com/aws-samples/aws-cdk-examples/tree/master/python)

for beginners to get used to use AWS Services to develop.

Table of Contents

- lambda-store-real-estate-open-data, Lambda fn to store data into S3 from https://plvr.land.moi.gov.tw


Steps to get yourself started,
In order to get the authority configuration more fit and clean to your use cases,
   you'd better follow the steps below, 

1. create IAM User called cdk-admin which attached the IAM policy 
   cdk-admin-customized-user-policy created with the following json. And then,
   use `aws configure` to switch the operating user to cdk-admin.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudformation:*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        },
        {
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::cdk-staging-bucket-*",
            "Effect": "Allow"
        }
    ]
}
```

