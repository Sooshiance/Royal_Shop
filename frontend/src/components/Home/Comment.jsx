import React, { useState } from 'react';
import { sendWithAuth } from '../../context/auth/authUtils';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Form } from 'react-bootstrap';

const Comment = () => {

    const [comment, setComment] = useState({ txt: "", status: "" });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const sendUserComment = async (e) => {
        e.preventDefault();

        try {
            const response = await sendWithAuth("comments/create/", navigate,
                {
                    txt: comment.txt,
                    status: comment.status
                }
            )

            if (response.status_code == 200) {
                setComment(response);
                navigate("/");
            }
        } catch (error) {
            setError(error);
        }
    }

    if (error) return <div>Error fetching comments: {error.message}</div>;

    return (
        <>
            <Container className="mt-3">
                Suggestion or Criticism
                <Row>
                    <Col md={6} className="mx-auto">
                        <Form onSubmit={sendUserComment}>
                            <Form.Group className="mb-3">
                                <Form.Label>Status of your opinion</Form.Label>
                                <Form.Control
                                    type="number"
                                    value={comment.status}
                                    onChange={(e) => setComment({ ...comment, vote: e.target.value })}
                                    placeholder="Status (1-2)"
                                    required
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label>Your Comment</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    value={comment.txt}
                                    onChange={(e) => setComment({ ...comment, txt: e.target.value })}
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
        </>
    )
}

export default Comment;