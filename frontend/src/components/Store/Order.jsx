// /src/components/Store/Order.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';

const Order = () => {

  const [orderItem, setOrderItem] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    //
  }, [])

  return (
    <>
      <Header />
      Order
      <Footer />
    </>
  )
}

export default Order