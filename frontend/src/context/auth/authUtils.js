// src/context/auth/authUtils
import apiCall from '../../services/apiCall';
// import { useNavigate } from 'react-router-dom';

export const fetchWithAuth = async (endpoint, navigate) => {
    const token = localStorage.getItem('accessToken');

    if (!token) {
        console.warn("No access token found, redirecting to login.");
        navigate('/login'); // Redirect to login if no token
        return null;
    }

    try {
        const response = await apiCall.get(endpoint, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 401) {
            console.error("Unauthorized, redirecting to login.");
            navigate('/login'); // Redirect to login if unauthorized
        } else {
            console.error("Failed to fetch data:", error);
        }
        throw error;
    }
};