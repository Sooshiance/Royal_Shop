import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../Header';
import Footer from '../Footer';
import apiCall from '../../services/apiCall';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
// import { useDispatch } from 'react-redux';

const Product = () => {

  const [product, setProduct] = useState({});
  const { pk } = useParams();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {

    const fetchProduct = async () => {
      try {
        const response = await apiCall.get(`store/product/${pk}`);
        console.log("API response:", response.data);
        setProduct(response.data);
      } catch (error) {
        setError(error);
        console.log(error);
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
            {product.product_title}
          </Card.Title>
          <Card.Text>
            {product.description}
          </Card.Text>
          <Button variant="primary">Add to  Cart</Button>
          <Card.Img height={250} width={250} variant="top" src={product.thumbnail} />
        </Card.Body>
        <Card.Footer className="text-muted">
          <small className="text-muted col-6">
            {product.price}
          </small>
          <small className="text-muted col-6">
            {product.old_price}
          </small>
        </Card.Footer>
      </Card>
      <Footer />
    </>
  )
}

export default Product