import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';

const Rate = () => {
    const { pk } = useParams();
    const [rates, setRate] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRate = async () => {
            try {
                const response = await apiCall.get(`club/rates/${pk}`);
                if (response && response.data) {
                    console.log('Fetched data:', response.data);
                    setRate(response.data);
                }
            } catch (error) {
                setError(error);
            }
        };
        fetchRate();
    }, [pk]);

    if (error) return <div>Error fetching rates: {error.message}</div>;

    console.log('Rates state:', rates);

    return (
        <>
            <Header />
            <div>
                {rates.length > 0 ? (
                    rates.map((rate) => (
                        <div key={rate.pk}>
                            <h3>
                                {rate.user_profile}
                            </h3>
                            <h1>
                                {rate.txt}
                            </h1>
                        </div>
                    ))
                ) : (
                    <div>No Rate available!</div>
                )}
            </div>
            <Footer />
        </>
    );
};

export default Rate;