// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './components/loginservice'   // <-- Asegúrate de que la ruta coincida
import Register from './components/Register'; // ruta correcta según tu estructura

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta de login en “/” */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Aquí luego agregarás más rutas, p.ej. Dashboard, Signup, etc. */}
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
        {/* <Route path="/signup" element={<Signup />} /> */}
      </Routes>
    </BrowserRouter>
  )
}

