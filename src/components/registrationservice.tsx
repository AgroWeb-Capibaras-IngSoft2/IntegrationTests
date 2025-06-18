import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import farmImg from '/src/assets/farm.png';
import bcrypt from 'bcryptjs';

const Registro = () => {
  const navigate = useNavigate();

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

  const handleSubmit = async (e:React.FormEvent) => {
    e.preventDefault();
    if (formData.contrasena!== formData.repetirContrasena) {
      alert('Las contraseñas no coinciden.');
      return;
    }
    if (!formData.aceptoTerminos) {
      alert('Debes aceptar los términos y condiciones.');
      return;
    }

  try {
    const response = await fetch('http://localhost:5001/users/register', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        firstName: formData.nombre,
        middleName: formData.segundoNombre,
        surName1: formData.apellido1,
        surName2: formData.apellido2,
        bornDate: formData.fechaNacimiento,
        department: formData.departamento,
        municipality: formData.municipio,
        trail: formData.ruta,
        email: formData.correo,
        typeDocument: formData.tipoDocumento,
        numberDocument: formData.numeroDocumento,
        phoneNumber: formData.telefono,
        hashPassword: bcrypt.hashSync(formData.contrasena, 10),
        username: formData.nombreUsuario
      })
    });

    if (response.ok) {
      const data = await response.json();
      alert('¡Registro exitoso!');
      console.log('Respuesta del servidor:', data);
    } else {
      const errorData = await response.json();
      alert('Error en el registro: ' + (errorData.error || response.statusText));
    }
  } catch (error) {
    alert('Error de red: ' + error.message);
  }


  };

  const handleIrAlLogin = () => {
    navigate('/');
  };

  const campos = [
    { label: 'Nombre', name: 'nombre' },
    { label: 'Segundo nombre', name: 'segundoNombre' },
    { label: 'Primer apellido', name: 'apellido1' },
    { label: 'Segundo apellido', name: 'apellido2' },
    { label: 'Fecha de nacimiento', name: 'fechaNacimiento', type: 'date', inputMode: 'numeric', pattern: '\\d{4}-\\d{2}-\\d{2}' },
    { label: 'Departamento', name: 'departamento' },
    { label: 'Municipio', name: 'municipio' },
    { label: 'Ruta', name: 'ruta' },
    { label: 'Correo electrónico', name: 'correo', type: 'email' },
    { label: 'Número de documento', name: 'numeroDocumento' },
    { label: 'Número de teléfono', name: 'telefono' },
    { label: 'Nombre de usuario', name: 'nombreUsuario' },
    { label: 'Contraseña', name: 'contrasena', type: 'password' },
    { label: 'Repetir contraseña', name: 'repetirContrasena', type: 'password' }
  ];

  return (
    <div className="container mt-4">
      <header className="text-center mb-4">
        <h1 style={{ color: 'green' }}>Agroweb</h1>
      </header>
      <div className="row align-items-start">
        <div className="col-md-6 mb-4 d-flex flex-column align-items-center position-relative">
          <h2 className="position-absolute top-0 start-50 translate-middle-x text-center bg-white px-2" style={{ marginTop: '-1.5rem', zIndex: 1 }}>
            Productos frescos del campo a tu mesa
          </h2>
          <img
            src={farmImg}
            alt="Granja"
            className="img-fluid border rounded shadow-sm mt-5"
            style={{ width: '100%', maxWidth: '500px', height: 'auto' }}
          />
        </div>

        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-body">
              <h3 className="fw-bold mb-4 text-center">Crear una cuenta</h3>
              <form onSubmit={handleSubmit}>
                <div className="row">
                  {campos.map(({ label, name, type = 'text', inputMode, pattern }) => (
                    <div className="col-md-6 mb-3" key={name}>
                      <label className="form-label fw-semibold">{label}</label>
                      <input
                        type={type}
                        className="form-control"
                        name={name}
                        value={formData[name]}
                        onChange={handleChange}
                        required
                        {...(inputMode ? { inputMode } : {})}
                        {...(pattern ? { pattern } : {})}
                      />
                    </div>
                  ))}

                  <div className="col-md-6 mb-3">
                    <label className="form-label fw-semibold">Tipo de documento</label>
                    <select
                      className="form-select"
                      name="tipoDocumento"
                      value={formData.tipoDocumento}
                      onChange={handleChange}
                      required
                    >
                      <option value="">Seleccione...</option>
                      <option value="C.C">C.C</option>
                    </select>
                  </div>

                  <div className="col-12 mb-3">
                    <div className="form-check">
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
                  </div>

                  <div className="col-12 d-grid gap-2">
                    <button type="submit" className="btn btn-success">
                      Registrarme
                    </button>
                    <button type="button" className="btn btn-outline-success" onClick={handleIrAlLogin}>
                      Ya tengo cuenta
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Registro;
