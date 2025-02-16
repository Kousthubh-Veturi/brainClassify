from fastapi import FastAPI
import tensorflow as tf
import app
from app.routes import upload, predict

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(predict.router, prefix="/predict", tags=["Predict"])


@app.get("/")
def home():
    return {"message": "Brain Tumor Classification API is running"}



