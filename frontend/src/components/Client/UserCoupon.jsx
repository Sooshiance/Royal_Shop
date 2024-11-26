import React, { useEffect, useReducer } from 'react';
import { fetchWithAuth } from '../../context/auth/authUtils';
import Spinner from 'react-bootstrap/Spinner';
import Card from 'react-bootstrap/Card';
import Badge from 'react-bootstrap/Badge';

const initialState = {
    coupons: [],
    remainingTimes: {},
    loading: true,
    error: null,
};

const reducer = (state, action) => {
    switch (action.type) {
        case 'FETCH_SUCCESS':
            return {
                ...state,
                coupons: action.payload,
                loading: false,
            };
        case 'FETCH_ERROR':
            return {
                ...state,
                error: action.payload,
                loading: false,
            };
        case 'UPDATE_TIMES':
            return {
                ...state,
                remainingTimes: action.payload,
            };
        default:
            return state;
    }
};

const UserCoupon = () => {
    const [state, dispatch] = useReducer(reducer, initialState);

    useEffect(() => {
        const fetchUserCoupons = async () => {
            try {
                const response = await fetchWithAuth("user/user-coupon/timeout/");
                console.log(response);
                if (response) {
                    dispatch({ type: 'FETCH_SUCCESS', payload: response });
                }
            } catch (error) {
                dispatch({ type: 'FETCH_ERROR', payload: error });
            }
        };

        fetchUserCoupons();
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            const newTimes = {};
            state.coupons.forEach((coupon) => {
                const createdAt = new Date(coupon.created_at).getTime();
                const expirationParts = coupon.coupon.expiration.split(' ');
                const days = parseInt(expirationParts[0], 10);
                const timeParts = expirationParts[1].split(':');
                const hours = parseInt(timeParts[0], 10);
                const minutes = parseInt(timeParts[1], 10);
                const seconds = parseInt(timeParts[2], 10);
                const expirationDuration = ((days * 24 + hours) * 60 + minutes) * 60 + seconds; // Convert to seconds
                const expirationTime = createdAt + expirationDuration * 1000; // Convert to milliseconds
                const remainingTime = expirationTime - Date.now();
                newTimes[coupon.pk] = remainingTime;
            });
            dispatch({ type: 'UPDATE_TIMES', payload: newTimes });
        }, 1000);

        return () => clearInterval(interval);
    }, [state.coupons]);

    if (state.loading) return (
        <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
        </Spinner>
    );

    if (state.error) return <div>Error fetching coupons: {state.error.message}</div>;

    const formatTime = (milliseconds) => {
        if (milliseconds <= 0) return "Expired";
        const totalSeconds = Math.floor(milliseconds / 1000);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        return `${hours}h ${minutes}m ${seconds}s`;
    };

    return (
        <div>
            {state.coupons.map((coupon) => (
                <Card key={coupon.pk} className="mb-3">
                    <Card.Body>
                        <Card.Title>{coupon.coupon.title}</Card.Title>
                        <Card.Text>
                            Status: {coupon.is_used ? "Used" : "Active"}
                        </Card.Text>
                        <Card.Text>
                            Remaining Time: {formatTime(state.remainingTimes[coupon.pk])}
                        </Card.Text>
                        <Badge bg="success">{coupon.coupon.coupon_type}</Badge>
                    </Card.Body>
                </Card>
            ))}
        </div>
    );
};

export default UserCoupon;