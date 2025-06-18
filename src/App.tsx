// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/loginservice';
import Registro from './components/registrationservice';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Registro />} />
        {/* otras rutas: */}
      </Routes>
    </Router>
  );
}

export default App;
