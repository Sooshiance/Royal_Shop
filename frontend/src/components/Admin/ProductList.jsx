import React, { useState } from 'react';
import { fetchWithAuth } from '../../context/auth/authUtils';
import { Button, Card, Container, Row, Col, Spinner, Alert } from 'react-bootstrap';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const seeProductList = async (status) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetchWithAuth(`dashboard/product/list/ ? status = ${status}`);
            if (response.status_code === 200) {
                const data = await response.json();
                setProducts(data);
            } else {
                setError(response.error);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
            <Container>
                <h1 className="my-4">Product List</h1>
                <div className="mb-3">
                    <Button variant="success" onClick={() => seeProductList('full')}>See In Stock Products</Button>
                    <Button variant="danger" onClick={() => seeProductList('empty')} className="ml-2">See Out of Stock Products</Button>
                </div>

                {loading && <Spinner animation="border" variant="primary" />}
                {error && <Alert variant="danger">{error}</Alert>}

                <Row>
                    {products.map(product => (
                        <Col key={product.pk} md={4} className="mb-4">
                            <Card>
                                <Card.Img variant="top" src={product.thumbnail} alt={product.product_title} />
                                <Card.Body>
                                    <Card.Title>{product.product_title}</Card.Title>
                                    <Card.Text>
                                        Price: ${product.price}<br />
                                        {product.in_stock ? 'In Stock' : 'Out of Stock'}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                        </Col>
                    ))}
                </Row>
            </Container>
        </>
    );
}

export default ProductList;