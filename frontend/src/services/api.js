import axios from 'axios';
import { BASE_API_URL } from '../config';

export const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
        const response = await axios.post(`${BASE_API_URL}/upload`, formData);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getPrediction = async (filename) => {
    try {
        const response = await axios.post(`${BASE_API_URL}/predict`, { filename });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const submitFeedback = async (filename, feedback) => {
    try {
        const response = await axios.post(`${BASE_API_URL}/feedback`, { filename, feedback });
        return response.data;
    } catch (error) {
        throw error;
    }
};

