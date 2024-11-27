import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';

const RequestOTP = () => {

    const [username, setUsername] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const sendUsername = async () => {
        try {
            const response = await apiCall.post("user/password-reset-request/", { username });

            if (response.status_code === 200) {
                navigate("/verify-otp");
            } else {
                navigate("/request-otp");
            }
        } catch (error) {
            setError(error);
            navigate("/request-otp");
        }
    };

    if (error) return <div>Error fetching products: {error.message}</div>;

    return (
        <>
            <Header />
            Enter your username
            <Footer />
        </>
    )
}

export default RequestOTP