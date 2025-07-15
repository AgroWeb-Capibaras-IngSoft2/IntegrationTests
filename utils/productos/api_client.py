"""
Cliente API especializado para pruebas de integración del Servicio de Gestión de Productos
Encapsula todas las operaciones de la API REST siguiendo el patrón AgroWeb
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ProductsAPIClient:
    """Cliente HTTP para interactuar con la API de Gestión de Productos AgroWeb"""
    
    def __init__(self, session: requests.Session, base_url: str = "http://localhost:5000"):
        self.session = session
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'AgroWeb-ProductsIntegrationTest/1.0'
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Realizar request HTTP con logging y manejo de errores"""
        url = f"{self.base_url}{endpoint}"
        
        # Agregar headers por defecto si no se especifican otros
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers.copy()
        else:
            # Merge headers
            merged_headers = self.headers.copy()
            merged_headers.update(kwargs['headers'])
            kwargs['headers'] = merged_headers
        
        logger.info(f"🌐 {method.upper()} {url}")
        if 'json' in kwargs:
            logger.debug(f"📤 Request body: {json.dumps(kwargs['json'], indent=2)}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"📊 Response: {response.status_code} ({len(response.content)} bytes)")
            
            # Log response content for debugging (except for large responses)
            if len(response.content) < 1000:
                try:
                    response_data = response.json()
                    logger.debug(f"📥 Response body: {json.dumps(response_data, indent=2)}")
                except:
                    logger.debug(f"📥 Response body: {response.text}")
            
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request failed: {str(e)}")
            raise
    
    # Endpoints principales de la API
    
    def get_health(self) -> requests.Response:
        """GET /health - Health check del servicio"""
        return self._make_request('GET', '/health')
    
    def get_all_products(self) -> requests.Response:
        """GET /products - Obtener todos los productos"""
        return self._make_request('GET', '/products')
    
    def get_product_by_id(self, product_id: str) -> requests.Response:
        """GET /products/{id} - Obtener producto específico por ID"""
        return self._make_request('GET', f'/products/{product_id}')
    
    def create_product(self, product_data: Dict[str, Any]) -> requests.Response:
        """POST /products - Crear nuevo producto (productId se auto-genera)"""
        return self._make_request('POST', '/products', json=product_data)
    
    def get_metrics(self) -> requests.Response:
        """GET /metrics - Obtener métricas de Prometheus"""
        # Para métricas, usar headers específicos
        headers = {'Accept': 'text/plain'}
        return self._make_request('GET', '/metrics', headers=headers)
    
    def get_test_endpoint(self) -> requests.Response:
        """GET /test - Endpoint de prueba básico"""
        return self._make_request('GET', '/test')
    
    # Métodos para casos de error y edge cases
    
    def create_product_invalid_data(self, invalid_data: Any) -> requests.Response:
        """POST /products con datos inválidos para testing de errores"""
        return self._make_request('POST', '/products', json=invalid_data)
    
    def create_product_missing_fields(self) -> requests.Response:
        """POST /products con campos faltantes"""
        incomplete_data = {
            "name": "Producto Incompleto"
            # Faltan campos requeridos: category, price, etc.
        }
        return self._make_request('POST', '/products', json=incomplete_data)
    
    def create_product_invalid_content_type(self, data: str) -> requests.Response:
        """POST /products con Content-Type incorrecto"""
        headers = {'Content-Type': 'text/plain'}
        return self._make_request('POST', '/products', data=data, headers=headers)
    
    def get_nonexistent_product(self) -> requests.Response:
        """GET producto que no existe para testing 404"""
        return self._make_request('GET', '/products/PROD-NONEXISTENT123')
    
    def get_invalid_product_id(self) -> requests.Response:
        """GET con ID de producto inválido"""
        return self._make_request('GET', '/products/INVALID_ID_FORMAT')
    
    def get_nonexistent_endpoint(self) -> requests.Response:
        """GET endpoint que no existe para testing 404"""
        return self._make_request('GET', '/nonexistent/endpoint/123')
    
    # Métodos de utilidad para testing
    
    def create_multiple_products(self, products_data: List[Dict[str, Any]]) -> List[requests.Response]:
        """Crear múltiples productos para testing de carga"""
        responses = []
        for product_data in products_data:
            response = self.create_product(product_data)
            responses.append(response)
        return responses
    
    def measure_response_time(self, method: str, endpoint: str, **kwargs) -> tuple:
        """Medir tiempo de respuesta de un endpoint"""
        start_time = datetime.now()
        response = self._make_request(method, endpoint, **kwargs)
        end_time = datetime.now()
        response_time_ms = (end_time - start_time).total_seconds() * 1000
        return response, response_time_ms

class APITestHelper:
    """Utilidades adicionales para testing de API de productos"""
    
    @staticmethod
    def validate_json_response(response: requests.Response) -> Dict[str, Any]:
        """Validar que la respuesta sea JSON válido"""
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise AssertionError(f"Respuesta no es JSON válido: {str(e)}")
    
    @staticmethod
    def validate_product_structure(product: Dict[str, Any]) -> bool:
        """Validar estructura básica de un producto"""
        required_fields = [
            'productId', 'name', 'category', 'price', 'unit', 
            'imageUrl', 'stock', 'origin', 'description', 'isActive'
        ]
        
        for field in required_fields:
            if field not in product:
                raise AssertionError(f"Campo requerido '{field}' faltante en producto")
        
        # Validaciones de tipo
        if not isinstance(product['price'], (int, float)) or product['price'] < 0:
            raise AssertionError("Campo 'price' debe ser numérico positivo")
        
        if not isinstance(product['stock'], int) or product['stock'] < 0:
            raise AssertionError("Campo 'stock' debe ser entero no negativo")
        
        if not isinstance(product['isActive'], bool):
            raise AssertionError("Campo 'isActive' debe ser booleano")
        
        # Validar formato de productId (PROD-XXXXXXXX)
        product_id = product['productId']
        if not (product_id.startswith('PROD-') and len(product_id) >= 13):
            raise AssertionError(f"ProductId '{product_id}' no tiene formato válido PROD-XXXXXXXX")
        
        return True
    
    @staticmethod
    def validate_products_list(products: List[Dict[str, Any]]) -> bool:
        """Validar lista de productos"""
        if not isinstance(products, list):
            raise AssertionError("La respuesta debe ser una lista")
        
        for i, product in enumerate(products):
            try:
                APITestHelper.validate_product_structure(product)
            except AssertionError as e:
                raise AssertionError(f"Error en producto {i}: {str(e)}")
        
        return True
    
    @staticmethod
    def validate_error_response(response: requests.Response, expected_status: int) -> bool:
        """Validar respuesta de error"""
        if response.status_code != expected_status:
            raise AssertionError(f"Expected status {expected_status}, got {response.status_code}")
        
        try:
            data = response.json()
            if 'error' not in data:
                raise AssertionError("Respuesta de error debe contener campo 'error'")
        except json.JSONDecodeError:
            # Algunas respuestas de error pueden no ser JSON
            pass
        
        return True
    
    @staticmethod
    def extract_product_ids(products: List[Dict[str, Any]]) -> List[str]:
        """Extraer IDs de una lista de productos"""
        return [product['productId'] for product in products if 'productId' in product]
    
    @staticmethod
    def find_product_by_name(products: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
        """Buscar producto por nombre en una lista"""
        for product in products:
            if product.get('name') == name:
                return product
        return None
    
    @staticmethod
    def calculate_total_stock(products: List[Dict[str, Any]]) -> int:
        """Calcular stock total de una lista de productos"""
        return sum(product.get('stock', 0) for product in products)
    
    @staticmethod
    def filter_products_by_category(products: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
        """Filtrar productos por categoría"""
        return [product for product in products if product.get('category') == category]
    
    @staticmethod
    def validate_prometheus_metrics(metrics_text: str) -> bool:
        """Validar formato de métricas de Prometheus"""
        if not metrics_text:
            raise AssertionError("Métricas de Prometheus están vacías")
        
        expected_metrics = [
            'agroweb_productos_info',
            'flask_http_requests_total',
            'flask_http_request_duration_seconds'
        ]
        
        for metric in expected_metrics:
            if metric not in metrics_text:
                raise AssertionError(f"Métrica esperada '{metric}' no encontrada")
        
        return True
