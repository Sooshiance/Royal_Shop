import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import Header from '../Header';
import Footer from '../Footer';
import AdvancedSearch from './AdvancedSearch';
import ProductList from './ProductList';
import User from './User';
import ProductTreshold from './ProductThreshold';

const AdminWrapper = () => {

    const navigate = useNavigate();

    const navigateUpdatingPage = () => {
        navigate("/config-staff/admin/access/granted/");
    }

    return (
        <>
            <Header />
            <AdvancedSearch />
            <ProductTreshold />
            <ProductList />
            <User />
            <Button variant="success" onClick={navigateUpdatingPage} >
                Do you need to update your staff in api? 
            </Button>
            <Footer />
        </>
    )
}

export default AdminWrapper