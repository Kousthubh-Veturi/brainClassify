from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from app.routes import upload, predict, feedback

app = FastAPI(title="Brain Tumor Classification API")

# Add CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(predict.router, prefix="/predict", tags=["Predict"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])

@app.get("/", tags=["Root"])
def home():
    return {
        "message": "Brain Tumor Classification API is running",
        "docs": "/docs",
        "endpoints": {
            "upload": "/upload",
            "predict": "/predict",
            "feedback": "/feedback"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring and verification scripts
    """
    return {
        "status": "ok",
        "api": "BrainClassify Backend API",
        "version": "1.0.0"
    }



