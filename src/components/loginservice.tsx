
import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    // Aquí llamarías tu servicio de autenticación, por ejemplo:
    // authService.login({ email, password }).then(...)
    console.log('Login:', { email, password });
  };

  const handleCreateAccount = () => {
    // Navega al formulario de registro
    navigate('/signup');
  };

  return (
    <div className="w-screen h-screen flex items-center justify-center bg-green-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-2xl shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Iniciar Sesión en AgroWeb
        </h2>

        <label className="block mb-4">
          <span className="text-gray-700">Correo electrónico</span>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="tucorreo@ejemplo.com"
          />
        </label>

        <label className="block mb-6">
          <span className="text-gray-700">Contraseña</span>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            className="mt-1 block w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Tu contraseña"
          />
        </label>

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
        >
          Iniciar Sesión
        </button>

        <p className="mt-4 text-center text-gray-600">
          ¿No tienes cuenta?{' '}
          <button
            type="button"
            onClick={handleCreateAccount}
            className="text-green-600 hover:underline"
          >
            Crear cuenta
          </button>
        </p>
      </form>
    </div>
  );
}
