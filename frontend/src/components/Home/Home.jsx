import React from 'react'
import Header from '../Header';
import Footer from '../Footer';
import Banner from './Banner';
import { TopProduct } from './TopProduct';

const Home = () => {
  return (
    <>
      <Header />
      <Banner />
      <TopProduct />
      <Footer />
    </>
  )
}

export default Home