import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';
import { Container, Row, Col, Card } from 'react-bootstrap';

const Rate = () => {
    const { pk } = useParams();
    const [rates, setRate] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRate = async () => {
            try {
                const response = await apiCall.get(`club/rates/${pk}`);
                if (response && response.data) {
                    console.log('Fetched data:', response.data);
                    setRate(response.data);
                }
            } catch (error) {
                setError(error);
            }
        };
        fetchRate();
    }, [pk]);

    if (error) return <div>Error fetching rates: {error.message}</div>;

    console.log('Rates state:', rates);

    return (
        <>
            <Header />
            <Container>
                <Row>
                    {rates.length > 0 ? (
                        rates.map((rate) => (
                            <Col xs={12} sm={6} md={4} lg={3} key={rate.pk} className="mb-4">
                                <Card>
                                    <Card.Body>
                                        <Card.Title>{rate.user_profile}</Card.Title>
                                        <Card.Text>{rate.txt}</Card.Text>
                                    </Card.Body>
                                </Card>
                            </Col>
                        ))
                    ) : (
                        <Col>
                            <div>No Rate available!</div>
                        </Col>
                    )}
                </Row>
            </Container>
            <Footer />
        </>
    );
};

export default Rate;