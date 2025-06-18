import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Registro = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    correo: '',
    contrasena: '',
    repetirContrasena: '',
    aceptoTerminos: false
  });

  const handleChange = (e: { target: { name: any; value: any; type: any; checked: any; }; }) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e: { preventDefault: () => void; }) => {
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
  };

  return (
    <div className="container mt-5">
      <div className="row align-items-center">
        <div className="col-md-6">
          <h2 className="text-center">
            Productos frescos del 
            campo a tu mesa</h2>

          <img
            src="/assets/farm.png"
            alt="Granja"
            className="img-fluid border rounded"
            style={{ width: '500px', height: 'auto' }} 
          />
        </div>

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

            <div className="form-check mb-3">
              <input
                className="form-check-input"
                type="checkbox"
                name="aceptoTerminos"
                checked={formData.aceptoTerminos}
                onChange={handleChange}
              />
              <label className="form-check-label">
                Acepto los <a href="#">términos y condiciones</a> de servicio
              </label>
            </div>

            <div className="d-flex gap-2">
              <button type="submit" className="btn btn-success">
                Registrarme
              </button>
              <button type="button" className="btn btn-outline-success">
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
