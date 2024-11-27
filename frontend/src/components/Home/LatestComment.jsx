import React, { useState, useEffect } from 'react';
import apiCall from '../../services/apiCall';
import Card from 'react-bootstrap/Card';
import { Container } from 'react-bootstrap';

const LatestComment = () => {

    const [comments, setComment] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchComments = async () => {
            try {
                const response = await apiCall.get("club/comments/");
                if (response) {
                    setComment(response.data);
                    console.log(response.data);
                }
            } catch (error) {
                setError(error);
            }
        }

        fetchComments();
    }, []);

    if (error) return <div>Error fetching comments: {error.message}</div>;

    return (
        <>
            {
                comments.length > 0 ? (
                    comments.map((comment) => (
                        <Card key={comment.pk}>
                            <Card.Header>
                                {comment.user_profile.username}
                            </Card.Header>
                            <Card.Body>
                                <Card.Title>
                                    {comment.status}
                                </Card.Title>
                                <Card.Text>
                                    {comment.txt}
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    ))
                ) : (
                    <div>
                        No comments
                    </div>
                )
            }

        </>
    )
}

export default LatestComment;