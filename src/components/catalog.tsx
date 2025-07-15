import React, { useState, useEffect } from 'react';

import { ChevronRight } from 'lucide-react';

import { Icon } from '@iconify/react';

import { CategoryFilter } from './category-filter';
import { ProductCard } from './product-card';

import { useNavigate } from 'react-router-dom';

// 1. Import fetchProducts and Product type
import { fetchProducts } from '../data/product';
import { Product } from '../types/product';

export default function Catalog() {
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [currentPage, setCurrentPage] = useState(1);
  const [isSortOpen, setIsSortOpen] = useState(false);
  const [sortOption, setSortOption] = useState("popular");

  // 2. Add products, loading, error state
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  const itemsPerPage = 8;

  const userName = localStorage.getItem('userName');
  const [showUserMenu, setShowUserMenu] = useState(false);

  // 3. Fetch products from backend
  useEffect(() => {
    setLoading(true);
    fetchProducts()
      .then(data => {
        setProducts(data);
        setError(null);
        setLoading(false);
      })
      .catch(() => {
        setError("No se pudieron cargar los productos. Intenta nuevamente más tarde.");
        setLoading(false);
      });
  }, []);

  // 4. Remove static products array usage
  // 5. Filtering and sorting logic
  let filteredProducts = products.filter((product) => {
    const matchesCategory =
      selectedCategory === "all" || product.category === selectedCategory;
    const matchesSearch = product.name
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  // Optional: Sorting logic
  if (sortOption === "price-low") {
    filteredProducts = [...filteredProducts].sort((a, b) => a.price - b.price);
  } else if (sortOption === "price-high") {
    filteredProducts = [...filteredProducts].sort((a, b) => b.price - a.price);
  } else if (sortOption === "name") {
    filteredProducts = [...filteredProducts].sort((a, b) =>
      a.name.localeCompare(b.name)
    );
  }
  // "popular" can be left as default order

  const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
  const currentProducts = filteredProducts.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  React.useEffect(() => {
    setCurrentPage(1);
  }, [selectedCategory, searchQuery]);

  // Función para cambiar página
  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  // 6. Loading and error states
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <span className="text-lg text-gray-500">Cargando productos...</span>
      </div>
    );
  }
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <span className="text-lg text-red-500">Error: {error}</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 shadow-sm bg-opacity-60 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <Icon
              icon="lucide:sprout"
              className="text-green-600 text-2xl mr-2"
            />
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
              <div className="relative hidden md:block">
                <button
                  className="text-green-600 underline font-semibold px-4 py-2 rounded-md bg-white border border-green-200 hover:bg-green-50 transition-colors flex items-center gap-2"
                  onClick={() => setShowUserMenu((prev) => !prev)}
                  type="button"
                >
                  <Icon icon="lucide:user" className="text-base mr-1" />
                  {userName}
                  <Icon icon="lucide:chevron-down" className="text-base" />
                </button>
                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                    <button
                      className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50"
                      onClick={() => { setShowUserMenu(false); navigate('/registrar-producto'); }}
                    >
                      Registrar productos
                    </button>
                    {/* Puedes agregar más opciones aquí si lo deseas */}
                  </div>
                )}
              </div>
            ) : (
              <button className="hidden md:block px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
                onClick={() => navigate('/')}
              >
                Iniciar Sesión
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Banner */}
      <div className="relative w-full h-64 sm:h-80 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-green-600/80 to-green-400/30 z-10" />
        <img
          src="https://i0.wp.com/www.yesmagazine.org/wp-content/uploads/imports/306009e1b96645c98f6e9253a39cc136.jpg?resize=1950%2C1016&quality=90&ssl=1"
          alt="Farm landscape"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 z-20 flex flex-col justify-center items-center text-white p-4">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-center mb-4">
            Productos del campo a tu mesa
          </h1>
          <p className="text-lg sm:text-xl text-center max-w-2xl">
            Directamente de nuestros campos a tu mesa. Orgánico, sostenible y
            cultivado localmente.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-grow container mx-auto px-4 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <CategoryFilter
              selectedCategory={selectedCategory}
              onSelectCategory={setSelectedCategory}
            />

            {/* Sort Dropdown */}
            <div className="relative">
              <button
                onClick={() => setIsSortOpen(!isSortOpen)}
                className="hs-dropdown-toggle py-3 px-4 inline-flex items-center gap-2 text-sm font-medium rounded-lg border bg-white text-gray-800 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors shadow-sm border-gray-200 dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700"
              >
                Ordenar por
                <Icon
                  icon="lucide:chevron-down"
                  className="text-sm transform transition-transform duration-200 ${isSortOpen ? 'rotate-180"
                />
              </button>

              {isSortOpen && (
                <div className="absolute z-10 mt-1 w-48 bg-white border border-gray-200 rounded-md shadow-lg">
                  <button
                    className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50"
                    onClick={() => {
                      setSortOption("price-low");
                      setIsSortOpen(false);
                    }}
                  >
                    Precio: Menor a Mayor
                  </button>
                  <button
                    className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50"
                    onClick={() => {
                      setSortOption("price-high");
                      setIsSortOpen(false);
                    }}
                  >
                    Precio: Mayor a Menor
                  </button>
                  <button
                    className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50"
                    onClick={() => {
                      setSortOption("name");
                      setIsSortOpen(false);
                    }}
                  >
                    Nombre
                  </button>
                  <button
                    className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-50"
                    onClick={() => {
                      setSortOption("popular");
                      setIsSortOpen(false);
                    }}
                  >
                    Popularidad
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Search Input */}
          <div className="w-full sm:w-auto max-w-xs ml-auto">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Icon icon="lucide:search" className="text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Buscar Productos..."
                className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:bg-white"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Products Grid */}
        {currentProducts.length > 0 ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {/* 7. Use product.productId as key */}
              {currentProducts.map((product) => (
                <ProductCard key={product.productId} product={product} />
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center mt-10">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  className={`px-3 py-1 rounded-md ${
                    currentPage === 1
                      ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                      : "bg-gray-200 hover:bg-gray-300"
                  }`}
                >
                  <ChevronRight
                    className="w-5 h-5 rotate-180 transform" // Rotación 180° para apuntar a la izquierda
                    aria-hidden="true" // Oculta el icono de lectores de pantalla (usa aria-label)
                  />
                </button>

                {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                  (page) => (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`w-8 h-8 rounded-full ${
                        currentPage === page
                          ? "bg-green-600 text-white"
                          : "bg-gray-200 hover:bg-gray-300"
                      }`}
                    >
                      {page}
                    </button>
                  )
                )}

                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className={`px-3 py-1 rounded-md ${
                    currentPage === totalPages
                      ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                      : "bg-gray-200 hover:bg-gray-300"
                  }`}
                >
                  <ChevronRight className="w-5 h-5" aria-hidden="true" />
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="w-full py-12 bg-white rounded-xl shadow-sm flex flex-col items-center justify-center">
            <Icon
              icon="lucide:search-x"
              className="text-4xl text-gray-400 mb-4"
            />
            <h3 className="text-xl font-medium">
              No hay productos encontrados
            </h3>
            <p className="text-gray-500 mt-2 text-center">
              Intenta ajustar tu búsqueda o filtro para encontrar lo que estás
              buscando.
            </p>
            <button
              className="mt-4 px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
              onClick={() => {
                setSearchQuery("");
                setSelectedCategory("all");
              }}
            >
              Limpiar filtros
            </button>
          </div>
        )}
      </div>

      {/* Farm Benefits */}
      <div className="bg-gray-100 py-12">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-10">
            ¿Por que elegir nuestros productos?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-xl">
              <div className="bg-green-100 p-4 rounded-full w-16 h-16 flex items-center justify-center mb-4 mx-auto">
                <Icon icon="lucide:leaf" className="text-3xl text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-center">
                100% Organico
              </h3>
              <p className="text-gray-500 text-center">
                Todos nuestros productos son cultivados sin pesticidas ni
                fertilizantes artificiales, garantizando la pureza y el sabor.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-xl">
              <div className="bg-green-100 p-4 rounded-full w-16 h-16 flex items-center justify-center mb-4 mx-auto">
                <Icon icon="lucide:truck" className="text-3xl text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-center">
                Entrega Rápida
              </h3>
              <p className="text-gray-500 text-center">
                Ofrecemos entrega rápida y confiable para que disfrutes de tus
                productos frescos sin demoras.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-xl">
              <div className="bg-green-100 p-4 rounded-full w-16 h-16 flex items-center justify-center mb-4 mx-auto">
                <Icon icon="lucide:heart" className="text-3xl text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-center">
                Sostenibilidad
              </h3>
              <p className="text-gray-500 text-center">
                Nos comprometemos con prácticas agrícolas sostenibles para
                proteger el medio ambiente y apoyar a las comunidades locales.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-lg mb-4 flex items-center">
                <Icon icon="lucide:sprout" className="mr-2 text-green-400" />{" "}
                Agroweb
              </h3>
              <p className="text-gray-400">
                Tu tienda de confianza para productos frescos y orgánicos
                directamente del campo. Apoyamos la agricultura local y
                sostenible.
              </p>
            </div>

            <div>
              <h3 className="font-bold text-lg mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Home
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Catalogo
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Acerca de Nosotros
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Contacto
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-lg mb-4">Contactanos</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="flex items-center">
                  <Icon icon="lucide:map-pin" className="mr-2" /> Universidad
                  Nacional de Colombia
                </li>
                <li className="flex items-center">
                  <Icon icon="lucide:phone" className="mr-2" /> (555) 123-4567
                </li>
                <li className="flex items-center">
                  <Icon icon="lucide:mail" className="mr-2" /> Agroweb@unal.com
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-bold text-lg mb-4">Suscríbete</h3>
              <p className="text-gray-400 mb-4">
                Suscríbete para recibir actualizaciones sobre nuevos productos y
                ofertas de temporada.
              </p>
              <div className="flex">
                <input
                  type="email"
                  placeholder="Tu correo electrónico"
                  className="flex-grow px-4 py-2 rounded-l-full bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <button className="px-4 py-2 bg-green-600 rounded-r-full hover:bg-green-700 transition-colors">
                  Suscribirse
                </button>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
            <p>
              © {new Date().getFullYear()} Agroweb. Todos los derechos
              reservados.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
