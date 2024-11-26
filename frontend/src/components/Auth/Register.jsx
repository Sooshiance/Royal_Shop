import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiCall from '../../services/apiCall';
import Header from '../Header';
import Footer from '../Footer';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const Register = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const navigate = useNavigate();
    
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        
        e.preventDefault();

        try {
            const response = await apiCall.post("user/register/",
                { username, password }
            )

            if (response) {
                navigate("/");
            }
        } catch (error) {
            setError(error);
            console.log(error.message);
        } 
    }

    if (error) return <div>Error fetching user data: {error.message}</div>;

    return (
        <>
            <Header />
            <Form onSubmit={handleSubmit} className=''>
                <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
            <Footer />
        </>
    )
}

export default Register