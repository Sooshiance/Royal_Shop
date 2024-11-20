// src/context/auth/authUtils
import apiCall from '../../services/apiCall';

export const fetchWithAuth = async (endpoint, navigate) => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        navigate('/login');
        return null;
    }
    try {
        const response = await apiCall.get(endpoint, {
            headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 401) {
            navigate('/login');
        } else {
            console.error("Failed to fetch data:", error);
        }
        throw error;
    }
};

export const sendWithAuth = async (endpoint, navigate, data) => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        navigate('/login');
        return null;
    }
    try {
        const response = await apiCall.post(endpoint, data, {
            headers: { Authorization: `Bearer ${token}`, }
        });
        return response.data; // Return the response data
    } catch (error) {
        if (error.response && error.response.status === 401) {
            navigate('/login');
        } else {
            console.error("Failed to send data:", error);
        }
        throw error;
    }
};

export const putWithAuth = async (endpoint, navigate, data) => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        navigate('/login');
        return null;
    }
    try {
        const response = await apiCall.put(endpoint, data, {
            headers: { Authorization: `Bearer ${token}`, }
        });
        return response.data; // Return the response data
    } catch (error) {
        if (error.response && error.response.status === 401) {
            navigate('/login');
        } else {
            console.error("Failed to send data:", error);
        }
        throw error;
    }
};

export const deleteWithAuth = async (endpoint, navigate, data) => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        navigate('/login');
        return null;
    }
    try {
        const response = await apiCall.delete(endpoint, data, {
            headers: { Authorization: `Bearer ${token}`, }
        });
        console.log(response.status);
        return response.status
    } catch (error) {
        if (error.response && error.response.status === 401) {
            navigate('/login');
        } else {
            console.error("Failed to send data:", error);
        }
        throw error;
    }
};