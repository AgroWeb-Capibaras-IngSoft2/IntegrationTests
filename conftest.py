"""
Configuración global para pruebas de integración AgroWeb
Fixtures compartidas y configuración de pytest
"""

import pytest
import requests
import time
import os
from datetime import datetime
from typing import Dict, Any, Generator
import logging

# Configurar logging para pruebas
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración global
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))

# Datos de prueba compartidos
SAMPLE_PRODUCTS = [
    {
        "productId": "TEST_001",
        "name": "Papa Criolla Test",
        "category": "Tubérculos",
        "price": 2500.0,
        "stock": 100,
        "description": "Papa criolla fresca para pruebas de integración",
        "imageUrl": "http://localhost:5000/static/catalog/papa_sabanera.jpg",
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": True
    },
    {
        "productId": "TEST_002", 
        "name": "Tomate Chonto Test",
        "category": "Verduras",
        "price": 3200.0,
        "stock": 50,
        "description": "Tomate chonto orgánico para testing",
        "imageUrl": "http://localhost:5000/static/catalog/tomate.jpg",
        "isOrganic": True,
        "isBestSeller": True,
        "freeShipping": False
    }
]

@pytest.fixture(scope="session")
def api_base_url():
    """URL base de la API para todas las pruebas"""
    return API_BASE_URL

@pytest.fixture(scope="session") 
def api_client():
    """Cliente HTTP configurado para pruebas"""
    session = requests.Session()
    session.timeout = API_TIMEOUT
    return session

@pytest.fixture(scope="session")
def api_health_check(api_client, api_base_url):
    """Verificar que la API esté disponible antes de ejecutar pruebas"""
    logger.info("🔍 Verificando disponibilidad de la API...")
    
    for attempt in range(MAX_RETRIES):
        try:
            response = api_client.get(f"{api_base_url}/health")
            if response.status_code == 200:
                logger.info("✅ API disponible y saludable")
                return True
            else:
                logger.warning(f"⚠️ API responde con código {response.status_code}")
        except requests.exceptions.ConnectionError:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"🔄 Intento {attempt + 1} fallido, reintentando en 5 segundos...")
                time.sleep(5)
            else:
                logger.error("❌ No se puede conectar a la API después de múltiples intentos")
                pytest.skip("API no disponible para pruebas")

@pytest.fixture(scope="function")
def clean_test_products(api_client, api_base_url):
    """Limpiar productos de prueba antes y después de cada test"""
    def cleanup():
        """Eliminar productos de prueba si existen"""
        for product in SAMPLE_PRODUCTS:
            try:
                # Intentar obtener el producto
                response = api_client.get(f"{api_base_url}/products/{product['productId']}")
                if response.status_code == 200:
                    logger.info(f"🧹 Producto de prueba {product['productId']} encontrado (limpieza necesaria)")
                    # Nota: Aquí se implementaría DELETE si existiera en la API
            except:
                pass  # Ignorar errores en limpieza
    
    # Limpiar antes del test
    cleanup()
    yield
    # Limpiar después del test
    cleanup()

@pytest.fixture(scope="function")
def sample_product_data():
    """Datos de producto válido para pruebas"""
    return SAMPLE_PRODUCTS[0].copy()

@pytest.fixture(scope="function") 
def multiple_test_products():
    """Múltiples productos para pruebas de listas"""
    return [product.copy() for product in SAMPLE_PRODUCTS]

@pytest.fixture(scope="session")
def test_metrics():
    """Recolector de métricas de pruebas"""
    metrics = {
        "start_time": datetime.now(),
        "requests_made": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "endpoints_tested": set(),
        "response_times": [],
        "error_codes": {}
    }
    return metrics

@pytest.fixture(autouse=True)
def collect_request_metrics(test_metrics):
    """Recolectar métricas automáticamente en cada prueba"""
    yield
    # Las métricas se recolectan en los tests individuales

@pytest.fixture(scope="session")
def test_report_data():
    """Datos para generar reporte PDF al final"""
    return {
        "university": "Universidad Nacional de Colombia",
        "faculty": "Facultad de Ingeniería", 
        "course": "Ingeniería de Software II",
        "project": "AgroWeb - Gestión de Productos",
        "team": "Capibaras Team",
        "test_date": datetime.now(),
        "results": []
    }

def pytest_configure(config):
    """Configuración ejecutada al inicio de pytest"""
    # Crear directorio de reportes si no existe
    os.makedirs("reports", exist_ok=True)
    
    # Log de inicio
    logger.info("🧪 Iniciando Suite de Pruebas de Integración AgroWeb")
    logger.info(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🎯 API Base URL: {API_BASE_URL}")

def pytest_sessionstart(session):
    """Ejecutado al inicio de la sesión de pruebas"""
    logger.info("🚀 Sesión de pruebas iniciada")

def pytest_sessionfinish(session, exitstatus):
    """Ejecutado al final de la sesión de pruebas"""
    logger.info(f"🏁 Sesión de pruebas finalizada con código: {exitstatus}")
    
    # Generar reporte PDF automáticamente
    try:
        from reporting.pdf_generator import generate_integration_report
        generate_integration_report()
        logger.info("📄 Reporte PDF generado exitosamente")
    except ImportError:
        logger.warning("⚠️ No se pudo generar reporte PDF (módulo no disponible)")
    except Exception as e:
        logger.error(f"❌ Error generando reporte PDF: {str(e)}")

def pytest_runtest_setup(item):
    """Configuración antes de cada test individual"""
    logger.info(f"🧪 Ejecutando: {item.name}")

def pytest_runtest_teardown(item):
    """Limpieza después de cada test individual"""
    logger.info(f"✅ Completado: {item.name}")

# Marcadores personalizados para pruebas
pytest_plugins = []
