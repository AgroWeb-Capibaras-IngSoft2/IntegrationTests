import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import farmImg from '/src/assets/farm.jpeg';
import bcrypt from 'bcryptjs';
import '../index.css'; // Asegura que el CSS global se importe

const usersApiUrl = import.meta.env.VITE_API_USERS_URL;

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
    const response = await fetch(`${usersApiUrl}/users/register`, {
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
        hashPassword: formData.contrasena,
        username: formData.nombreUsuario
      })
    });

    if (response.ok) {
      const data = await response.json();
      alert('¡Registro exitoso!');
      console.log('Respuesta del servidor:', data);
      navigate('/');
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
  <div className="container-fluid p-0">
    <div className="row align-items-stretch" style={{ minHeight: '100vh' }}>
      <div className="col-md-6 d-flex flex-column align-items-center position-relative p-0">
        <img
          src={farmImg}
          alt="Granja"
          className="img-cover border rounded shadow-sm h-100 w-100"
          style={{ objectFit: 'cover', borderRadius: '0 0 0 1.5rem' }}
        />
      </div>
      <div className="col-md-6 d-flex align-items-center justify-content-center bg-light" style={{ background: 'rgba(255,255,255,0.95)', borderRadius: '0 1.5rem 1.5rem 0' }}>
        <div className="card shadow-lg w-100 border-0" style={{ maxWidth: '480px', borderRadius: '1.5rem', background: 'rgba(255,255,255,0.98)' }}>
          <div className="card-body p-5">
            <h2 className="fw-bold mb-4 text-center text-success" style={{ letterSpacing: '1px' }}>Crea una cuenta en AgroWeb</h2>
            <form onSubmit={handleSubmit} autoComplete="off">
              <div className="row g-3">
                {campos.map(({ label, name, type = 'text', inputMode, pattern }) => (
                  <div className="col-12 col-md-6" key={name}>
                    <label className="form-label fw-semibold text-secondary small mb-1">{label}</label>
                    <input
                      type={type}
                      className="form-control rounded-pill shadow-sm px-3 py-2"
                      name={name}
                      value={formData[name]}
                      onChange={handleChange}
                      required
                      {...(inputMode ? { inputMode } : {})}
                      {...(pattern ? { pattern } : {})}
                    />
                  </div>
                ))}
                <div className="col-12 col-md-6">
                  <label className="form-label fw-semibold text-secondary small mb-1">Tipo de documento</label>
                  <select
                    className="form-select rounded-pill shadow-sm px-3 py-2"
                    name="tipoDocumento"
                    value={formData.tipoDocumento}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Seleccione...</option>
                    <option value="C.C">C.C</option>
                  </select>
                </div>
                <div className="col-12">
                  <div className="form-check mb-2">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      name="aceptoTerminos"
                      checked={formData.aceptoTerminos}
                      onChange={handleChange}
                      id="aceptoTerminos"
                    />
                    <label className="form-check-label small text-secondary" htmlFor="aceptoTerminos">
                      Acepto los <a href="#" className="text-success text-decoration-underline">términos y condiciones</a> de servicio
                    </label>
                  </div>
                </div>
                <div className="col-12 d-grid gap-2 mt-2">
                  <button type="submit" className="btn btn-success rounded-pill py-2 fw-bold shadow-sm">
                    Registrarme
                  </button>
                  <button type="button" className="btn btn-outline-success rounded-pill py-2 fw-bold shadow-sm" onClick={handleIrAlLogin}>
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