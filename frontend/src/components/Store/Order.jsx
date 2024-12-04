// /src/components/Store/Order.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../Header';
import Footer from '../Footer';
import { fetchWithAuth } from '../../context/auth/authUtils';

const Order = () => {

  const [orders, setOrder] = useState([]);

  const [error, setError] = useState({});

  const navigate = useNavigate();

  useEffect(() => {
    // fetch OrderItem from api

    const fetchOrderItem = async () => {
      try {
        const response = await fetchWithAuth("store/orders/");
        setOrder(response);
      } catch (error) {
        setError(error);
      }
    };

    fetchOrderItem();

  }, [orderItem])

  return (
    <>
      <Header />
      <div>
        {orders.length > 0 ? (
          orders.map((order) => (
            <Card key={order.pk} style={{ width: '18rem' }}>
              <Card.Img variant="top" src={order.cart.pk} />
              <Card.Body>
                <Card.Title>
                  {order.user.username}
                </Card.Title>
                <Card.Text>
                </Card.Text>
                <Card.Footer className="text-muted">
                  <small className="text-muted col-6">
                    {order.total_price}
                  </small>
                </Card.Footer>
              </Card.Body>
            </Card>
          ))
        ) : (
          <div>No Order available</div>
        )}
      </div>
      <Footer />
    </>
  )
}

export default Order