import React, { useState } from 'react';
import ImageUpload from '../components/ImageUpload';
import PredictionResult from '../components/PredictionResult';
import FeedbackForm from '../components/FeedbackForm';
import { getPrediction } from '../services/api';

const UploadPage = () => {
    const [filename, setFilename] = useState('');
    const [prediction, setPrediction] = useState(null);

    const handleUploadSuccess = async (uploadedFilename) => {
        setFilename(uploadedFilename);
        try {
            const result = await getPrediction(uploadedFilename);
            setPrediction(result);
        } catch (error) {
            alert('Failed to get prediction.');
        }
    };

    return (
        <div className="max-w-lg mx-auto mt-10">
            <h1 className="text-2xl font-bold mb-4">Brain Tumor Classifier</h1>
            <ImageUpload onUploadSuccess={handleUploadSuccess} />
            {prediction && (
                <>
                    <PredictionResult prediction={prediction} />
                    <FeedbackForm filename={filename} />
                </>
            )}
        </div>
    );
};

export default UploadPage;
