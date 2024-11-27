import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { sendWithAuth } from '../../context/auth/authUtils';
import { useNavigate } from 'react-router-dom';
import Header from '../Header';
import Footer from '../Footer';
import { Container, Row, Col, Form } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';

const CreateRate = () => {
    const { pk } = useParams();
    const navigate = useNavigate();
    const [rate, setRate] = useState({ vote: '', txt: '' });
    const [error, setError] = useState(null);

    const sendUserRate = async (e) => {

        e.preventDefault();

        try {
            const product_id = pk;
            await sendWithAuth(`club/rates/create/${product_id}/`, navigate, {
                vote: rate.vote,
                txt: rate.txt,
            });
            navigate(`/products/${pk}`);
        } catch (error) {
            console.error("Error submitting rate:", error);
            setError(error);
        }
    };

    if (error) return <div>Error fetching cart data: {error.message}</div>;

    return (
        <>
            <Header />
            <Container className="mt-3">
                <Row>
                    <Col md={6} className="mx-auto">
                        <Form onSubmit={sendUserRate}>
                            <Form.Group className="mb-3">
                                <Form.Label>Rate (1-5)</Form.Label>
                                <Form.Control
                                    type="number"
                                    min="1"
                                    max="5"
                                    value={rate.vote}
                                    onChange={(e) => setRate({ ...rate, vote: e.target.value })}
                                    placeholder="Rate (1-5)"
                                    required
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Your Comment</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    value={rate.txt}
                                    onChange={(e) => setRate({ ...rate, txt: e.target.value })}
                                    placeholder="Your comment..."
                                />
                            </Form.Group>
                            <Button variant="primary" type="submit">
                                Send Your Rate
                            </Button>
                        </Form>
                    </Col>
                </Row>
            </Container>
            <Footer />
        </>
    );
};

export default CreateRate