import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
// import { useDispatch } from 'react-redux';

const Product = () => {

  const [product, setProduct] = useState([]);
  const { pk } = useParams();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {

    const fetchProduct = async () => {
      try {
        const data = await apiCall.get(`store/each/product/${pk}/`);
        if (data) {
          setProduct(data);
          console.log(data);
        }
      } catch (error) {
        console.log(error);
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchProduct();

  }, [])

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error fetching products: {error.message}</div>;

  return (
    <>
      <Header />
      <Card className="text-center">
        <Card.Body>
          <Card.Title>
            {product.title}
          </Card.Title>
          <Card.Text>
            With supporting text below as a natural lead-in to additional content.
          </Card.Text>
          <Button variant="primary">Add to  Cart</Button>
        </Card.Body>
        {/* <Card.Footer className="text-muted">
          <small className="text-muted col-6">
            {product.price}
          </small>
          <small className="text-muted col-6">
            {product.old_price}
          </small>
        </Card.Footer> */}
      </Card>
      <Footer />
    </>
  )
}

export default Product