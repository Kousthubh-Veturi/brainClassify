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

def upload_image_to_s3(file, encrypt=False):
    filename = file.filename
    try:
        image_bytes = file.file.read()
        s3.put_object(Bucket=S3_BUCKET, Key=filename, Body=image_bytes)
        print(f"Image uploaded successfully: {filename}")
        return filename

    except NoCredentialsError:
        raise Exception("⚠️ AWS credentials not found.")
    except Exception as e:
        raise Exception(f"Failed to upload image to S3: {e}")
    

def download_image_from_s3(filename, decrypt=False):
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=filename)
        image_bytes = response["Body"].read()
        return image_bytes

    except Exception as e:
        raise Exception(f"Failed to download image from S3: {e}")
    
def list_images_in_s3():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        if "Contents" not in response:
            return []
        return [obj["Key"] for obj in response["Contents"]]

    except Exception as e:
        raise Exception(f"❌ Failed to list images in S3: {e}")
    
def delete_image_from_s3(filename):
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=filename)
        print(f"✅ Image deleted successfully: {filename}")
    except Exception as e:
        raise Exception(f"❌ Failed to delete image from S3: {e}")
    
