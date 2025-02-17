import React, { useState } from 'react';
import { submitFeedback } from '../services/api';

const FeedbackForm = ({ filename }) => {
    const [feedback, setFeedback] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await submitFeedback(filename, feedback);
            alert('Feedback submitted successfully!');
            setFeedback('');
        } catch (error) {
            alert('Failed to submit feedback.');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="mt-4">
            <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Provide feedback on the prediction"
                className="w-full border p-2"
                required
            />
            <button type="submit" className="mt-2 bg-blue-500 text-white px-4 py-2 rounded">
                Submit Feedback
            </button>
        </form>
    );
};

export default FeedbackForm;
