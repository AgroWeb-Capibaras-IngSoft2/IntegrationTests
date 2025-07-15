import React from 'react';

import { useNavigate } from 'react-router-dom';

import { Icon } from '@iconify/react';

interface NavbarProps {
  userName: string | null;
}

const Navbar: React.FC<NavbarProps> = ({ userName }) => {
  const navigate = useNavigate();

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 shadow-sm bg-opacity-60 backdrop-blur-lg">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center">
          <Icon icon="lucide:sprout" className="text-green-600 text-2xl mr-2" />
          <span className="font-bold text-xl">Agroweb</span>
        </div>

        <div className="hidden md:flex space-x-6">
          <a
            href="#"
            className="text-gray-700 hover:text-gray-900 transition-colors"
          >
            Home
          </a>
          <a
            href="#"
            className="text-green-600 font-medium"
            aria-current="page"
          >
            Catalogo
          </a>
          <a
            href="#"
            className="text-gray-700 hover:text-gray-900 transition-colors"
          >
            Acerca de Nosotros
          </a>
          <a
            href="#"
            className="text-gray-700 hover:text-gray-900 transition-colors"
          >
            Contacto
          </a>
        </div>

        <div className="flex items-center space-x-4">
          <button className="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <Icon
              icon="lucide:shopping-cart"
              className="text-lg text-gray-600"
            />
          </button>
          {userName ? (
            <span className="hidden md:block text-green-600 underline font-semibold">
              {userName}
            </span>
          ) : (
            <button
              className="hidden md:block px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
              onClick={() => navigate("/")}
            >
              Iniciar Sesión
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
