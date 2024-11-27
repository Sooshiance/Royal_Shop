import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';

const VerifyOTP = () => {

    const [otp, setOTP] = useState("");
    const [username, setUsername] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const sendOTP = async() => {
        try {
            const response = await apiCall.post("user/verify-otp/", { otp, username });

            if (response.status_code === 200) {
                navigate("/password-reset");
            } else {
                navigate("/verify-otp");
            }
        } catch (error) {
            setError(error);
        }
    }

    if (error) return <div>Error fetching products: {error.message}</div>;

    return (
        <>
            <Header />
            Enter the given OTP 
            <Footer />
        </>
    )
}

export default VerifyOTP