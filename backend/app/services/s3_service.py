import boto3
import os
from botocore.exceptions import NoCredentialsError

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

S3_BUCKET = os.getenv("S3_BUCKET")

