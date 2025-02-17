import React from 'react';

const PredictionResult = ({ prediction }) => {
    return (
        <div className="p-4 border rounded-md shadow-md bg-white">
            <h2 className="text-xl font-bold mb-2">Prediction Result</h2>
            <p className="text-lg">Tumor Prediction: <span className="font-semibold">{prediction.prediction}</span></p>
            <p className="text-sm text-gray-600">Filename: {prediction.filename}</p>
        </div>
    );
};

export default PredictionResult;
