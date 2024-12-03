import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const OrderItem = () => {

    const [userOrder, setUserOrder] = useState([]);

    const navigate = useNavigate();

    useEffect(() => {
        // 
    }, [])

    const redirectPayment = () => {
        // redirect to Payment gateway
        // navigate("");
    }

    return (
        <>

        </>
    )
}

export default OrderItem