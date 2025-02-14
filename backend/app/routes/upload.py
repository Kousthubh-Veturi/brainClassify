from fastapi import APIRouter, File, UploadFile, HTTPException
import boto3
import os
from app.services.db_service import save_metadata
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

AWS_KEYACCESS = os.getenv("AWS_ACCESS_KEY")
AWS_KEYSECRET = os.getenv("AWS_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client("s3", aws_access_key_id=AWS_KEYACCESS, aws_secret_access_key=AWS_KEYSECRET)

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        s3.put_object(Bucket=S3_BUCKET, Key=file.filename, Body=image_bytes)
        save_metadata(file.filename, "upload completed")
        return {"message": "Image uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

