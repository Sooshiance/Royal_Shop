import './App.css';
import { Route, Routes } from 'react-router-dom';
import Home from './components/Home/Home';
import Products from './components/Products/Products';

function App() {
  return (
    <>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/products' element={<Products />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
