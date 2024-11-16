import './App.css';
import { Route, Routes } from 'react-router-dom';
import PrivateRoute from './components/PrivateRoute';
import Home from './components/Home/Home';
import Products from './components/Products/Products';
import Login from './components/Auth/Login';
import Logout from './components/Auth/Logout';
import Profile from './components/Client/Profile';

function App() {
  return (
    <>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/login" element={<Login />} />
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
        </Routes>
      </div>
    </>
  );
}

export default App;
