import React from 'react';

import { useNavigate } from 'react-router-dom';

import { Icon } from '@iconify/react';

interface NavbarProps {
  userName: string | null;
}

const Navbar: React.FC<NavbarProps> = ({ userName }) => {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = React.useState(false);

  // Cierra el menú si se hace click fuera
  React.useEffect(() => {
    if (!menuOpen) return;
    const handleClick = (e: MouseEvent) => {
      const dropdown = document.getElementById('user-dropdown-menu');
      if (dropdown && !dropdown.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [menuOpen]);


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
              onClick={() => navigate('/cart')}
            />
          </button>
          {userName ? (
            
            <div className="relative hidden md:flex items-center gap-2">
              <button
                className="flex items-center p-2 rounded-full hover:bg-gray-100 transition-colors focus:outline-none"
                onClick={() => setMenuOpen((v) => !v)}
                aria-haspopup="true"
                aria-expanded={menuOpen}
              >
                <Icon icon="lucide:user" className="text-green-600 text-xl mr-1" />
                <span className="text-green-600 font-semibold">{userName}</span>
                <Icon icon="lucide:chevron-down" className="ml-1 text-green-600 text-base" />
              </button>
              {/* Dropdown menu */}
              {menuOpen && (
                <div
                  id="user-dropdown-menu"
                  className="absolute left-1/2 -translate-x-1/2 top-10 mt-2 w-52 bg-white border border-gray-100 rounded-2xl shadow-2xl z-50 p-2"
                >
                  <button
                    className="flex items-center gap-2 w-full text-left px-4 py-2 text-base font-medium text-green-800 bg-gradient-to-r from-green-100 to-green-50 rounded-xl shadow-sm hover:from-green-200 hover:to-green-100 hover:shadow-md transition-all duration-200 mb-2"
                    onClick={() => {
                      navigate('/registrar-producto');
                      setMenuOpen(false);
                    }}
                  >
                    <Icon icon="lucide:plus-circle" className="text-green-500 text-lg" />
                    Registrar productos
                  </button>
                  <button
                    className="flex items-center gap-2 w-full text-left px-4 py-2 text-base font-medium text-green-800 bg-gradient-to-r from-green-100 to-green-50 rounded-xl shadow-sm hover:from-green-200 hover:to-green-100 hover:shadow-md transition-all duration-200 mt-2"
                    onClick={() => {
                      navigate('/dashboard');
                      setMenuOpen(false);
                    }}
                  >
                    <Icon icon="lucide:bar-chart-3" className="text-green-500 text-lg" />
                    Dashboard de estadísticas
                  </button>
                  <button
                    className="flex items-center gap-2 w-full text-left px-4 py-2 text-base font-medium text-green-800 bg-gradient-to-r from-green-100 to-green-50 rounded-xl shadow-sm hover:from-green-200 hover:to-green-100 hover:shadow-md transition-all duration-200 mt-2"
                    onClick={() => {
                      navigate('/')
                      // logica para cerrar sesión
                    
                    }}
                    >
                    <Icon icon="lucide:log-out" className="text-green-500 text-lg" />
                    Cerrar sesión
                    </button>
                </div>
              )}
            </div>

          ) : (
            <button
              className="hidden md:block px-4 py-2 bg-green-100 text-green-600 rounded-md hover:bg-green-200 transition-colors"
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

