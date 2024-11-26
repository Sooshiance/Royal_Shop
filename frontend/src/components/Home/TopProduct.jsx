import React, { useState, useEffect } from 'react';
import apiCall from '../../services/apiCall';
import Spinner from 'react-bootstrap/Spinner';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

export const TopProduct = () => {

    const [products, setProduct] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {

                const response = await apiCall.get("club/rates/highest-product/");

                console.log(response.data);

                if (response) {
                    setProduct(response.data);
                }
            } catch (error) {
                console.log(error);
                setError(error);
            } finally {
                setLoading(false);
            }
        }

        fetchProducts();
    }, [])

    if (loading) return (
        <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
        </Spinner>
    );

    if (error) return <div>Error fetching products: {error.message}</div>;

    return (
        <>
            <h2>Top Rated Products by viewers:</h2>
            {products.length > 0 ? (
                products.map((product) => (
                    <Card key={product.id} style={{ width: '18rem' }}>
                        <Card.Img variant="top" src={product.thumbnail} />
                        <Card.Body>
                            <Card.Title>{product.product_title}</Card.Title>
                            <Card.Text>{product.description}</Card.Text>
                            <Link to={`/products/${product.id}`}>
                                <Button variant="primary">See the details</Button>
                            </Link>
                            <Card.Footer className="text-muted">
                                <small className="text-muted col-6">{product.price}</small>
                                <small className="text-muted col-6">{product.old_price}</small>
                            </Card.Footer>
                        </Card.Body>
                    </Card>
                ))
            ) : (
                <div>No products available</div>
            )}
        </>
    )
}