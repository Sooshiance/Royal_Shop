import React from 'react'
import Header from '../Header';
import Footer from '../Footer';
import Banner from './Banner';
import { TopProduct } from './TopProduct';
import LatestComment from './LatestComment';

const Home = () => {
  return (
    <>
      <Header />
      <Banner />
      <TopProduct />
      <LatestComment />
      <Footer />
    </>
  )
}

export default Home