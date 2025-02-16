from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.s3_service import upload_image_to_s3

router = APIRouter()

@router.post("/")
async def upload_image(file: UploadFile = File(...)):
    try:
        filename = upload_image_to_s3(file, encrypt=True)
        return {"message": "Image uploaded to S3 successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))