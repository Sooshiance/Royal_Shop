import React from 'react';
import e2 from '../../assets/e2.jpg';
import { Container, Row, Col, Image } from 'react-bootstrap';
import '../../styles/banner.css';

const Banner = () => {
    return (
        <>
            <Container fluid>
                <Row>
                    <Col xs={12} md={8} lg={6} >
                        <Image src={e2} alt="Royal_Shop" className="banner-image" fluid />
                    </Col>
                </Row>
            </Container>
        </>
    )
}

export default Banner;