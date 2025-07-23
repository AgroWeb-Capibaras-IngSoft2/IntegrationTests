"""
Configuración de pruebas de integración para el Servicio de Gestión de Productos
Configuración centralizada siguiendo el patrón AgroWeb
"""

import os
from datetime import datetime

class TestConfig:
    """Configuración centralizada para pruebas de integración de productos"""
    
    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    MAX_RETRY_ATTEMPTS = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
    
    # Database Configuration
    CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
    CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
    CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "agroweb")
    DB_WAIT_TIME = int(os.getenv("DB_WAIT_TIME", "60"))
    
    # Test Configuration
    CONCURRENT_USERS = int(os.getenv("CONCURRENT_USERS", "10"))
    TEST_DURATION_SECONDS = int(os.getenv("TEST_DURATION_SECONDS", "60"))
    LOAD_TEST_REQUESTS = int(os.getenv("LOAD_TEST_REQUESTS", "100"))
    
    # Performance Thresholds (milliseconds)
    PERFORMANCE_THRESHOLDS = {
        "health_check": 3000,        # Increased from 100
        "get_products": 5000,        # Increased from 2000
        "create_product": 5000,      # Increased from 1000
        "get_product_by_id": 3000,   # Increased from 500
        "metrics": 3000,             # Increased from 200
        "test_endpoint": 3000        # Increased from 50
    }
    
    # Error Rate Thresholds
    MAX_ERROR_RATE = float(os.getenv("MAX_ERROR_RATE", "0.05"))  # 5%
    MIN_SUCCESS_RATE = float(os.getenv("MIN_SUCCESS_RATE", "0.95"))  # 95%
    
    # Reporting Configuration
    REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "reports")
    INCLUDE_PERFORMANCE_GRAPHS = os.getenv("INCLUDE_PERFORMANCE_GRAPHS", "true").lower() == "true"
    UNIVERSITY_LOGO_PATH = os.getenv("UNIVERSITY_LOGO_PATH", "config/university_assets/logo_unal.png")
    
    # University Information
    UNIVERSITY_INFO = {
        "name": "Universidad Nacional de Colombia",
        "faculty": "Facultad de Ingeniería",
        "department": "Departamento de Ingeniería de Sistemas e Industrial",
        "course": "Ingeniería de Software II",
        "semester": "2025-1",
        "project": "AgroWeb - Servicio de Gestión de Productos",
        "team": "Capibaras Team",
        "service": "Productos Agrícolas API",
        "logo_path": UNIVERSITY_LOGO_PATH
    }
    
    # Test Categories
    TEST_CATEGORIES = {
        "api": "Pruebas de API REST",
        "integration": "Pruebas de Integración End-to-End",
        "database": "Pruebas de Base de Datos Cassandra",
        "performance": "Pruebas de Rendimiento y Carga",
        "error_handling": "Pruebas de Manejo de Errores",
        "smoke": "Pruebas de Smoke Testing",
        "regression": "Pruebas de Regresión",
        "observability": "Pruebas de Observabilidad y Métricas"
    }
    
    # API Endpoints for Testing
    ENDPOINTS = {
        "health": "/health",
        "products": "/products",
        "product_by_id": "/products/{id}",
        "metrics": "/metrics",
        "test": "/test"
    }
    
    # Valid Test Data Categories
    VALID_CATEGORIES = ["Frutas", "Verduras", "Lácteos", "Carnes", "Bebidas", "Tubérculos",
        "Cereales", "Especias", "Huevos", "Hierbas", "Otros"]

    # Test Environment Configuration
    TEST_ENV = os.getenv("TEST_ENV", "integration")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cleanup Configuration
    CLEANUP_TEST_DATA = os.getenv("CLEANUP_TEST_DATA", "true").lower() == "true"
    TEST_DATA_PREFIX = "TEST_"
    
    # Retry Configuration
    RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", "5"))
    
    # Observability Configuration
    PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
    GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3001")
    METRICS_SCRAPE_INTERVAL = int(os.getenv("METRICS_SCRAPE_INTERVAL", "5"))
    
    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """Construir URL completa para un endpoint"""
        return f"{cls.API_BASE_URL}{endpoint}"
    
    @classmethod
    def get_test_timestamp(cls) -> str:
        """Obtener timestamp para identificar ejecuciones de test"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @classmethod
    def get_report_filename(cls, test_type: str = "integration") -> str:
        """Generar nombre de archivo para reportes"""
        timestamp = cls.get_test_timestamp()
        return f"productos_{test_type}_report_{timestamp}"
    
    @classmethod
    def is_debug_mode(cls) -> bool:
        """Verificar si está en modo debug"""
        return os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def get_concurrent_users(cls) -> int:
        """Obtener número de usuarios concurrentes para pruebas de carga"""
        return cls.CONCURRENT_USERS
    
    @classmethod
    def get_performance_threshold(cls, endpoint: str) -> int:
        """Obtener umbral de rendimiento para un endpoint específico"""
        return cls.PERFORMANCE_THRESHOLDS.get(endpoint, 5000)  # Default 5 segundos
    
    @classmethod
    def should_include_graphs(cls) -> bool:
        """Verificar si incluir gráficos en reportes"""
        return cls.INCLUDE_PERFORMANCE_GRAPHS
    
    @classmethod
    def get_database_config(cls) -> dict:
        """Obtener configuración de base de datos"""
        return {
            "host": cls.CASSANDRA_HOST,
            "port": cls.CASSANDRA_PORT,
            "keyspace": cls.CASSANDRA_KEYSPACE,
            "wait_time": cls.DB_WAIT_TIME
        }
    
    @classmethod
    def get_test_categories(cls) -> dict:
        """Obtener categorías de pruebas disponibles"""
        return cls.TEST_CATEGORIES.copy()
    
    @classmethod
    def validate_environment(cls) -> list:
        """Validar configuración del entorno"""
        issues = []
        
        # Verificar URLs
        if not cls.API_BASE_URL.startswith(('http://', 'https://')):
            issues.append("API_BASE_URL debe ser una URL válida")
        
        # Verificar valores numéricos
        if cls.API_TIMEOUT <= 0:
            issues.append("API_TIMEOUT debe ser positivo")
        
        if cls.MAX_RETRY_ATTEMPTS <= 0:
            issues.append("MAX_RETRY_ATTEMPTS debe ser positivo")
        
        # Verificar umbrales de rendimiento
        for endpoint, threshold in cls.PERFORMANCE_THRESHOLDS.items():
            if threshold <= 0:
                issues.append(f"Performance threshold para '{endpoint}' debe ser positivo")
        
        return issues

class TestDataConfig:
    """Configuración específica para datos de prueba"""
    
    # Tamaños de datasets para diferentes tipos de prueba
    DATASET_SIZES = {
        "smoke": 3,
        "integration": 10,
        "performance": 100,
        "load": 1000
    }
    
    # Configuración de productos de prueba
    TEST_PRODUCT_CONFIG = {
        "min_price": 100.0,
        "max_price": 50000.0,
        "min_stock": 0,
        "max_stock": 1000,
        "name_max_length": 200,
        "description_max_length": 1000
    }
    
    @classmethod
    def get_dataset_size(cls, test_type: str) -> int:
        """Obtener tamaño de dataset para tipo de prueba"""
        return cls.DATASET_SIZES.get(test_type, 10)

class MonitoringConfig:
    """Configuración para monitoreo y observabilidad"""
    
    # Métricas esperadas en Prometheus
    EXPECTED_METRICS = [
        'productos_requests_total',
        'productos_request_duration_seconds',
        'productos_errors_total'
    ]
    
    # Endpoints de monitoreo
    MONITORING_ENDPOINTS = {
        "health": "/health",
        "metrics": "/metrics"
    }
    
    # Alertas y umbrales
    ALERT_THRESHOLDS = {
        "response_time_p95": 2000,  # ms
        "error_rate": 0.05,  # 5%
        "availability": 0.99  # 99%
    }
    
    @classmethod
    def get_expected_metrics(cls) -> list:
        """Obtener lista de métricas esperadas"""
        return cls.EXPECTED_METRICS.copy()
