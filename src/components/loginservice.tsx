// src/components/Login.tsx
import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import bgImage from '../assets/paisaje_login.jpg';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    console.log('Login:', { email, password, remember });
    // aquí tu lógica de login...
  };

  return (
    <div className="h-screen flex overflow-hidden">
      {/* IZQUIERDA: 1/2 ancho en lg, 100% altura */}
      <div className="hidden lg:block lg:w-1/2 h-full">
        <img
          src={bgImage}
          alt="paisaje de login"
          className="w-full h-full object-cover"
        />
      </div>

      {/* DERECHA: 1/2 ancho en lg, scroll si es necesario */}
      <div className="w-full lg:w-1/2 flex items-center justify-center overflow-hidden">
        <div className="flex items-center justify-center py-4">
          <div className="w-full max-w-xl bg-white rounded-lg shadow-lg p-6 mx-4 sm:mx-8">
            <h1 className="text-3xl font-bold text-green-700 mb-4">AgroWeb</h1>
            <h2 className="text-2xl font-semibold mb-8">¡Bienvenido de vuelta!</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email */}
              <div>
                <label className="block text-gray-700 mb-1">
                  Correo electrónico
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Escribe tu correo electrónico"
                />
              </div>

              {/* Contraseña con botón 'ojito' */}
              <div>
                <label className="block text-gray-700 mb-1">Contraseña</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                    className="w-full pr-12 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="Escribe tu contraseña"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(prev => !prev)}
                    className="absolute inset-y-0 right-3 flex items-center text-gray-500 bg-transparent border-none p-0 focus:outline-none focus:ring-0 hover:text-gray-700"
                    tabIndex={-1}
                  >
                    {showPassword ? '🙈' : '👁️'}
                  </button>
                </div>
              </div>

              {/* Recordarme + Olvidaste */}
              <div className="flex items-center justify-between">
                <label className="inline-flex items-center">
                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={e => setRemember(e.target.checked)}
                    className="form-checkbox h-5 w-5 text-green-600"
                  />
                  <span className="ml-2 text-gray-700">Recuérdame</span>
                </label>
                <button
                  type="button"
                  onClick={() => navigate('/forgot-password')}
                  className="text-sm text-green-600 hover:underline focus:outline-none"
                >
                  ¿Olvidaste tu contraseña?
                </button>
              </div>

              {/* Botón Entrar */}
              <button
                type="submit"
                className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition"
              >
                Entrar
              </button>

              {/* Continuar como visitante */}
              <button
                type="button"
                onClick={() => navigate('/catalog')}
                className="w-full border border-green-600 text-green-600 py-3 rounded-lg hover:bg-green-100 transition"
              >
                Continuar como visitante
              </button>
            </form>

            {/* Redes sociales */}
            <div className="mt-6 flex space-x-4">
              <button className="flex-1 flex items-center justify-center py-2 border rounded-lg hover:bg-gray-100 transition">
                Facebook
              </button>
              <button className="flex-1 flex items-center justify-center py-2 border rounded-lg hover:bg-gray-100 transition">
                Google
              </button>
            </div>

            {/* Registro + Términos */}
            <p className="mt-8 text-center text-gray-600">
              ¿No tienes cuenta?{' '}
              <button
                onClick={() => navigate('/signup')}
                className="text-green-600 font-medium hover:underline focus:outline-none"
              >
                Regístrate
              </button>
            </p>
            <p className="mt-2 text-center text-xs text-gray-500">
              Al registrarte estás de acuerdo con los{' '}
              <a href="/terms" className="text-green-600 hover:underline">
                Términos de servicio
              </a>{' '}
              y la{' '}
              <a href="/privacy" className="text-green-600 hover:underline">
                Política de privacidad
              </a>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
