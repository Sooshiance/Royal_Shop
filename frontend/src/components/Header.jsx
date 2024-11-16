// src/components/Header.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Container, Nav, Form, FormControl, Button } from 'react-bootstrap';
import authService from '../services/authService';

const Header = () => {

  const isAuthenticated = authService.isAuthenticated();

  return (
    <>
      <Navbar expand="lg" className="bg-body-tertiary">
        <Container fluid>
          <Link to="/">
            <Navbar.Brand>Royal Shop</Navbar.Brand>
          </Link>
          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="me-auto my-2 my-lg-0"
              style={{ maxHeight: '100px' }}
              navbarScroll
            >
              <Nav.Link as={Link} to="/">Home</Nav.Link>
              <Nav.Link as={Link} to="/products">All Products</Nav.Link>
              {isAuthenticated ? (
                <>
                  <Nav.Link as={Link} to="/logout">Logout</Nav.Link>
                  <Nav.Link as={Link} to="/profile">Profile</Nav.Link>
                </>
              ) : (
                <Nav.Link as={Link} to="/login">Login</Nav.Link>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default Header