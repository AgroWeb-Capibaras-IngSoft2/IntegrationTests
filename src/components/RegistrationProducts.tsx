import { desc } from 'framer-motion/client';

import { useState } from 'react';
import RegisProductImg from '/src/assets/RegisProduct.jpg';
const RegistrationProducts = () => {
  const [formData, setFormData] = useState({
    name: '',
    caterogy: '',
    price: '',
    unit: '',
    imageUrl: null,
    stock: '',
    origin: '',
    description: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    if (type === 'file') {
      setFormData({
        ...formData,
        imageUrl: files[0]
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const data = new FormData();
      data.append('name', formData.name);
      data.append('caterogy', formData.caterogy);
      data.append('price', formData.price);
      data.append('unit', formData.unit);
      data.append('stock', formData.stock);
      data.append('origin', formData.origin);
      data.append('description', formData.description);
      if (formData.imageUrl) {
        data.append('image', formData.imageUrl);
      }

      // Porceso de envio de la imagen al backend 
      const response = await fetch('http://localhost:8000/api/productos', {
        method: 'POST',
        body: data
      });
      if (response.ok) {
        alert('Producto registrado con éxito');
        setFormData({
          name: '',
          caterogy: '',
          price: '',
          unit: '',
          imageUrl: null,
          stock: '',
          origin: '',
          description: ''
        });
      } else {
        alert('Error al registrar el producto');
      }
    } catch (error) {
      alert('Error de red al registrar el producto');
    } finally {
      setIsSubmitting(false);
    }
  };
  const departamentos = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar", "Boyacá", "Caldas",
    "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca",
    "Guainía", "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta", "Nariño",
    "Norte de Santander", "Putumayo", "Quindío", "Risaralda", "San Andrés y Providencia",
    "Santander", "Sucre", "Tolima", "Valle del Cauca", "Vaupés", "Vichada"
  ];
  return (
    <div className="container mt-5">
      <div className="row">
        {/* Columna del formulario */}
        <div className="col-md-8 col-lg-6" style={{ marginLeft: '-20px' }}>
          <div className="card shadow-lg border-3">
            <div className="card-body p-4">
              <div className="d-flex align-items-center justify-content-center mb-4">
                <h2 className="fw-bold text-success mb-0 text-center" style={{ fontSize: '2em' }}>
                  Registra tu producto en <span style={{ display: 'inline-flex', alignItems: 'center' }}>AgroWeb <img src="/src/assets/icon.png" alt="Logo AgroWeb" className="img-fluid ms-2" style={{ width: '35px', height: '35px', verticalAlign: 'middle' }} /></span>
                </h2>
              </div>
              <form onSubmit={handleSubmit} autoComplete="off">
                <div className="row">
                  <div className="mb-3 col-md-6">
                    <label className="form-label">Nombre del producto</label>
                    <input type="text" className="form-control" name="name" value={formData.name} onChange={handleChange} required />
                  </div>
                  <div className="mb-3 col-md-6">
                    <label className="form-label">Categoría</label>
                    <input type="text" className="form-control" name="caterogy" value={formData.caterogy} onChange={handleChange} required />
                  </div>
                </div>
                <div className="row">
                  <div className="mb-3 col-md-6">
                    <label className="form-label">Precio</label>
                    <input type="number" className="form-control" name="price" value={formData.price} onChange={handleChange} required min="0" step="0.01" />
                  </div>
                  <div className="mb-3 col-md-6">
                    <label className="form-label">Unidad de venta (ej: libra, kilo, etc)</label>
                    <input type="number" className="form-control" name="unit" value={formData.unit} onChange={handleChange} required min="1" />
                  </div>
                </div>
                <div className="row">
                  <div className="mb-3 col-md-6">
                    <label className="form-label">Stock o cantidad en inventario</label>
                    <input type="number" className="form-control" name="stock" value={formData.stock} onChange={handleChange} required min="1" />
                  </div>
                  <div className="mb-3 col-md-6">
                    <label className="form-label">Origen del producto</label>
                    <select
                      className="form-select"
                      name="origin"
                      value={formData.origin}
                      onChange={handleChange}
                      required
                    >
                      <option value="">Seleccione un departamento</option>
                      {departamentos.map(dep => (
                        <option key={dep} value={dep}>{dep}</option>
                      ))}
                    </select>
                  </div>
                </div>
                {/* Origen y Descripción fuera de la grilla */}
                <div className="mb-3">
                    <label className="form-label">Imagen del producto</label>
                    <input type="file" className="form-control" name="imageUrl" accept="image/*" onChange={handleChange} />
                  </div>
                <div className="mb-3">
                  <label className="form-label">Descripción del producto</label>
                  <textarea className="form-control" name="description" value={formData.description} onChange={handleChange} required />
                </div>
                <div className="d-grid gap-2">
                  <button type="submit" className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition">
                    {isSubmitting ? 'Registrando...' : 'Registrar Producto'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
        {/* Columna de la imagen */}
     <div className="col-md-4 col-lg-6 d-flex align-items-center justify-content-center p-0" style={{ height: '100vh' }}>
  <img
    src={RegisProductImg}
    alt="Productos"
    className="img-fluid w-88 h-80"
    style={{
      objectFit: 'cover',
      marginRight: '-100px',
      marginTop: '-135px',
    }}
  />
</div>

      </div>
    </div>
  );
};


export default RegistrationProducts;
