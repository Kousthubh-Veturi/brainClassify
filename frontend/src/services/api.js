import axios from 'axios';
import { BASE_API_URL } from '../config';

// Create axios instance with base URL
const api = axios.create({
    baseURL: BASE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Add request interceptor for debugging
api.interceptors.request.use(
    (config) => {
        console.log(`API Request to: ${config.baseURL}${config.url}`, config);
        return config;
    },
    (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
    }
);

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => {
        console.log('API Response:', response);
        return response;
    },
    (error) => {
        console.error('API Error:', error.response || error.message || error);
        return Promise.reject(error);
    }
);

/**
 * Upload MRI image to the backend
 * @param {File} file - The image file to upload
 * @returns {Promise<Object>} - The response with filename
 */
export const uploadImage = async (file) => {
    console.log('Uploading image:', file.name, file.size, file.type);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        console.log('Sending upload request to:', `${BASE_API_URL}/upload`);
        const response = await api.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        console.log('Upload successful, response:', response.data);
        return response.data;
    } catch (error) {
        console.error('Upload failed:', error);
        throw error;
    }
};

/**
 * Get prediction for an uploaded image
 * @param {string} filename - The filename of the uploaded image
 * @returns {Promise<Object>} - The prediction result
 */
export const getPrediction = async (filename) => {
    console.log('Getting prediction for:', filename);
    try {
        const response = await api.post('/predict', { filename });
        console.log('Prediction result:', response.data);
        return response.data;
    } catch (error) {
        console.error('Prediction failed:', error);
        throw error;
    }
};

/**
 * Submit feedback for a prediction
 * @param {string} filename - The filename of the image
 * @param {Object} feedback - The feedback data
 * @returns {Promise<Object>} - The response
 */
export const submitFeedback = async (filename, feedback) => {
    console.log('Submitting feedback:', filename, feedback);
    try {
        const response = await api.post('/feedback', { 
            filename, 
            rating: feedback.rating,
            comment: feedback.text
        });
        console.log('Feedback submitted successfully:', response.data);
        return response.data;
    } catch (error) {
        console.error('Feedback submission failed:', error);
        throw error;
    }
};

export default api;

