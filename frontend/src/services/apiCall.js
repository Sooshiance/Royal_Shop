// src/services/apiCall
import axios from 'axios';

const apiCall = axios.create({
    baseURL: "http://127.0.0.1:8080/api/v1/",

    timeout: 3000,
    
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
    }
});

export default apiCall;