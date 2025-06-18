import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import bgImage from '../assets/paisaje_login.jpg';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/users/autenticate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          hashPassword: password
        }),
      });

      const data = await response.json();

      if (response.ok) {
        navigate('/catalog'); // Redirect to catalog after successful login
        // You can store user info/token here if needed
        // navigate('/dashboard'); // Uncomment if you have a dashboard route
      } else {
        setError(data.error || 'Error de autenticación');
      }
    } catch (err) {
      setError('No se pudo conectar con el servidor');
    }
  };

  return (
    <div className="h-screen flex overflow-hidden">
      {/* Left side: image */}
      <div className="hidden lg:block lg:w-2/3 h-full">
        <img
          src={bgImage}
          alt="paisaje de login"
          className="w-full h-full object-cover"
        />
      </div>

      {/* Right side: form */}
      <div className="w-full lg:w-1/3 overflow-auto">
        <div className="min-h-screen flex items-center justify-center p-8">
          <div className="w-full bg-white rounded-lg shadow-lg p-8 mx-4 sm:mx-8">
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

              {/* Password */}
              <div>
                <label className="block text-gray-700 mb-1">
                  Contraseña
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Escribe tu contraseña"
                />
              </div>

              {/* Error message */}
              {error && (
                <div className="text-red-600 text-sm">{error}</div>
              )}

              {/* Remember me and forgot password */}
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
                  className="text-sm text-green-600 hover:underline"
                >
                  Olvidaste tu contraseña?
                </button>
              </div>

              {/* Entrar button */}
              <button
                type="submit"
                className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition"
              >
                Entrar
              </button>
            </form>

            {/* Social login buttons */}
            <div className="mt-6 flex space-x-4">
              <button className="flex-1 flex items-center justify-center py-2 border rounded-lg hover:bg-gray-100 transition">
                Facebook
              </button>
              <button className="flex-1 flex items-center justify-center py-2 border rounded-lg hover:bg-gray-100 transition">
                Google
              </button>
            </div>

            {/* Register and terms */}
            <p className="mt-8 text-center text-gray-600">
              ¿No tienes cuenta?{' '}
              <button
                onClick={() => navigate('/signup')}
                className="text-green-600 font-medium hover:underline"
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