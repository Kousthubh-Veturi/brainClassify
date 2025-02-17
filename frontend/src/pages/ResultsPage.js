import React from 'react';

const ResultsPage = ({ prediction }) => {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-3xl font-bold mb-6">Prediction Result</h1>
            <div className="border p-6 rounded-md shadow-md text-center">
                <p className="text-xl">Prediction: <strong>{prediction}</strong></p>
            </div>
        </div>
    );
};

export default ResultsPage;
