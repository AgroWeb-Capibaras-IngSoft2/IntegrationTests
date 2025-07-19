"""
Configuración de pruebas de integración para el Servicio de Carrito de Compras
Configuración centralizada siguiendo el patrón AgroWeb
"""

import os
from datetime import datetime

class TestConfig:
    """Configuración centralizada para pruebas de integración de carrito"""
    
    # API Configuration
    API_BASE_URL = os.getenv("CART_API_BASE_URL", "http://localhost:5003")
    API_TIMEOUT = int(os.getenv("CART_API_TIMEOUT", "30"))
    MAX_RETRY_ATTEMPTS = int(os.getenv("CART_MAX_RETRY_ATTEMPTS", "3"))
    
    # Performance Thresholds (milliseconds)
    PERFORMANCE_THRESHOLDS = {
        "create_carrito": int(os.getenv("CREATE_CART_THRESHOLD", "300")),
        "add_product": int(os.getenv("ADD_PRODUCT_THRESHOLD", "400")),
        "change_quantity": int(os.getenv("CHANGE_QUANTITY_THRESHOLD", "350")),
        "delete_product": int(os.getenv("DELETE_PRODUCT_THRESHOLD", "300")),
        "get_carrito": int(os.getenv("GET_CART_THRESHOLD", "200")),
        "vaciar_carrito": int(os.getenv("VACIAR_CART_THRESHOLD", "500"))
    }
    
    # Test Configuration
    CONCURRENT_USERS = int(os.getenv("CONCURRENT_USERS", "5"))
    TEST_DURATION_SECONDS = int(os.getenv("TEST_DURATION_SECONDS", "30"))
    
    # Error Rate Thresholds
    MAX_ERROR_RATE = float(os.getenv("MAX_ERROR_RATE", "0.05"))  # 5%
    MIN_SUCCESS_RATE = float(os.getenv("MIN_SUCCESS_RATE", "0.95"))  # 95%
    
    # Reporting Configuration
    REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "reports")
    UNIVERSITY_LOGO_PATH = os.getenv("UNIVERSITY_LOGO_PATH", "config/university_assets/logo_unal.png")
    
    # University Information
    UNIVERSITY_INFO = {
        "name": "Universidad Nacional de Colombia",
        "faculty": "Facultad de Ingeniería",
        "department": "Departamento de Ingeniería de Sistemas e Industrial",
        "course": "Ingeniería de Software II",
        "semester": "2025-1",
        "project": "AgroWeb - Servicio de Carrito de Compras",
        "team": "Capibaras Team",
        "service": "Carrito de Compras API",
        "logo_path": UNIVERSITY_LOGO_PATH
    }
    
    # Test Categories
    TEST_CATEGORIES = {
        "api": "Pruebas de API REST",
        "integration": "Pruebas de Integración End-to-End",
        "error_handling": "Pruebas de Manejo de Errores",
        "smoke": "Pruebas de Smoke Testing"
    }
    
    # API Endpoints for Testing
    ENDPOINTS = {
        "create_carrito": "/carrito/create",
        "add_product": "/carrito/addProduct",
        "change_quantity": "/carrito/changeQuantity",
        "delete_product": "/carrito/deleteProduct",
        "vaciar_carrito": "/carrito/vaciar",
        "get_carrito": "/carrito/getCarrito/{id}"
    }
    
    # Test Data Configuration
    TEST_DATA = {
        "valid_users": [
            {"userdocument": "12345678", "doctype": "CC"},
            {"userdocument": "87654321", "doctype": "CC"},
            {"userdocument": "11223344", "doctype": "CC"}
        ],
        "valid_product_ids": ["PROD-577D6765", "PROD-661AA7F9", "PROD-E0B41C01"],
        "valid_quantities": [1, 2, 5, 10],
        "invalid_quantities": [0, -1, -5, 1000000],
        "invalid_doctypes": ["TI", "CE", "INVALID", ""]
    }
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Cleanup Configuration
    CLEANUP_TEST_DATA = os.getenv("CLEANUP_TEST_DATA", "true").lower() == "true"
    
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
        return f"carrito_{test_type}_report_{timestamp}"
    
    @classmethod
    def get_performance_threshold(cls, endpoint: str) -> int:
        """Obtener umbral de rendimiento para un endpoint específico"""
        return cls.PERFORMANCE_THRESHOLDS.get(endpoint, 1000)  # Default 1 segundo
    
    @classmethod
    def get_test_user_data(cls) -> dict:
        """Obtener datos de usuario para testing"""
        return cls.TEST_DATA["valid_users"][0]
    
    @classmethod
    def get_test_product_id(cls) -> str:
        """Obtener ID de producto para testing"""
        return cls.TEST_DATA["valid_product_ids"][0]
    
    @classmethod
    def ensure_report_directory(cls) -> str:
        """Asegurar que el directorio de reportes existe y devolver la ruta"""
        import os
        report_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(report_dir, exist_ok=True)
        return report_dir
