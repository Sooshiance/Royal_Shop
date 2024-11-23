import React from 'react';
import e1 from '../../assets/e1.jpg';
import { Container, Row, Image } from 'react-bootstrap';
import '../../styles/banner.css';

const Banner = () => {
    return (
        <>
            <Container fluid>
                <Row>
                    <Image src={e1} alt="Royal_Shop" className="banner-image" />
                </Row>
            </Container>
        </>
    )
}

export default Banner;