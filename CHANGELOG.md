# CHANGELOG

## [1.1.0] - 2025-06-18
### Changed
- Integración completa con el microservicio de productos: el catálogo ahora consume los productos dinámicamente desde el backend.
- Eliminación de datos estáticos de productos en el frontend.
- Visualización del nombre de usuario autenticado en la barra de navegación (en verde y subrayado), ocultando el botón "Iniciar Sesión" si el usuario está logueado.
- Mejoras en la gestión del estado de autenticación usando `localStorage`.
- Ajuste de la lógica para mostrar mensajes de error claros en login y conexión.
- Mejoras visuales y de usabilidad en el catálogo y formularios.
- Sección de configuración de la API documentada en el README.
- Inclusión de capturas de pantalla en el README.
- Manejo automático de rutas relativas en `imageUrl` para imágenes de productos: el frontend ahora convierte rutas relativas a URLs absolutas usando la variable de entorno del backend.
- Mejora en el manejo del estado `loading` para evitar quedarse en "Cargando productos..." indefinidamente.
- Mensajes de error más claros para carga de productos e imágenes.

## [1.0.1] - 2025-06-16
### Added
- Formulario de registro de usuario con validaciones y hash de contraseña.
- Consumo del microservicio de usuarios para login y registro.
- Navegación SPA entre catálogo, login y registro.
- Estilos responsivos y modernos usando Tailwind CSS y HeroUI.

## [1.0.0] - 2025-06-12
### Added
- Estructura inicial del frontend de AgroWeb con React, TypeScript y Vite.
- Catálogo de productos con filtrado, búsqueda y paginación (usando datos estáticos).
- Primeros componentes visuales y estructura de carpetas.