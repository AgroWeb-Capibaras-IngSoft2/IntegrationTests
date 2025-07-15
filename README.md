# 🧪 AgroWeb - Suite de Pruebas de Integración Centralizada

## 📋 Descripción

Suite completa de pruebas de integración para todos los microservicios de AgroWeb. Proporciona un marco unificado para pruebas end-to-end, casos de éxito y error, y generación automática de reportes profesionales.

## 🎯 Objetivos

- **Pruebas Unificadas**: Centralizar todas las pruebas de integración en un repositorio único
- **Pruebas Multi-Servicio**: Soportar pruebas para Productos, Usuarios y otros servicios
- **Casos Completos**: Validar respuestas correctas y manejo de errores
- **Simulación Realista**: Recrear escenarios reales de uso del sistema
- **Reportes Profesionales**: Generar PDFs formales con métricas, gráficos y resultados

## 🏗️ Estructura del Proyecto

```
IntegrationTests/
├── conftest.py                         # Fixtures y configuración global
├── pytest.ini                          # Configuración global de pytest
├── requirements.txt                    # Dependencias consolidadas
├── setup.py                            # Configuración del paquete
├── README.md                           # Documentación principal
├── CHANGELOG.md                        # Historial de cambios
│
├── config/
│   ├── .env.example                    # Plantilla de variables de entorno
│   ├── productos/                      # Configuración específica del servicio de productos
│   │   ├── __init__.py
│   │   └── test_config.py
│   ├── usuarios/                       # Configuración específica del servicio de usuarios (futuro)
│   └── university_assets/              # Logos y assets de la universidad
│
├── tests/
│   ├── productos/                      # Pruebas del servicio de gestión de productos
│   │   ├── __init__.py
│   │   ├── conftest.py                 # Fixtures específicas de productos
│   │   ├── test_api_integration.py     # Pruebas de integración de API
│   │   ├── test_product_lifecycle.py   # Pruebas de ciclo de vida completo
│   │   ├── test_error_scenarios.py     # Pruebas de manejo de errores
│   │   └── test_performance.py         # Pruebas de rendimiento y carga
│   ├── usuarios/                       # Pruebas del servicio de usuarios (futuro)
│   └── integration/                    # Pruebas cross-service (futuro)
│
├── utils/
│   ├── productos/                      # Utilidades específicas de productos
│   │   ├── __init__.py
│   │   ├── api_client.py               # Cliente HTTP para API de productos
│   │   ├── test_data.py                # Generadores de datos de prueba
│   │   └── validators.py               # Validadores de respuesta
│   ├── usuarios/                       # Utilidades específicas de usuarios (futuro)
│   └── shared/                         # Utilidades compartidas entre servicios
│
├── reporting/                          # Sistema de reportes
│   ├── pdf_generator.py                # Generador de reportes PDF
│   ├── metrics_collector.py            # Recolector de métricas
│   └── templates/                      # Plantillas de reportes
│
└── reports/                           # Reportes generados
    └── [timestamp]/                   # Reportes organizados por fecha
```

## 🚀 Instalación y Configuración

### 1. Prerrequisitos
- Python 3.8 o superior
- Servicios AgroWeb ejecutándose (Productos, Usuarios)

### 2. Instalar Dependencias
```bash
# Navegar al directorio de pruebas
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests"

# Instalar dependencias (método recomendado)
pip install -r requirements.txt

# O usando setup.py
python setup.py install

# Desde cualquier ubicación:
pip install -r "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\requirements.txt"
```

### 3. Configurar Variables de Entorno
```bash
# Copiar plantilla de configuración
copy config\.env.example .env

# Editar configuración según necesidades
# Variables principales:
# - API_BASE_URL_PRODUCTOS=http://localhost:5000
# - API_BASE_URL_USUARIOS=http://localhost:5001
# - API_TIMEOUT=30
```

### 4. Verificar Servicios
```bash
# Verificar servicio de productos
curl http://localhost:5000/health

# Verificar servicio de usuarios
curl http://localhost:5001/health
```

## 🧪 Ejecución de Pruebas

### Ruta Completa del Proyecto
```bash
# Navegar al directorio de pruebas de integración
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests"

# Verificar ubicación actual
pwd
```

### Ejecutar Suite Completa
```bash
# Desde el directorio IntegrationTests:
# Todas las pruebas con reporte HTML
python -m pytest --html=reports/integration_report.html --self-contained-html

# Con reporte JSON adicional
python -m pytest --html=reports/integration_report.html --json-report --json-report-file=reports/test_results.json

# Desde cualquier ubicación (ruta absoluta):
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests" && python -m pytest --html=reports/integration_report.html --self-contained-html
```

### Ejecutar Pruebas por Servicio
```bash
# Desde IntegrationTests/
# Solo pruebas del servicio de productos
python -m pytest tests/productos/ -v

# Solo pruebas del servicio de usuarios
python -m pytest tests/usuarios/ -v

# Con marcadores específicos
python -m pytest -m "productos and api" -v
python -m pytest -m "error_handling" -v

# Desde cualquier ubicación (rutas absolutas):
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests"
python -m pytest "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\tests\productos" -v
python -m pytest "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\tests\usuarios" -v
```

### Ejecutar Pruebas Específicas
```bash
# Desde IntegrationTests/
# Pruebas de integración de API
python -m pytest tests/productos/test_api_integration.py -v

# Pruebas de manejo de errores
python -m pytest tests/productos/test_error_scenarios.py -v

# Filtrar por nombre de prueba
python -m pytest -k "test_create_product" -v

# Pruebas de rendimiento (más lentas)
python -m pytest tests/productos/test_performance.py -v -s

# Desde cualquier ubicación con rutas absolutas:
python -m pytest "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\tests\productos\test_api_integration.py" -v
python -m pytest "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\tests\productos\test_error_scenarios.py" -v

# Ejecutar desde directorio del proyecto completo:
cd "d:\UN\2025-1\Ingesoft 2\Proyecto"
python -m pytest IntegrationTests/tests/productos/test_api_integration.py -v
```

### Generar Reportes PDF
```bash
# Desde IntegrationTests/ después de ejecutar las pruebas
python reporting/pdf_generator.py

# Con ruta absoluta desde cualquier ubicación
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests"
python reporting/pdf_generator.py

# O directamente:
python "d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\reporting\pdf_generator.py"

# El reporte se guardará en: d:\UN\2025-1\Ingesoft 2\Proyecto\IntegrationTests\reports\[timestamp]\
```

## 📊 Tipos de Pruebas Implementadas

### 1. **Pruebas de API REST** (`test_api_integration.py`)
- ✅ Health check endpoints
- ✅ Operaciones CRUD completas
- ✅ Validación de respuestas HTTP
- ✅ Consistencia de datos
- ✅ Métricas de observabilidad
- ✅ Pruebas concurrentes

### 2. **Pruebas de Ciclo de Vida** (`test_product_lifecycle.py`)
- ✅ Flujos end-to-end completos
- ✅ Múltiples categorías de productos
- ✅ Persistencia entre operaciones
- ✅ Simulación de sesiones reales
- ✅ Validación de integridad de datos

### 3. **Pruebas de Manejo de Errores** (`test_error_scenarios.py`)
- ❌ Datos inválidos (400 Bad Request)
- ❌ Content-Type incorrecto (415)
- ❌ Recursos inexistentes (404)
- ❌ Endpoints no disponibles (404)
- ❌ Valores negativos y campos faltantes
- ❌ Estabilidad después de errores

### 4. **Pruebas de Rendimiento** (`test_performance.py`)
- ⚡ Umbrales de tiempo de respuesta
- ⚡ Operaciones concurrentes
- ⚡ Pruebas de carga
- ⚡ Análisis de throughput
- ⚡ Percentiles de rendimiento

## 📄 Reportes y Métricas

### Reportes HTML
- Resultados detallados por prueba
- Gráficos de tiempo de ejecución
- Logs de fallos y errores
- Estadísticas de cobertura

### Reportes PDF Profesionales
- Portada con información universitaria
- Resumen ejecutivo con métricas clave
- Análisis detallado por servicio
- Gráficos de rendimiento
- Recomendaciones basadas en resultados

### Métricas JSON
- Datos estructurados para análisis
- Integración con sistemas de monitoreo
- Tendencias históricas
- Métricas de performance

## 🔧 Configuración Avanzada

### Marcadores de Pruebas
```bash
# Marcadores disponibles:
pytest --markers

# Ejemplos de uso:
python -m pytest -m "smoke"              # Pruebas básicas
python -m pytest -m "integration"        # Pruebas de integración
python -m pytest -m "performance"        # Pruebas de rendimiento
python -m pytest -m "productos"          # Específicas de productos
python -m pytest -m "not slow"           # Excluir pruebas lentas
```

### Variables de Entorno
```bash
# Configuración de API
export API_BASE_URL_PRODUCTOS="http://localhost:5000"
export API_BASE_URL_USUARIOS="http://localhost:5001"
export API_TIMEOUT="30"

# Configuración de pruebas
export MAX_RETRY_ATTEMPTS="3"
export TEST_ENV="integration"
export PYTEST_RUNNING="true"
```

### Configuración de Timeouts
```bash
# Timeout por prueba individual
python -m pytest --timeout=300

# Solo para pruebas específicas
python -m pytest tests/productos/test_performance.py --timeout=600
```

## 🔄 Agregar Nuevos Servicios

### 1. Crear Estructura para Nuevo Servicio (ej: usuarios)
```
tests/usuarios/
├── __init__.py
├── conftest.py                # Fixtures específicas
├── test_user_api.py          # Pruebas de API
├── test_auth.py              # Pruebas de autenticación
└── test_user_lifecycle.py    # Pruebas end-to-end

utils/usuarios/
├── __init__.py
├── api_client.py             # Cliente HTTP
├── auth_client.py            # Cliente de autenticación
├── test_data.py              # Datos de prueba
└── validators.py             # Validadores

config/usuarios/
├── __init__.py
└── test_config.py            # Configuración específica
```

### 2. Actualizar Configuración Global
```ini
# En pytest.ini, agregar marcador:
markers =
    usuarios: Pruebas específicas del servicio de usuarios
```

### 3. Implementar Patrón Consistente
- Seguir la estructura de `productos/`
- Usar los mismos patrones de naming
- Implementar fixtures similares
- Mantener estándares de calidad

## 🚀 Integración CI/CD

### Pipeline Básico
```yaml
# Ejemplo para GitHub Actions
steps:
  - name: Install dependencies
    run: pip install -r IntegrationTests/requirements.txt
  
  - name: Run integration tests
    run: |
      cd IntegrationTests
      python -m pytest --html=reports/ci_report.html --json-report
  
  - name: Generate PDF report
    run: python IntegrationTests/reporting/pdf_generator.py
```

### Ejecutión en Paralelo
```bash
# Pruebas en paralelo con pytest-xdist
python -m pytest -n auto

# Por servicio específico
python -m pytest tests/productos/ -n 2
python -m pytest tests/usuarios/ -n 2
```

## 🏆 Características Avanzadas

### 1. **Observabilidad Completa**
- Integración con métricas Prometheus
- Validación de health checks
- Monitoreo de performance en tiempo real

### 2. **Datos de Prueba Realistas**
- Generadores de productos colombianos
- Categorías específicas (Papa Criolla, Tomate Chonto)
- Datos consistentes con el dominio de negocio

### 3. **Validación Exhaustiva**
- Validadores de estructura JSON
- Validadores de lógica de negocio
- Validadores de performance
- Validadores de consistencia cross-endpoint

### 4. **Reportes Universitarios**
- Formato académico profesional
- Logos y branding institucional
- Análisis estadístico detallado
- Cumplimiento de estándares académicos

## 🤝 Contribución

### Estándares de Código
- Seguir PEP 8 para Python
- Documentar todas las funciones
- Incluir docstrings descriptivos
- Mantener cobertura de pruebas

### Agregar Nuevas Pruebas
1. Identificar el servicio objetivo
2. Crear la estructura necesaria
3. Implementar pruebas siguiendo patrones existentes
4. Actualizar documentación
5. Validar con suite completa

## 📞 Soporte

Para dudas sobre:
- **Estructura**: Consultar este README
- **Configuración**: Revisar archivos en `config/`
- **Implementación**: Analizar ejemplos en `tests/productos/`
- **Reportes**: Documentación en `reporting/`

La suite de pruebas está diseñada para ser auto-explicativa y seguir patrones consistentes que faciliten su extensión y mantenimiento.

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias
```bash
# Crear entorno virtual
python -m venv integration_env
integration_env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
# Copiar archivo de configuración
copy config\.env.example .env

# Editar configuración según necesidades
```

### 3. Verificar Servicio Principal
```bash
# Asegurar que el servicio de productos esté ejecutándose
# En directorio principal:
python app.py

# Verificar health check
curl http://localhost:5000/health
```

## 🧪 Ejecución de Pruebas

### Ejecutar Suite Completa
```bash
# Ejecutar todas las pruebas con reporte
pytest --html=reports/integration_report.html --json-report --json-report-file=reports/test_results.json

# Generar reporte PDF
python reporting/pdf_generator.py
```

### Ejecutar Pruebas Específicas
```bash
# Solo pruebas de API
pytest tests/test_api_integration.py -v

# Solo pruebas de casos de error
pytest tests/test_error_scenarios.py -v

# Pruebas con filtros
pytest -k "test_create_product" -v
```

### Pruebas de Carga
```bash
# Ejecutar pruebas de rendimiento
locust -f tests/test_performance.py --host=http://localhost:5000
```

## 📊 Tipos de Pruebas Implementadas

### 1. Pruebas de Integración de API
- ✅ Crear productos (POST /products)
- ✅ Listar productos (GET /products)
- ✅ Obtener producto por ID (GET /products/{id})
- ✅ Filtrar por categoría (GET /products/category/{category})
- ✅ Health check (GET /health)
- ✅ Métricas (GET /metrics)

### 2. Pruebas de Ciclo de Vida Completo
- ✅ Flujo completo: Crear → Listar → Consultar → Validar
- ✅ Integración con base de datos Cassandra
- ✅ Persistencia de datos entre operaciones

### 3. Pruebas de Casos de Error
- ❌ Datos inválidos (400 Bad Request)
- ❌ Productos no encontrados (404 Not Found)
- ❌ Content-Type incorrecto (415 Unsupported Media Type)
- ❌ Errores de servidor (500 Internal Server Error)

### 4. Pruebas de Rendimiento
- 📈 Latencia de respuesta
- 📈 Throughput (peticiones por segundo)
- 📈 Manejo de carga concurrente
- 📈 Métricas de Prometheus

## 📄 Reportes Generados

### Reporte PDF Profesional
- **Header universitario** con logo y datos institucionales
- **Resumen ejecutivo** con métricas clave
- **Resultados detallados** por categoría de prueba
- **Gráficos de rendimiento** (latencia, throughput, errores)
- **Análisis de cobertura** de endpoints
- **Recomendaciones** basadas en resultados

### Métricas Incluidas
- ✅ **Tasa de éxito** por endpoint
- ⏱️ **Latencia promedio** y percentiles
- 📊 **Distribución de códigos de estado HTTP**
- 📈 **Gráficos de rendimiento temporal**
- 🎯 **Cobertura de casos de prueba**

## 🏛️ Información Institucional

**Universidad Nacional de Colombia**  
**Facultad de Ingeniería**  
**Ingeniería de Software II**  
**Proyecto: AgroWeb - Plataforma de Productos Agrícolas**

**Equipo de Desarrollo:** Capibaras Team  
**Fecha de Generación:** [Auto-generada en cada ejecución]

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# API Configuration
API_BASE_URL=http://localhost:5000
API_TIMEOUT=30

# Database
DB_WAIT_TIME=60

# Reporting
REPORT_OUTPUT_DIR=reports
INCLUDE_PERFORMANCE_GRAPHS=true
UNIVERSITY_LOGO_PATH=config/university_assets/logo_unal.png

# Test Configuration
MAX_RETRY_ATTEMPTS=3
CONCURRENT_USERS=10
TEST_DURATION_SECONDS=60
```

## 📚 Casos de Uso Probados

1. **Usuario consulta catálogo de productos**
   - Lista todos los productos disponibles
   - Filtra por categoría específica
   - Verifica formato de respuesta y datos

2. **Usuario busca producto específico**
   - Busca producto por ID válido
   - Maneja producto inexistente
   - Valida estructura de respuesta

3. **Administrador agrega nuevo producto**
   - Crea producto con datos válidos
   - Valida creación exitosa
   - Verifica persistencia en base de datos

4. **Sistema maneja errores gracefully**
   - Datos malformados en requests
   - Endpoints inexistentes
   - Sobrecarga del sistema

## 🎯 Criterios de Aceptación

- ✅ **Tasa de éxito ≥ 95%** para casos de éxito
- ✅ **Latencia promedio ≤ 200ms** para operaciones CRUD
- ✅ **Cobertura de errores 100%** para códigos HTTP esperados
- ✅ **Disponibilidad del sistema ≥ 99%** durante pruebas
- ✅ **Reporte PDF generado** sin errores en cada ejecución

---

*Generado automáticamente por el Suite de Pruebas de Integración AgroWeb*
