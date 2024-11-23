import React, { useState, useEffect } from 'react';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';
import Spinner from 'react-bootstrap/Spinner';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';

export const TopProduct = () => {

    const [products, setProduct] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                data = await apiCall.get("");

                if (data) {
                    setProduct(data);
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
            <Header />
            <div>
                {products.length > 0 ? (
                    products.map((product) => {
                        <Card key={product.pk} style={{ width: '18rem' }}>
                            <Card.Img variant="top" src={product.thumbnail} />
                            <Card.Body>
                                <Card.Title>
                                    {product.product_title}
                                </Card.Title>
                                <Card.Text>
                                    {product.description}
                                </Card.Text>
                                <Link to={`/products/${product.pk}`}>
                                    <Button variant="primary">See the details</Button>
                                </Link>
                                <Card.Footer className="text-muted">
                                    <small className="text-muted col-6">
                                        {product.price}
                                    </small>
                                    <small className="text-muted col-6">
                                        {product.old_price}
                                    </small>
                                </Card.Footer>
                            </Card.Body>
                        </Card>
                    })
                ) :
                    <div>
                        No products available
                    </div>
                }
            </div>
            <Footer />
        </>
    )
}