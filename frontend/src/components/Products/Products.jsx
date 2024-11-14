import React, { useState, useEffect } from 'react';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';

const Products = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data = await apiCall.get("products/");
                if (data) {
                    setProducts(data);
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
            {products.map((product) => (
                <Card key={product.pid} style={{ width: '18rem' }}> {/* Make sure to use a unique key */}
                    <Card.Body>
                        <Card.Title>{product?.title}</Card.Title>
                        <Card.Img src={product?.thumbnail} />
                        <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
                        <Card.Link>Card Link</Card.Link>
                        <Card.Link>Another Link</Card.Link>
                    </Card.Body>
                </Card>
            ))}
            <Footer />
        </>
    );
};

export default Products