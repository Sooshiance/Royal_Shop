// src/components/Client/Profile.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchWithAuth } from '../../context/auth/authUtils';
import Header from '../Header';
import Footer from '../Footer';

const Profile = () => {

    const [profile, setProfile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await fetchWithAuth("user/profile/", navigate);
                if (data) {
                    setProfile(data);
                }
            } catch (error) {
                console.error("Failed to fetch profile:", error.detail);
            }
        };

        fetchProfile();
    }, [navigate]);

    return (
        <>
            <Header />
            <div>Profile Page</div>
            <div>
                {profile ? (
                    <h1>{profile.username}</h1>
                ) : (
                    <p>Loading...</p>
                )}
            </div>
            <Footer />
        </>
    )
}

export default Profile