// src/components/Cart.jsx
import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchWithAuth, deleteWithAuth, putWithAuth } from '../../context/auth/authUtils';
import { useNavigate } from 'react-router-dom';
import { addProduct, removeProduct } from '../../context/cart/cartSlice';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';

const Cart = () => {

    const cartProducts = useSelector(state => state.cart.products);
    const [cart, setCart] = useState([]);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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

    const proceedToOrder = () => {
        navigate("/order");
    }

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error fetching cart data: {error.message}</div>;

    return (
        <>
            <Header />
            <h2>Shopping Cart</h2>
            {cart.length === 0 ? (
                <p>Your cart is empty.</p>
            ) : (
                <div>
                    {cart.map(item => (
                        <div key={item.pk}>
                            <img src={item.thumbnail} alt={item.product_title} height={250} width={250} />
                            <h3>{item.product.product_title}</h3>
                            <p>Quantity: {item.quantity}</p>
                            <button onClick={() => handleAddProduct(item)}>Increase product quantity</button>
                            <button onClick={() => handleRemoveProduct(item)}>Remove</button>
                        </div>
                    ))}
                </div>
            )}
            <Footer />
        </>
    );
};

export default Cart;