from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
from app.services.db_service import update_prediction

load_dotenv()
router = APIRouter()
AWS_KEYACCESS = os.getenv("AWS_ACCESS_KEY")
AWS_KEYSECRET = os.getenv("AWS_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")

s3 = boto3.client("s3", aws_access_key_id=AWS_KEYACCESS, aws_secret_access_key=AWS_KEYSECRET)

model = tf.keras.models.load_model("model.h5")



