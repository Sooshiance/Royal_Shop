import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';
import Card from 'react-bootstrap/Card';
import { Button } from 'react-bootstrap';

const OrderItem = () => {
    const [userOrderItem, setUserOrderItem] = useState({});
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchOrderItem = async () => {
            try {
                const token = localStorage.getItem("accessToken");

                const response = await apiCall.get("store/order-items/", {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    }
                });

                if (response.status === 200) {
                    console.log('Fetched order item data:', response.data);
                    setUserOrderItem(response.data);
                }
            } catch (error) {
                setError(error);
                console.log('Error fetching order item:', error.message);
            }
        }

        fetchOrderItem();
    }, [navigate]);

    const redirectPayment = async () => {
        const token = localStorage.getItem("accessToken");

        try {
            const response = await apiCall.post("payment/info/", {}, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (response.status === 201) {
                alert("Payment info accepted");
                navigate("payment/");
            }
        } catch (error) {
            setError(error);
            console.log('Error redirecting to payment:', error.message);
        }
    }

    if (error) return (
        <>
            <Header />
            <div>Error fetching Order Item: {error.message}</div>
            <Footer />
        </>
    );

    return (
        <>
            <Header />
            <div>
                <Card>
                    <Card.Body>
                        <Card.Title>Order Item Details</Card.Title>
                        <Card.Text>Order ID: {userOrderItem.pk}</Card.Text>
                        <Card.Text>Order: {userOrderItem.order}</Card.Text>
                        <Card.Text>Final Price: {userOrderItem.final_price}</Card.Text>
                    </Card.Body>
                </Card>
                <Button onClick={redirectPayment}>
                    Go to Payment
                </Button>
            </div>
            <Footer />
        </>
    );
}

export default OrderItem;
