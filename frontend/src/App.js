import './App.css';
import { Route, Routes } from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute';
import NoPage from './components/NoPage';
import Home from './components/Home/Home';
import Products from './components/Store/Products';
import Product from './components/Store/Product';
import Login from './components/Auth/Login';
import Logout from './components/Auth/Logout';
import Profile from './components/Client/Profile';
import CartItem from './components/Store/CartItem';
import Cart from './components/Store/Cart';
import Register from './components/Auth/Register';
import Rate from './components/Store/Rate';
import CreateRate from './components/Store/CreateRate';
import LatestComment from './components/Home/LatestComment';
import Comment from './components/Home/Comment';
import RequestOTP from './components/Auth/RequestOTP';
import VerifyOTP from './components/Auth/VerifyOTP';
import PasswordReset from './components/Auth/PasswordReset';
import AdminWrapper from './components/Admin/AdminWrapper';
import AllConfig from './components/Admin/Config/AllConfig';
import Order from './components/Store/Order';
import OrderItem from './components/Store/OrderItem';

function App() {
  return (
    <>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/products/:pk" element={<Product />} />
          <Route path="/products/:pk/rate" element={<Rate />} />
          <Route path="/cart-item" element={<CartItem />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/comments" element={<LatestComment />} />
          <Route path="/request-otp" element={<RequestOTP />} />
          <Route path="/verify-otp" element={<VerifyOTP />} />
          <Route path="/password-reset" element={<PasswordReset />} />
          <Route path="/logout" element={
            <PrivateRoute>
              <Logout />
            </PrivateRoute>
          } />
          <Route path="/profile" element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          } />
          <Route path="/cart" element={
            <PrivateRoute>
              <Cart />
            </PrivateRoute>
          } />
          <Route path="/order" element={
            <PrivateRoute>
              <Order />
            </PrivateRoute>
          } />
          <Route path="/order-item" element={
            <PrivateRoute>
              <OrderItem />
            </PrivateRoute>
          } />
          <Route path="/comments/create" element={
            <PrivateRoute>
              <Comment />
            </PrivateRoute>
          } />
          <Route path="/products/:pk/create/rate" element={
            <PrivateRoute>
              <CreateRate />
            </PrivateRoute>
          } />
          <Route path="nonsense/admin/access-granted/statistics" element={
            <PrivateRoute>
              <AdminWrapper />
            </PrivateRoute>
          } />
          <Route path="nonsense/admin/access-granted/config" element={
            <PrivateRoute>
              <AllConfig />
            </PrivateRoute>
          } />
          <Route path='*' element={<NoPage />} />
        </Routes>
      </div>
    </>
  );
}

export default App;