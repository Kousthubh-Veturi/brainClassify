from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.model_service import predict_tumor

router = APIRouter()

class PredictionRequest(BaseModel):
    filename: str

@router.post("/")
async def predict(request: PredictionRequest):
    try:
        prediction = predict_tumor(request.filename)
        return {"filename": request.filename, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))