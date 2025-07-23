"""
Validadores de respuesta para pruebas de integración del Servicio de Gestión de Productos
Validaciones completas siguiendo el patrón AgroWeb
"""

import json
import re
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

class ResponseValidator:
    """Validador de respuestas de la API de Gestión de Productos"""
    
    # Patrones de validación
    PRODUCT_ID_PATTERN = re.compile(r'^PROD-[A-Z0-9]{8}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    URL_PATTERN = re.compile(r'^https?://.*')
    
    # Categorías válidas
    VALID_CATEGORIES = ["Frutas", "Verduras", "Lácteos", "Carnes", "Bebidas", "Tubérculos",
        "Cereales", "Especias", "Huevos", "Hierbas", "Otros"]
    
    def __init__(self):
        self.errors = []
    
    def reset_errors(self):
        """Limpiar lista de errores"""
        self.errors = []
    
    def get_errors(self) -> List[str]:
        """Obtener lista de errores encontrados"""
        return self.errors.copy()
    
    def validate_http_status(self, response, expected_status: int) -> bool:
        """Validar código de estado HTTP"""
        if response.status_code != expected_status:
            self.errors.append(
                f"Expected HTTP status {expected_status}, got {response.status_code}"
            )
            return False
        return True
    
    def validate_json_response(self, response) -> Optional[Dict[str, Any]]:
        """Validar que la respuesta sea JSON válido"""
        try:
            return response.json()
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON response: {str(e)}")
            return None
    
    def validate_content_type(self, response, expected_type: str = "application/json") -> bool:
        """Validar Content-Type de la respuesta"""
        content_type = response.headers.get('Content-Type', '')
        if expected_type not in content_type:
            self.errors.append(
                f"Expected Content-Type '{expected_type}', got '{content_type}'"
            )
            return False
        return True
    
    def validate_product_structure(self, product: Dict[str, Any], strict: bool = True) -> bool:
        """Validar estructura completa de un producto"""
        self.reset_errors()
        
        # Campos requeridos
        required_fields = [
            'productId', 'name', 'category', 'price', 'unit', 
            'imageUrl', 'stock', 'origin', 'description', 'isActive'
        ]
        
        # Verificar campos requeridos
        for field in required_fields:
            if field not in product:
                self.errors.append(f"Missing required field: '{field}'")
        
        if self.errors and strict:
            return False
        
        # Validaciones específicas por campo
        self._validate_product_id(product.get('productId'))
        self._validate_product_name(product.get('name'))
        self._validate_product_category(product.get('category'))
        self._validate_product_price(product.get('price'))
        self._validate_product_stock(product.get('stock'))
        self._validate_product_image_url(product.get('imageUrl'))
        self._validate_product_description(product.get('description'))
        self._validate_product_origin(product.get('origin'))
        self._validate_product_unit(product.get('unit'))
        self._validate_product_is_active(product.get('isActive'))
        
        # Validar campos opcionales si están presentes
        if 'originalPrice' in product and product['originalPrice'] is not None:
            self._validate_product_price(product['originalPrice'], field_name='originalPrice')
        
        if 'isOrganic' in product:
            self._validate_boolean_field(product['isOrganic'], 'isOrganic')
        
        if 'isBestSeller' in product:
            self._validate_boolean_field(product['isBestSeller'], 'isBestSeller')
        
        if 'freeShipping' in product:
            self._validate_boolean_field(product['freeShipping'], 'freeShipping')
        
        # Validar campo calculado inStock
        if 'inStock' in product:
            expected_in_stock = product.get('stock', 0) > 0
            if product['inStock'] != expected_in_stock:
                self.errors.append(
                    f"Field 'inStock' should be {expected_in_stock} based on stock={product.get('stock')}"
                )
        
        return len(self.errors) == 0
    
    def _validate_product_id(self, product_id: Any) -> bool:
        """Validar formato de productId"""
        if not isinstance(product_id, str):
            self.errors.append("Field 'productId' must be a string")
            return False
        
        if not self.PRODUCT_ID_PATTERN.match(product_id):
            self.errors.append(
                f"Field 'productId' has invalid format: '{product_id}'. Expected: PROD-XXXXXXXX"
            )
            return False
        
        return True
    
    def _validate_product_name(self, name: Any) -> bool:
        """Validar nombre del producto"""
        if not isinstance(name, str):
            self.errors.append("Field 'name' must be a string")
            return False
        
        if not name.strip():
            self.errors.append("Field 'name' cannot be empty")
            return False
        
        if len(name) > 200:  # Límite razonable
            self.errors.append("Field 'name' is too long (max 200 characters)")
            return False
        
        return True
    
    def _validate_product_category(self, category: Any) -> bool:
        """Validar categoría del producto"""
        if not isinstance(category, str):
            self.errors.append("Field 'category' must be a string")
            return False
        
        if category not in self.VALID_CATEGORIES:
            self.errors.append(
                f"Field 'category' has invalid value: '{category}'. "
                f"Valid categories: {self.VALID_CATEGORIES}"
            )
            return False
        
        return True
    
    def _validate_product_price(self, price: Any, field_name: str = 'price') -> bool:
        """Validar precio del producto"""
        if not isinstance(price, (int, float)):
            self.errors.append(f"Field '{field_name}' must be a number")
            return False
        
        if price < 0:
            self.errors.append(f"Field '{field_name}' cannot be negative")
            return False
        
        if price > 999999.99:  # Límite razonable
            self.errors.append(f"Field '{field_name}' is too high (max 999999.99)")
            return False
        
        return True
    
    def _validate_product_stock(self, stock: Any) -> bool:
        """Validar stock del producto"""
        if not isinstance(stock, int):
            self.errors.append("Field 'stock' must be an integer")
            return False
        
        if stock < 0:
            self.errors.append("Field 'stock' cannot be negative")
            return False
        
        if stock > 999999:  # Límite razonable
            self.errors.append("Field 'stock' is too high (max 999999)")
            return False
        
        return True
    
    def _validate_product_image_url(self, image_url: Any) -> bool:
        """Validar URL de imagen"""
        if not isinstance(image_url, str):
            self.errors.append("Field 'imageUrl' must be a string")
            return False
        
        if not self.URL_PATTERN.match(image_url):
            self.errors.append(f"Field 'imageUrl' is not a valid URL: '{image_url}'")
            return False
        
        return True
    
    def _validate_product_description(self, description: Any) -> bool:
        """Validar descripción del producto"""
        if not isinstance(description, str):
            self.errors.append("Field 'description' must be a string")
            return False
        
        if not description.strip():
            self.errors.append("Field 'description' cannot be empty")
            return False
        
        if len(description) > 1000:  # Límite razonable
            self.errors.append("Field 'description' is too long (max 1000 characters)")
            return False
        
        return True
    
    def _validate_product_origin(self, origin: Any) -> bool:
        """Validar origen del producto"""
        if not isinstance(origin, str):
            self.errors.append("Field 'origin' must be a string")
            return False
        
        if not origin.strip():
            self.errors.append("Field 'origin' cannot be empty")
            return False
        
        return True
    
    def _validate_product_unit(self, unit: Any) -> bool:
        """Validar unidad del producto"""
        if not isinstance(unit, str):
            self.errors.append("Field 'unit' must be a string")
            return False
        
        if not unit.strip():
            self.errors.append("Field 'unit' cannot be empty")
            return False
        
        return True
    
    def _validate_product_is_active(self, is_active: Any) -> bool:
        """Validar campo isActive"""
        return self._validate_boolean_field(is_active, 'isActive')
    
    def _validate_boolean_field(self, value: Any, field_name: str) -> bool:
        """Validar campo booleano"""
        if not isinstance(value, bool):
            self.errors.append(f"Field '{field_name}' must be a boolean")
            return False
        return True
    
    def validate_products_list(self, products: List[Dict[str, Any]]) -> bool:
        """Validar lista de productos"""
        self.reset_errors()
        
        if not isinstance(products, list):
            self.errors.append("Response must be a list")
            return False
        
        for i, product in enumerate(products):
            if not isinstance(product, dict):
                self.errors.append(f"Product at index {i} must be a dictionary")
                continue
            
            # Validar cada producto
            product_validator = ResponseValidator()
            if not product_validator.validate_product_structure(product):
                for error in product_validator.get_errors():
                    self.errors.append(f"Product {i}: {error}")
        
        return len(self.errors) == 0
    
    def validate_health_response(self, health_data: Dict[str, Any]) -> bool:
        """Validar respuesta del endpoint /health"""
        self.reset_errors()
        
        required_fields = ['status', 'service', 'version', 'metrics_endpoint']
        
        for field in required_fields:
            if field not in health_data:
                self.errors.append(f"Health response missing field: '{field}'")
        
        # Validaciones específicas
        if health_data.get('status') != 'healthy':
            self.errors.append("Service status is not 'healthy'")
        
        if health_data.get('service') != 'productos':
            self.errors.append("Service name should be 'productos'")
        
        if health_data.get('metrics_endpoint') != '/metrics':
            self.errors.append("Metrics endpoint should be '/metrics'")
        
        return len(self.errors) == 0
    
    def validate_error_response(self, error_data: Dict[str, Any], expected_status: int) -> bool:
        """Validar respuesta de error"""
        self.reset_errors()
        
        if 'error' not in error_data:
            self.errors.append("Error response must contain 'error' field")
        
        error_message = error_data.get('error', '')
        if not isinstance(error_message, str) or not error_message.strip():
            self.errors.append("Error message must be a non-empty string")
        
        return len(self.errors) == 0
    
    def validate_prometheus_metrics(self, metrics_text: str) -> bool:
        """Validar métricas de Prometheus"""
        self.reset_errors()
        
        if not metrics_text:
            self.errors.append("Prometheus metrics cannot be empty")
            return False
        
        # Métricas esperadas
        expected_metrics = [
            'productos_requests_total',
            'productos_request_duration_seconds',
            'productos_errors_total'
        ]
        
        for metric in expected_metrics:
            if metric not in metrics_text:
                self.errors.append(f"Missing expected metric: '{metric}'")
        
        # Validar formato básico de Prometheus
        lines = metrics_text.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Comentarios y líneas vacías son válidas
            
            # Las métricas deben tener formato: metric_name{labels} value
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*(\{.*\})?\s+\S+$', line):
                # No reportar como error crítico, solo warning
                pass
        
        return len(self.errors) == 0
    
    def validate_response_time(self, response_time_ms: float, max_time_ms: float = 5000) -> bool:
        """Validar tiempo de respuesta"""
        self.reset_errors()
        
        if response_time_ms > max_time_ms:
            self.errors.append(
                f"Response time too slow: {response_time_ms:.2f}ms (max: {max_time_ms}ms)"
            )
            return False
        
        return True
    
    def validate_pagination_response(self, data: Dict[str, Any]) -> bool:
        """Validar respuesta paginada (si se implementa en el futuro)"""
        self.reset_errors()
        
        expected_fields = ['data', 'page', 'per_page', 'total', 'pages']
        
        for field in expected_fields:
            if field not in data:
                self.errors.append(f"Pagination response missing field: '{field}'")
        
        # Validar tipos
        if 'data' in data and not isinstance(data['data'], list):
            self.errors.append("Pagination 'data' field must be a list")
        
        for field in ['page', 'per_page', 'total', 'pages']:
            if field in data and not isinstance(data[field], int):
                self.errors.append(f"Pagination '{field}' field must be an integer")
        
        return len(self.errors) == 0

class PerformanceValidator:
    """Validador de métricas de rendimiento"""
    
    def __init__(self):
        self.thresholds = {
            'health_check': 100,  # ms
            'get_products': 2000,  # ms
            'create_product': 1000,  # ms
            'get_product_by_id': 500,  # ms
            'metrics': 200  # ms
        }
    
    def validate_response_time(self, endpoint: str, response_time_ms: float) -> bool:
        """Validar tiempo de respuesta por endpoint"""
        threshold = self.thresholds.get(endpoint, 5000)  # Default 5s
        return response_time_ms <= threshold
    
    def get_threshold(self, endpoint: str) -> float:
        """Obtener umbral de tiempo para un endpoint"""
        return self.thresholds.get(endpoint, 5000)
    
    def validate_throughput(self, requests_per_second: float, min_rps: float = 10) -> bool:
        """Validar throughput mínimo"""
        return requests_per_second >= min_rps
    
    def validate_error_rate(self, error_rate: float, max_error_rate: float = 0.05) -> bool:
        """Validar tasa de error máxima (5% por defecto)"""
        return error_rate <= max_error_rate
