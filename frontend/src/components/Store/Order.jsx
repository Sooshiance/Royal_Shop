// /src/components/Store/Order.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../Header';
import Footer from '../Footer';
import { fetchWithAuth } from '../../context/auth/authUtils';
import Card from 'react-bootstrap/Card';
import { Button } from 'react-bootstrap';
import apiCall from '../../services/apiCall';

const Order = () => {

  const [orders, setOrder] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetchWithAuth("store/orders/", navigate);
        console.log(response);
        setOrder(response); // Set the response data directly
      } catch (error) {
        setError(error);
        console.log(error.message);
      }
    };

    fetchOrders();
  }, [navigate]);

  const proceedToOrderItem = async () => {
    const token = localStorage.getItem("accessToken");

    if (!token) {
      navigate("/login");
    }

    try {
      const response = await apiCall.post("store/order-items/", {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (response.status === 201) {
        alert("accepted");
      }

      navigate("/order-item");
    } catch (error) {
      setError(error);
      console.log(error.message);
    }
  };

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
        {orders.length === 0 ? (
          <div>No Order</div>
        ) : (
          <div>
            {orders.map((order) => (
              <Card key={order.pk}>
                {order.pk}
              </Card>
            ))}
          </div>
        )}
        <Button onClick={proceedToOrderItem}>
          Proceed to OrderItem
        </Button>
      </div>
      <Footer />
    </>
  )
}

export default Order