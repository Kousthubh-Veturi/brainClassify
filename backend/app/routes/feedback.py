from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.s3_service import update_feedback

router = APIRouter()
class FeedbackRequest(BaseModel):
    filename: str
    feedback: str 
@router.post("/")
async def submit_feedback(request: FeedbackRequest):
    try:
        update_feedback(request.filename, request.feedback)
        return {"message": "Feedback recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))