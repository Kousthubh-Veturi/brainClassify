import os
import uuid
from fastapi import UploadFile
from PIL import Image
import io
import numpy as np

class ImageService:
    def __init__(self, upload_dir="uploads"):
        """
        Initialize the image service with the upload directory
        
        Args:
            upload_dir (str): Directory where images are stored
        """
        self.upload_dir = upload_dir
        
        # Create upload directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
    
    async def save_upload(self, file: UploadFile) -> str:
        """
        Save an uploaded file to the upload directory
        
        Args:
            file (UploadFile): The uploaded file
            
        Returns:
            str: The filename of the saved file
        """
        # Generate a unique filename with original extension
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Read file contents
        contents = await file.read()
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return filename
    
    def load_image(self, filename: str):
        """
        Load an image from the upload directory
        
        Args:
            filename (str): The filename of the image to load
            
        Returns:
            np.ndarray: The image as a numpy array
        """
        file_path = os.path.join(self.upload_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image {filename} not found")
        
        # Open and preprocess the image
        with Image.open(file_path) as img:
            # Convert to RGB if it's not already
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Resize to model input size (assuming 224x224 for standard models)
            img = img.resize((224, 224))
            
            # Convert to numpy array and normalize
            img_array = np.array(img) / 255.0
            
            return img_array
    
    def get_image_path(self, filename: str) -> str:
        """
        Get the full path of an image
        
        Args:
            filename (str): The filename of the image
            
        Returns:
            str: The full path of the image
        """
        return os.path.join(self.upload_dir, filename)
    
    def delete_image(self, filename: str) -> bool:
        """
        Delete an image from the upload directory
        
        Args:
            filename (str): The filename of the image to delete
            
        Returns:
            bool: True if the image was deleted, False otherwise
        """
        file_path = os.path.join(self.upload_dir, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        
        return False

# Create a singleton instance
image_service = ImageService() 