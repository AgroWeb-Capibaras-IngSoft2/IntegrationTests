# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-14

### 🎉 Nueva Versión - Centralización Completa

Esta versión marca la migración completa hacia una suite de pruebas centralizada para todos los microservicios de AgroWeb.

### ✨ Added
- **Estructura Modular por Servicios**: Organización clara con subdirectorios para cada microservicio
- **Soporte Multi-Servicio**: Framework preparado para Productos, Usuarios y servicios futuros
- **Configuración Centralizada**: pytest.ini y conftest.py globales con marcadores específicos por servicio
- **Utilidades Compartidas**: Framework de utilidades reutilizables entre servicios
- **Documentación Unificada**: README completo con toda la información consolidada
- **Reportes Mejorados**: Sistema de reportes que soporta múltiples servicios
- **Variables de Entorno**: Configuración flexible para diferentes entornos

### 🔄 Changed
- **Estructura de Directorios**: Migrado de estructura plana a organización por servicios

### 🐛 Fixed
- **Import Conflicts**: Resueltos conflictos de imports entre utilidades de diferentes servicios
- **Path Issues**: Corregidos problemas de rutas relativas en la nueva estructura
- **Configuration Overlap**: Separadas configuraciones específicas por servicio

#### Nueva Ejecución de Pruebas
```bash
# Antes:
run_tests.bat

# Después:
python -m pytest tests/productos/ -v
python -m pytest -m "productos and api" -v
```

#### Marcadores Mejorados
```ini
# Nuevos marcadores disponibles:
productos: Pruebas específicas del servicio de productos
usuarios: Pruebas específicas del servicio de usuarios
observability: Pruebas de métricas y observabilidad
```

## [1.0.0] - 2025-07-12

### 🎉 Versión Inicial

Primera versión completa de las pruebas de integración para el servicio de productos de AgroWeb.

### ✨ Added
- **Suite Completa de Pruebas**: Implementación inicial con 4 categorías principales
- **Pruebas de API REST**: Validación completa de todos los endpoints
- **Pruebas de Ciclo de Vida**: Flujos end-to-end de productos
- **Pruebas de Manejo de Errores**: Validación exhaustiva de casos de error
- **Pruebas de Rendimiento**: Análisis de performance y carga
- **Generación de Reportes PDF**: Reportes académicos profesionales
- **Datos de Prueba Realistas**: Productos colombianos específicos del dominio
- **Métricas de Observabilidad**: Integración con Prometheus
- **Configuración Cassandra**: Soporte para base de datos NoSQL

### 📊 Categorías de Pruebas

#### Pruebas de Integración de API
- Validación de endpoints de health check
- Operaciones CRUD de productos
- Filtrado por categorías
- Operaciones concurrentes
- Validación de endpoints de métricas

#### Pruebas de Escenarios de Error
- Manejo de datos inválidos (400)
- Campos requeridos faltantes
- Tipos de datos incorrectos
- Valores negativos
- Categorías inválidas
- Recursos inexistentes (404)
- Validación de Content-Type (415)

#### Pruebas de Rendimiento
- Umbrales de tiempo de respuesta
- Simulación de usuarios concurrentes
- Pruebas de carga
- Análisis de throughput
- Estabilidad del sistema bajo carga

#### Pruebas de Ciclo de Vida de Productos
- Flujos completos end-to-end
- Validación de consistencia de datos
- Creación de productos multi-categoría
- Integridad de datos cross-endpoint

### 🛠️ Infraestructura

#### Generación de Datos de Prueba
- Productos agrícolas colombianos
- Categorías válidas (vegetales, frutas, lácteos, hierbas)
- Datos realistas de precios y stock
- Banderas de orgánico y best-seller

#### Framework de Validación
- Validadores de respuesta HTTP
- Validadores de estructura JSON
- Validadores de lógica de negocio
- Validadores de umbrales de rendimiento
- Validadores de métricas Prometheus

#### Sistema de Reportes
- Reportes HTML con pytest-html
- Reportes JSON para automatización
- Reportes PDF con branding universitario
- Gráficos y charts de rendimiento
- Análisis estadístico

### 📈 Métricas y Calidad

#### Cobertura de Pruebas
- ✅ Endpoints de API: 100%
- ✅ Escenarios de error: 15+ casos
- ✅ Umbrales de rendimiento: Definidos
- ✅ Lógica de negocio: Validada

#### Estándares de Calidad
- Cumplimiento con PEP 8
- Docstrings comprehensivos
- Type hints en todo el código
- Patrones de manejo de errores
- Logging y monitoreo

### 🔧 Stack Técnico

#### Dependencias Principales
- pytest 7.4.0+ (framework de testing)
- requests 2.31.0+ (cliente HTTP)
- reportlab 4.0.4+ (generación de PDF)
- matplotlib 3.7.2+ (gráficos)
- cassandra-driver 3.28.0+ (base de datos)

#### Utilidades de Testing
- pytest-html (reportes HTML)
- pytest-cov (análisis de cobertura)
- pytest-xdist (ejecución paralela)
- pytest-benchmark (rendimiento)
- locust (pruebas de carga)

#### Datos y Validación
- jsonschema (validación JSON)
- pydantic (validación de datos)
- faker (generación de datos de prueba)
- prometheus-client (métricas)

### 📝 Documentación
- README comprehensivo
- Guías de configuración y ejecución
- Documentación de endpoints de API
- Descripciones de casos de prueba
- Benchmarks de rendimiento
- Guías de troubleshooting

---

## Notas de Versioning

### Schema de Versiones
- **MAJOR**: Cambios incompatibles en la API de testing
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs y mejoras menores

### Etiquetas de Cambios
- **Added**: Nuevas características
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Características que serán removidas
- **Removed**: Características removidas
- **Fixed**: Correcciones de bugs
- **Security**: Correcciones de seguridad

### Compatibilidad
- **v2.0.0+**: Estructura centralizada, soporte multi-servicio
- **v1.0.0**: Estructura original, solo servicio de productos

Para migrar de v1.0.0 a v2.0.0, seguir la guía de migración en el README principal.
