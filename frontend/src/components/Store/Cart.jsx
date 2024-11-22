import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { sendWithAuth, fetchWithAuth } from '../../context/auth/authUtils';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { addProduct, removeProduct } from '../../context/cart/cartSlice';
import Header from '../Header';
import Footer from '../Footer';

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
            await sendWithAuth('store/cart/', navigate, {
                product_id: product.pk,
                quantity: 1
            });
        } catch (error) {
            console.error('Error adding product:', error);
            setError(error)
        } finally {
            setLoading(false);
        }
    };

    const handleRemoveProduct = async (product) => {
        dispatch(removeProduct(product.pk));
        try {
            await axios.delete(`store/cart/${product.pk}/`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
        } catch (error) {
            console.error('Error removing product:', error);
            setError(error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error fetching cart data: {error.message}</div>;

    return (
        <>
            <Header />
            <h2>Shopping Cart</h2>
            {cartProducts.length === 0 ? (
                <p>Your cart is empty.</p>
            ) : (
                <div>
                    {cartProducts.map(item => (
                        <div key={item.pk}>
                            <img src={item.thumbnail} alt={item.product_title} height={250} width={250} />
                            <h3>{item.product_title}</h3>
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