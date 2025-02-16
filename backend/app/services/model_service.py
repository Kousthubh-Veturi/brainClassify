import numpy as np
from PIL import Image
from io import BytesIO
from app.services.s3_service import download_image_from_s3
import requests
import os

def preprocess_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    image = image.resize((768, 768))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def predict_tumor(filename):
    try:
        image_bytes = download_image_from_s3(filename, decrypt=True)
        image_array = preprocess_image(image_bytes)
        model_url = os.getenv("TFS_URL", "http://localhost:8501/v1/models/brain_tumor:predict")
        response = requests.post(model_url, json={"instances": image_array.tolist()})

        if response.status_code != 200:
            raise Exception(f"Model prediction failed: {response.text}")
        predictions = response.json()["predictions"][0]
        tumor_classes = ["No Tumor", "Glioma", "Meningioma", "Pituitary"]
        predicted_label = tumor_classes[np.argmax(predictions)]

        return predicted_label

    except Exception as e:
        raise Exception(f"Failed to predict tumor: {e}")