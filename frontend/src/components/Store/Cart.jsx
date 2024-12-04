// src/components/Cart.jsx
import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchWithAuth, sendWithAuth } from '../../context/auth/authUtils';
import { useNavigate } from 'react-router-dom';
import { addProduct, removeProduct } from '../../context/cart/cartSlice';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';
import { Container, Row, Col, Card, Button, Form } from 'react-bootstrap';

const Cart = () => {

    const cartProducts = useSelector(state => state.cart.products);
    const [cart, setCart] = useState([]);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [coupon_code, setCoupon] = useState("");

    useEffect(() => {
        const fetchCart = async () => {
            try {
                const data = await fetchWithAuth('store/cart/', navigate);
                setCart(data);
            } catch (error) {
                console.error('Error fetching cart data:', error);
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchCart();
    }, [navigate]);

    const handleAddProduct = async (product) => {
        dispatch(addProduct(product));
        try {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/login');
            }
            const response = await apiCall.put(`store/cart/${product.pk}/`, { quantity: 1 }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            console.log(response.status);
        } catch (error) {
            console.error('Error adding product:', error);
            setError(error);
        } finally {
            setLoading(false);
        }
    };

    const handleRemoveProduct = async (product) => {
        dispatch(removeProduct(product.pk));
        try {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/login');
            }
            const response = await apiCall.delete(`store/cart/${product.pk}/`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error removing product:', error);
            setError(error);
        } finally {
            setLoading(false);
        }
    };

    const proceedToOrder = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            navigate('/login');
        }

        try {
            const res = await apiCall.post("store/orders/", { coupon_code }, {
                headers: { Authorization: `Bearer ${token}` },
            })
            if (res.status === 201) {
                alert("your coupon code accepted!");
            }
            console.log(res.detail);
            console.log(res.status);
            navigate("/order");
        } catch (error) {
            setError(error);
        } finally {
            setLoading(false);
        }
    }

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error fetching cart data: {error.message}</div>;

    return (
        <>
            <Header />
            <Container>
                <Row className="mb-4">
                    <Col>
                        <h2>Shopping Cart</h2>
                        {cart.length === 0 ? (
                            <p>Your cart is empty.</p>
                        ) : (
                            cart.map(item => (
                                <Card key={item.pk} className="mb-3">
                                    <Row noGutters>
                                        <Col md={4}>
                                            <Card.Img src={item.thumbnail} alt={item.product.product_title} />
                                        </Col>
                                        <Col md={8}>
                                            <Card.Body>
                                                <Card.Title>{item.product.product_title}</Card.Title>
                                                <Card.Text>Quantity: {item.quantity}</Card.Text>
                                                <Button variant="success" onClick={() => handleAddProduct(item)}>Increase Quantity</Button>
                                                <Button variant="danger" className="ml-2" onClick={() => handleRemoveProduct(item)}>Remove</Button>
                                            </Card.Body>
                                        </Col>
                                    </Row>
                                </Card>
                            ))
                        )}
                    </Col>
                </Row>
                {cart.length > 0 && (
                    <Row>
                        <Col md={4}>
                            <Form onSubmit={(e) => e.preventDefault()}>
                                <Form.Group>
                                    <Form.Label>Coupon Code:</Form.Label>
                                    <Form.Control
                                        type="text"
                                        value={coupon_code}
                                        onChange={(e) => setCoupon(e.target.value)}
                                        placeholder="Enter coupon code"
                                    />
                                </Form.Group>
                                <Button variant="primary" onClick={proceedToOrder}>Proceed to Order</Button>
                            </Form>
                        </Col>
                    </Row>
                )}
            </Container>
            <Footer />
        </>
    );
};

export default Cart;