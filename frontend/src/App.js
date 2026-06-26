import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Installers from './pages/Installers';
import RequestForm from './pages/RequestForm';
import Register from './pages/Register';
import Login from './pages/Login';

function App() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <NavBar />
      <div className="flex-grow-1 container py-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/installers" element={<Installers />} />
          <Route path="/request" element={<RequestForm />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;