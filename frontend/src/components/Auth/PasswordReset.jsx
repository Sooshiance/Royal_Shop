import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';

const PasswordReset = () => {

    const [user, setUser] = useState({ username: "", otp: "", new_password: "" });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const sendUserData = async () => {
        try {
            const response = await apiCall.post("user/password-reset/", {
                username: user.username,
                otp: user.otp,
                new_password: user.new_password
            });

            if (response.status_code === 200) {
                // You can navigate to another endpoint
                navigate("/login");
            } else {
                navigate("/password-reset");
            }
        } catch (error) {
            setError(error);
        }
    }

    if (error) return <div>Error fetching products: {error.message}</div>;

    return (
        <>
            <Header />
            Reset your Password
            <Footer />
        </>
    )
}

export default PasswordReset