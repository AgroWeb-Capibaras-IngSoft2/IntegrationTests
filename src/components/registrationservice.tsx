import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const Registro = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    middleName: '',
    surName1: '',
    surName2: '',
    bornDate: '',
    department: '',
    municipality: '',
    trail: '',
    email: '',
    typeDocument: '',
    numberDocument: '',
    phoneNumber: '',
    hashPassword: '',
    repeatHashPassword: '',
    username: '',
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
    if (formData.hashPassword !== formData.repeatHashPassword) {
      alert('Las contraseñas no coinciden.');
      return;
    }
    if (!formData.aceptoTerminos) {
      alert('Debes aceptar los términos y condiciones.');
      return;
    }

    try{
      const response= await fetch("http://localhost:5001/users/register",
        {
          method:'POST',
          headers:{
            'Content-Type': 'application/json'
          },
          body:JSON.stringify(formData)
        }
      );

      if (response.ok){
        const data = await response.json();
        console.log('Respuesta del backend:', data);
        alert('¡Registro exitoso!');
        
      }
      else{
        const error = await response.json();
        alert(`Error en el registro: ${error.mensaje || 'Error desconocido'}`);
      }
    }
    catch (error){
      console.error('Error en la petición:', error);
      alert('Ocurrió un error al conectar con el servidor.');
    }
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
              { label: 'Nombre', name: 'firstName' },
              { label: 'Segundo nombre', name: 'middleName' },
              { label: 'Primer apellido', name: 'surName1' },
              { label: 'Segundo apellido', name: 'surName2' },
              { label: 'Fecha de nacimiento', name: 'bornDate', type: 'date' },
              { label: 'Departamento', name: 'department' },
              { label: 'Municipio', name: 'municipality' },
              { label: 'Ruta', name: 'trail' },
              { label: 'Correo electrónico', name: 'email', type: 'email' },
              { label: 'Tipo de documento', name: 'typeDocument' },
              { label: 'Número de documento', name: 'numberDocument' },
              { label: 'Número de teléfono', name: 'phoneNumber' },
              { label: 'Nombre de usuario', name: 'username' },
              { label: 'Contraseña', name: 'hashPassword', type: 'password' },
              { label: 'Repetir contraseña', name: 'repeatHashPassword', type: 'password' }
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
