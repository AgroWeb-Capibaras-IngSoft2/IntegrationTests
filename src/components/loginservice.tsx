import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import bgImage from '../assets/paisaje_login.jpg';
import bcrypt from 'bcryptjs';
import { getCarritoIdByUser } from '../services/cartservices';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const usersApiUrl = import.meta.env.VITE_API_USERS_URL;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch(`${usersApiUrl}/users/autenticate/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          hashPassword: password
        }),
      });

      const data = await response.json();
      console.log('data: ',data);

      if (response.ok) {
        // Fetch user data by email to get the username
        const loginData=data;
        try {
          const userResp = await fetch(`${usersApiUrl}/users/getByEmail/${email}`);
          const userData = await userResp.json();
          if (userResp.ok && userData.user && userData.user.username) {
            localStorage.setItem('userName', userData.user.username);
          } else if (userData.user && userData.user.name) {
            localStorage.setItem('userName', userData.user.name);
          } else {
            localStorage.setItem('userName', email);
          }
          //Guardamos el id del carrito
          try{
            console.log('document:',loginData.user.userdocument);
            console.log('doctype:',loginData.user.doctype);
            const carritoId= await getCarritoIdByUser(loginData.user.userdocument,loginData.user.doctype);
            localStorage.setItem('carritoId',carritoId);
          }catch(error){
            console.error('Error obtieniendo carrito:' ,error);
          }
          navigate('/catalog');
        } catch (err) {
          // If fetching user data fails, fallback to email
          localStorage.setItem('userName', email);
          navigate('/catalog');
        }
      } else {
        setError(data.error || 'Error de autenticación');
      }
    } catch (err) {
      setError('No se pudo conectar con el servidor');
    }
  };

  return (
    <div className="h-screen flex overflow-hidden bg-gray-100 dark:bg-gray-900">
      {/* IZQUIERDA: 1/2 ancho en lg, 100% altura */}
      <div className="hidden lg:block lg:w-1/2 h-full">
        <img
          src={bgImage}
          alt="paisaje de login"
          className="w-full h-full object-cover"
        />
      </div>

      {/* DERECHA: 1/2 ancho en lg, centrado y sin scroll */}
      <div className="w-full lg:w-1/2 flex items-center justify-center overflow-hidden">
        <div className="flex items-center justify-center py-4">
          <div className="w-full max-w-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-lg shadow-lg p-6 mx-4 sm:mx-8">
            <h1 className="text-3xl font-bold text-green-700 dark:text-green-400 mb-4">AgroWeb</h1>
            <h2 className="text-2xl font-semibold mb-8">¡Bienvenido de vuelta!</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email */}
              <div>
                <label className="block text-gray-700 dark:text-gray-300 mb-1">
                  Correo electrónico
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  placeholder="Escribe tu correo electrónico"
                />
              </div>

              {/* Contraseña con botón 'ojito' */}
              <div>
                <label className="block text-gray-700 dark:text-gray-300 mb-1">Contraseña</label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    required
                    className="w-full pr-12 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    placeholder="Escribe tu contraseña"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(prev => !prev)}
                    className="absolute inset-y-0 right-3 flex items-center text-gray-500 dark:text-gray-300 bg-transparent border-none p-0 focus:outline-none focus:ring-0 hover:text-gray-700 dark:hover:text-white"
                    tabIndex={-1}
                  >
                    {showPassword ? '🙈' : '👁️'}
                  </button>
                </div>
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
                    className="form-checkbox h-5 w-5 text-green-600 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <span className="ml-2 text-gray-700 dark:text-gray-300">Recuérdame</span>
                </label>
                <button
                  type="button"
                  onClick={() => navigate('/forgot-password')}
                  className="text-sm text-green-600 dark:text-green-400 hover:underline focus:outline-none"
                >
                  ¿Olvidaste tu contraseña?
                </button>
              </div>

              {/* Entrar button */}
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
                className="w-full border border-green-600 text-green-600 py-3 rounded-lg hover:bg-green-100 dark:hover:bg-green-900 transition bg-white"
              >
                Continuar como visitante
              </button>
            </form>

            {/* Social login buttons */}
            <div className="mt-6 flex space-x-4">
              <button className="flex-1 flex items-center justify-center py-2 border rounded-lg bg-white text-black hover:bg-gray-100 transition">
                Facebook
              </button>
              <button className="flex-1 flex items-center justify-center py-2 border rounded-lg bg-white text-black hover:bg-gray-100 transition">
                Google
              </button>
            </div>

            {/* Registro + Términos */}
            <p className="mt-8 text-center text-gray-600 dark:text-gray-400">
              ¿No tienes cuenta?{' '}
              <button
                onClick={() => navigate('/signup')}
                className="text-green-600 font-medium hover:underline focus:outline-none bg-transparent"
              >
                Regístrate
              </button>
            </p>
            <p className="mt-2 text-center text-xs text-gray-500 dark:text-gray-400">
              Al registrarte estás de acuerdo con los{' '}
              <a href="/terms" className="text-green-600 dark:text-green-400 hover:underline">
                Términos de servicio
              </a>{' '}
              y la{' '}
              <a href="/privacy" className="text-green-600 dark:text-green-400 hover:underline">
                Política de privacidad
              </a>.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}