"""
Configuración de fixtures y setup para pruebas de integración del Servicio de Carrito
Configuración centralizada siguiendo el patrón AgroWeb
"""

import pytest
import requests
import logging
import time
from typing import Dict, Any, List

from config.carrito.test_config import TestConfig

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def carrito_api_base_url():
    """URL base de la API de carrito para todas las pruebas"""
    return TestConfig.API_BASE_URL

@pytest.fixture(scope="session")
def carrito_api_client():
    """Cliente HTTP configurado para pruebas de integración de carrito"""
    session = requests.Session()
    session.timeout = TestConfig.API_TIMEOUT
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'AgroWeb-CarritoIntegrationTest/1.0'
    })
    return session

@pytest.fixture(scope="session")
def carrito_api_health_check(carrito_api_client, carrito_api_base_url):
    """Verificar que la API de carrito esté disponible antes de ejecutar pruebas"""
    logger.info("🔍 Verificando disponibilidad del Servicio de Carrito de Compras...")
    
    for attempt in range(TestConfig.MAX_RETRY_ATTEMPTS):
        try:
            # Como no tenemos /health, usamos cualquier endpoint
            response = carrito_api_client.get(f"{carrito_api_base_url}/carrito/getCarrito/test")
            # Si responde (aunque sea 404), el servicio está arriba
            if response.status_code in [200, 404, 400]:
                logger.info(f"✅ API de Carrito disponible en {carrito_api_base_url}")
                return True
            else:
                logger.warning(f"⚠️ API responde con código {response.status_code}")
        except requests.exceptions.ConnectionError:
            if attempt < TestConfig.MAX_RETRY_ATTEMPTS - 1:
                logger.warning(f"🔄 Intento {attempt + 1} fallido, reintentando en 5 segundos...")
                time.sleep(5)
            else:
                logger.error("❌ No se puede conectar a la API de Carrito después de múltiples intentos")
                pytest.skip("API de Carrito no disponible para pruebas")
    
    return False

@pytest.fixture(scope="function")
def carrito_test_metrics():
    """Recolector de métricas para cada test de carrito"""
    metrics = {
        "test_name": "",
        "start_time": time.time(),
        "requests_made": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "response_times": [],
        "endpoints_tested": set(),
        "errors_encountered": [],
        "created_carritos": [],
        "test_duration": 0
    }
    
    yield metrics
    
    # Calcular duración total del test
    metrics["test_duration"] = time.time() - metrics["start_time"]
    
    # Log de métricas finales
    logger.info(f"📊 Test completado en {metrics['test_duration']:.2f}s")
    logger.info(f"📈 Requests: {metrics['requests_made']} total, {metrics['successful_requests']} exitosos")

@pytest.fixture(scope="function")
def created_carritos_cleanup(carrito_api_client, carrito_api_base_url):
    """Fixture para rastrear y limpiar carritos creados durante pruebas"""
    created_carrito_ids = []
    
    def track_carrito(carrito_id: str):
        """Registrar un carrito creado para limpieza posterior"""
        if carrito_id and carrito_id not in created_carrito_ids:
            created_carrito_ids.append(carrito_id)
            logger.info(f"🛒 Carrito registrado para limpieza: {carrito_id}")
    
    yield track_carrito
    
    # Cleanup: Vaciar carritos creados (si es necesario)
    if created_carrito_ids and TestConfig.CLEANUP_TEST_DATA:
        logger.info(f"🧹 Limpiando {len(created_carrito_ids)} carritos de prueba...")
        for carrito_id in created_carrito_ids:
            try:
                # Intentar vaciar el carrito
                cleanup_data = {"id_carrito": carrito_id}
                response = carrito_api_client.delete(
                    f"{carrito_api_base_url}/carrito/vaciar", 
                    json=cleanup_data
                )
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get("Success"):
                        logger.info(f"✅ Carrito {carrito_id} limpiado")
                    else:
                        logger.warning(f"⚠️ No se pudo limpiar carrito {carrito_id}")
                else:
                    logger.warning(f"⚠️ Error HTTP limpiando carrito {carrito_id}: {response.status_code}")
            except:
                logger.warning(f"⚠️ Error limpiando carrito {carrito_id}")

@pytest.fixture(scope="function")
def sample_test_data():
    """Datos de prueba básicos para carritos"""
    return {
        "valid_user": TestConfig.get_test_user_data(),
        "valid_product": {
            "id_carrito": "",  # Se llenará dinámicamente
            "product_id": TestConfig.get_test_product_id(),
            "cantidad": 2
        },
        "invalid_carrito_id": "999999",
        "invalid_product_id": "PROD-INEXISTENTE123",
        "invalid_user": {"userdocument": "12345678", "doctype": "TI"}  # Tipo inválido
    }

def pytest_configure(config):
    """Configuración inicial de pytest para carrito"""
    logger.info("🚀 Iniciando suite de pruebas de integración - Servicio de Carrito de Compras")
    logger.info(f"🌐 API Base URL: {TestConfig.API_BASE_URL}")
    logger.info(f"⏰ Timeout: {TestConfig.API_TIMEOUT}s")
    logger.info(f"🔄 Max Retries: {TestConfig.MAX_RETRY_ATTEMPTS}")

def pytest_sessionfinish(session, exitstatus):
    """Finalización de la sesión de pruebas de carrito"""
    if exitstatus == 0:
        logger.info("✅ Todas las pruebas de carrito completadas exitosamente")
    else:
        logger.error(f"❌ Pruebas de carrito finalizadas con errores (exit code: {exitstatus})")
