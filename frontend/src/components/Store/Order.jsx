import React, { useState } from 'react';
import apiCall from '../../services/apiCall';
import { useNavigate } from 'react-router-dom';

const Order = () => {

  const [coupon, setCoupon] = useState("");

  const navigate = useNavigate();

  checkCoupon = async () => {
    // 

    const response = await apiCall.post("");

    if (response.status === 200) {
      alert("");
    }
  }

  return (
    <>

    </>
  )
}

export default Order