import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiCall from '../../services/apiCall';

const OrderItem = () => {

    const [userOrderItems, setUserOrderItem] = useState([]);

    const navigate = useNavigate();

    useEffect(() => {
        // 

        const fetchOrderItem = async () => {
            const response=await apiCall.get("store/order-item/")
        }

    }, [])

    const redirectPayment = async () => {
        // redirect to Payment gateway
        const response = await apiCall.post("payment/info/", {})
        // navigate("");
    }

    return (
        <>

        </>
    )
}

export default OrderItem