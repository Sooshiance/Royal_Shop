// // src/components/Store/CartItem
import React from 'react';
import Header from '../Header';
import Footer from '../Footer';
import { useSelector, useDispatch } from 'react-redux';
import { removeProduct, clearCart, addProduct } from '../../context/cart/cartSlice';
import { Container, Button } from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import { useNavigate } from 'react-router-dom';

const CartItem = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const cartProducts = useSelector(state => state.cart.products);

    const handleCart = () => {
        navigate('/cart');
    };

    return (
        <>
            <Header />
            <Container fluid>
                <h2>Shopping Cart</h2>
                {cartProducts.length === 0 ? (
                    <p>Your cart is empty.</p>
                ) : (
                    <div>
                        {cartProducts.map(item => (
                            <Container fluid key={item.pk}>
                                <Card>
                                    <Card.Img height={250} width={250} variant="top" src={item.thumbnail} />
                                    <Card.Body>
                                        <Card.Title>{item.product_title}</Card.Title>
                                        <Card.Text>Quantity: {item.quantity}</Card.Text>
                                        <Button onClick={() => dispatch(addProduct(item))}>Increase product quantity</Button>
                                        <Button onClick={() => dispatch(removeProduct(item.pk))}>Remove</Button>
                                    </Card.Body>
                                </Card>
                            </Container>
                        ))}
                        <Button onClick={() => dispatch(clearCart())}>Clear Cart</Button>
                        <Button onClick={handleCart}>Proceed to Checkout</Button>
                    </div>
                )}
            </Container>
            <Footer />
        </>
    );
}

export default CartItem;
