import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Registro = () => {
  const [formData, setFormData] = useState({
    nombre: '',
    segundoNombre: '',
    apellido1: '',
    apellido2: '',
    fechaNacimiento: '',
    departamento: '',
    municipio: '',
    ruta: '',
    correo: '',
    tipoDocumento: '',
    numeroDocumento: '',
    telefono: '',
    contrasena: '',
    repetirContrasena: '',
    nombreUsuario: '',
    aceptoTerminos: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
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
          <h2 className="text-center">Productos frescos del campo a tu mesa</h2>
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
            {[
              { label: 'Nombre', name: 'nombre' },
              { label: 'Segundo nombre', name: 'segundoNombre' },
              { label: 'Primer apellido', name: 'apellido1' },
              { label: 'Segundo apellido', name: 'apellido2' },
              { label: 'Fecha de nacimiento', name: 'fechaNacimiento', type: 'date' },
              { label: 'Departamento', name: 'departamento' },
              { label: 'Municipio', name: 'municipio' },
              { label: 'Ruta', name: 'ruta' },
              { label: 'Correo electrónico', name: 'correo', type: 'email' },
              { label: 'Tipo de documento', name: 'tipoDocumento' },
              { label: 'Número de documento', name: 'numeroDocumento' },
              { label: 'Número de teléfono', name: 'telefono' },
              { label: 'Nombre de usuario', name: 'nombreUsuario' },
              { label: 'Contraseña', name: 'contrasena', type: 'password' },
              { label: 'Repetir contraseña', name: 'repetirContrasena', type: 'password' }
            ].map(({ label, name, type = 'text' }) => (
              <div className="mb-3" key={name}>
                <label className="form-label">{label}</label>
                <input
                  type={type}
                  className="form-control"
                  name={name}
                  value={formData[name]}
                  onChange={handleChange}
                  required
                />
              </div>
            ))}

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
