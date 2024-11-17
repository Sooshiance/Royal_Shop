import React, { useState, useEffect } from 'react';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';

const Products = () => {

    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await apiCall.get("store/all/products/");
                console.log("API response:", response);
                if (response && Array.isArray(response.data)) {
                    setProducts(response.data);
                } else if (Array.isArray(response.results)) {
                    setProducts(response.results);
                } else if (Array.isArray(response)) {
                    setProducts(response);
                } else {
                    throw new Error("Data is not an array");
                }
            } catch (error) {
                setError(error);
                console.log(error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error fetching products: {error.message}</div>;

    return (
        <>
            <Header />
            <div>
                {products.length > 0 ? (
                    products.map((product) => (
                        <Card style={{ width: '18rem' }}>
                            <Card.Img variant="top" src={product.thumbnail} />
                            <Card.Body>
                                <Card.Title>
                                    {product.product_name}
                                </Card.Title>
                                <Card.Text>
                                    {product?.description}
                                </Card.Text>
                                <Link to={`/products/${product.pk}`}>
                                    <Button variant="primary">See the details</Button>
                                </Link>
                            </Card.Body>
                        </Card>
                    ))
                ) : (
                    <div>No products available</div>
                )}
            </div>
            <Footer />
        </>
    );
};

export default Products