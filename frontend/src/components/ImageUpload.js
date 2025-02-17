import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadImage } from '../services/api';

const ImageUpload = ({ onUploadSuccess }) => {
    const [isUploading, setIsUploading] = useState(false);
    const { getRootProps, getInputProps } = useDropzone({
        accept: 'image/*',
        onDrop: async (acceptedFiles) => {
            setIsUploading(true);
            try {
                const file = acceptedFiles[0];
                const response = await uploadImage(file);
                onUploadSuccess(response.filename);
            } catch (error) {
                alert('Failed to upload image');
            }
            setIsUploading(false);
        },
    });

    return (
        <div {...getRootProps()} className="border-2 border-dashed p-6 text-center cursor-pointer hover:bg-gray-100">
            <input {...getInputProps()} />
            {isUploading ? (
                <p className="text-blue-500">Uploading...</p>
            ) : (
                <p className="text-gray-700">Drag & drop an MRI image here, or click to select.</p>
            )}
        </div>
    );
};

export default ImageUpload;
