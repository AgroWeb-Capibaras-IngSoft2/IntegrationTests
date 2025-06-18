// src/components/registrationservice.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import farmImg from '../assets/farm.png';

const Registro: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nombre: '',
    correo: '',
    contrasena: '',
    repetirContrasena: '',
    aceptoTerminos: false
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.contrasena !== formData.repetirContrasena) {
      alert('Las contraseñas no coinciden.');
      return;
    }
    if (!formData.aceptoTerminos) {
      alert('Debes aceptar los términos y condiciones.');
      return;
    }
    console.log('Datos registrados:', formData);
    alert('¡Registro exitoso!');
    navigate('/'); // opcional: vuelve al login tras registrarse
  };

  return (
    <div className="container mt-5">
      <div className="row align-items-center">
        {/* Imagen y mensaje */}
        <div className="col-md-6 text-center mb-4 mb-md-0">
          <h2>Productos frescos del campo a tu mesa</h2>
          <img
            src={farmImg}
            alt="Granja"
            className="img-fluid border rounded mt-3"
            style={{ maxWidth: '100%', height: 'auto' }}
          />
        </div>

        {/* Formulario de registro */}
        <div className="col-md-6">
          <h3 className="fw-bold mb-3">Crear una cuenta</h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Nombre y apellido</label>
              <input
                type="text"
                className="form-control"
                placeholder="Ej. Rodolfo Rivera"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Correo electrónico</label>
              <input
                type="email"
                className="form-control"
                placeholder="Ej. hey@rodolforivera.co"
                name="correo"
                value={formData.correo}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Contraseña</label>
              <input
                type="password"
                className="form-control"
                name="contrasena"
                value={formData.contrasena}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Repetir contraseña</label>
              <input
                type="password"
                className="form-control"
                name="repetirContrasena"
                value={formData.repetirContrasena}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-check mb-4">
              <input
                className="form-check-input"
                type="checkbox"
                name="aceptoTerminos"
                checked={formData.aceptoTerminos}
                onChange={handleChange}
                id="aceptoTerminos"
              />
              <label className="form-check-label" htmlFor="aceptoTerminos">
                Acepto los <a href="#">términos y condiciones</a> de servicio
              </label>
            </div>

            <div className="d-flex gap-2">
              <button type="submit" className="btn btn-success">
                Registrarme
              </button>
              <button
                type="button"
                className="btn btn-outline-success"
                onClick={() => navigate('/')}
              >
                Ya tengo cuenta
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Registro;
