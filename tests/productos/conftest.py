"""
Configuración específica para pruebas de integración del Servicio de Gestión de Productos
Extiende la configuración global de AgroWeb para el servicio de productos
"""

import pytest
import requests
import time
import os
import logging
from datetime import datetime
from typing import Dict, Any, Generator, List
from cassandra.cluster import Cluster
import sys

# Agregar el directorio padre al path para imports relativos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config.productos.test_config import TestConfig

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

# Datos de prueba para productos
SAMPLE_PRODUCTS = [
    {
        "name": "Papa Criolla Integration Test",
        "category": "vegetables",
        "price": 2500.0,
        "unit": "1kg",
        "imageUrl": "http://localhost:5000/static/catalog/papa_criolla_test.jpg",
        "stock": 100,
        "origin": "Boyacá",
        "description": "Papa criolla fresca para pruebas de integración del sistema",
        "isActive": True,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": True
    },
    {
        "name": "Tomate Chonto Integration Test",
        "category": "vegetables", 
        "price": 3200.0,
        "unit": "500g",
        "imageUrl": "http://localhost:5000/static/catalog/tomate_test.jpg",
        "stock": 50,
        "origin": "Cundinamarca",
        "description": "Tomate chonto orgánico para testing de integración",
        "isActive": True,
        "isOrganic": True,
        "isBestSeller": True,
        "freeShipping": False
    },
    {
        "name": "Mango Tommy Integration Test",
        "category": "fruits",
        "price": 4500.0,
        "unit": "1kg",
        "imageUrl": "http://localhost:5000/static/catalog/mango_test.jpg",
        "stock": 0,  # Para testing de productos sin stock
        "origin": "Tolima",
        "description": "Mango Tommy para pruebas de productos sin stock",
        "isActive": True,
        "isOrganic": False,
        "isBestSeller": True,
        "freeShipping": True
    }
]

@pytest.fixture(scope="session")
def api_base_url():
    """URL base de la API para todas las pruebas"""
    return API_BASE_URL

@pytest.fixture(scope="session")
def api_client():
    """Cliente HTTP configurado para pruebas de integración"""
    session = requests.Session()
    session.timeout = API_TIMEOUT
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'AgroWeb-IntegrationTests/1.0'
    })
    return session

@pytest.fixture(scope="session")
def api_health_check(api_client, api_base_url):
    """Verificar que la API esté disponible antes de ejecutar pruebas"""
    logger.info("🔍 Verificando disponibilidad del Servicio de Gestión de Productos...")
    
    for attempt in range(MAX_RETRIES):
        try:
            response = api_client.get(f"{api_base_url}/health")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ API disponible: {data.get('service', 'productos')} v{data.get('version', '1.0')}")
                return True
            else:
                logger.warning(f"⚠️ API responde con código {response.status_code}")
        except requests.exceptions.ConnectionError:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"🔄 Intento {attempt + 1} fallido, reintentando en 5 segundos...")
                time.sleep(5)
            else:
                logger.error("❌ No se puede conectar a la API después de múltiples intentos")
                pytest.skip("API de Gestión de Productos no disponible para pruebas")
    
    return False

@pytest.fixture(scope="session")
def cassandra_health_check():
    """Verificar conectividad con Cassandra (opcional)"""
    logger.info("🔍 Verificando disponibilidad de Cassandra...")
    
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()
        
        # Verificar que el keyspace agroweb existe
        keyspaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        keyspace_names = [row.keyspace_name for row in keyspaces]
        
        if 'agroweb' in keyspace_names:
            logger.info("✅ Cassandra disponible con keyspace 'agroweb'")
            return True
        else:
            logger.warning("⚠️ Cassandra disponible pero sin keyspace 'agroweb'")
            return False
            
    except Exception as e:
        logger.warning(f"⚠️ Cassandra no disponible: {str(e)}")
        return False
    finally:
        try:
            cluster.shutdown()
        except:
            pass

@pytest.fixture(scope="function")
def test_metrics():
    """Recolector de métricas para cada test"""
    metrics = {
        "start_time": datetime.now(),
        "requests_made": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "response_times": [],
        "endpoints_tested": set(),
        "errors_encountered": []
    }
    
    yield metrics
    
    # Logging final de métricas
    duration = (datetime.now() - metrics["start_time"]).total_seconds()
    logger.info(f"📊 Test completado en {duration:.2f}s")
    logger.info(f"📈 Requests: {metrics['successful_requests']}/{metrics['requests_made']} exitosos")
    
    if metrics["response_times"]:
        avg_response_time = sum(rt[1] for rt in metrics["response_times"]) / len(metrics["response_times"])
        logger.info(f"⏱️ Tiempo de respuesta promedio: {avg_response_time:.2f}ms")

@pytest.fixture(scope="function")
def created_products(api_client, api_base_url):
    """Fixture para crear y limpiar productos de prueba"""
    created_product_ids = []
    
    def create_product(product_data: Dict[str, Any]) -> str:
        """Crear un producto de prueba y registrar su ID"""
        response = api_client.post(f"{api_base_url}/products", json=product_data)
        if response.status_code == 201:
            product = response.json()
            product_id = product.get('productId')
            if product_id:
                created_product_ids.append(product_id)
                logger.info(f"✅ Producto de prueba creado: {product_id}")
                return product_id
        
        logger.error(f"❌ Error creando producto de prueba: {response.status_code}")
        return None
    
    yield create_product
    
    # Cleanup: En una API real con DELETE, aquí limpiaríamos los productos
    # Por ahora solo logging
    if created_product_ids:
        logger.info(f"🧹 Productos de prueba creados: {len(created_product_ids)}")
        for product_id in created_product_ids:
            logger.info(f"   - {product_id}")

@pytest.fixture(scope="session")
def sample_products():
    """Datos de productos de muestra para testing"""
    return SAMPLE_PRODUCTS.copy()

@pytest.fixture(scope="function")
def clean_prometheus_metrics(api_client, api_base_url):
    """Limpiar estado de métricas antes del test (opcional)"""
    # Realizar una request inicial para resetear contadores de métricas
    try:
        api_client.get(f"{api_base_url}/metrics")
        logger.info("📊 Métricas de Prometheus inicializadas")
    except:
        logger.warning("⚠️ No se pudieron inicializar métricas de Prometheus")
    
    yield

def pytest_configure(config):
    """Configuración inicial de pytest"""
    logger.info("🚀 Iniciando suite de pruebas de integración - Servicio de Gestión de Productos")
    logger.info(f"🌐 API Base URL: {API_BASE_URL}")
    logger.info(f"⏰ Timeout: {API_TIMEOUT}s")
    logger.info(f"🔄 Max Retries: {MAX_RETRIES}")

def pytest_sessionfinish(session, exitstatus):
    """Finalizacion de la sesión de pruebas"""
    logger.info("🏁 Suite de pruebas de integración completada")
    logger.info(f"📋 Estado de salida: {exitstatus}")
