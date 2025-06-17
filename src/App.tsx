// src/App.tsx
import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './components/loginservice'   // <-- Asegúrate de que la ruta coincida

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta de login en “/” */}
        <Route path="/" element={<Login />} />

        {/* Aquí luego agregarás más rutas, p.ej. Dashboard, Signup, etc. */}
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
        {/* <Route path="/signup" element={<Signup />} /> */}
      </Routes>
    </BrowserRouter>
  )
}

