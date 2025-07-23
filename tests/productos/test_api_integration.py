"""
Pruebas de integración completas para la API del Servicio de Gestión de Productos
Prueba todos los endpoints principales y su integración siguiendo el patrón AgroWeb
"""

import pytest
import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List

from config.productos.test_config import TestConfig
from utils.productos.api_client import ProductsAPIClient, APITestHelper
from utils.productos.validators import ResponseValidator, PerformanceValidator
from utils.productos.test_data import ProductTestDataGenerator, TestScenarios

class TestProductsAPIIntegration:
    """Suite de pruebas de integración para API de Gestión de Productos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, api_health_check, test_metrics):
        """Configuración inicial para cada test"""
        self.api = ProductsAPIClient(api_client, TestConfig.API_BASE_URL)
        self.validator = ResponseValidator()
        self.performance_validator = PerformanceValidator()
        self.test_data = ProductTestDataGenerator()
        self.metrics = test_metrics
        
    @pytest.mark.api
    @pytest.mark.smoke
    def test_health_check_endpoint(self):
        """
        Prueba: Health check básico del servicio
        Verifica que el servicio esté disponible y responda correctamente
        """
        start_time = time.time()
        
        response = self.api.get_health()
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("health_check", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/health")
        
        # Validaciones de respuesta HTTP
        assert self.validator.validate_http_status(response, 200), \
            f"Health check failed: {response.status_code}"
        
        assert self.validator.validate_content_type(response), \
            "Health check should return JSON content"
        
        # Validar estructura JSON
        data = self.validator.validate_json_response(response)
        assert data is not None, "Health response should be valid JSON"
        
        # Validar contenido específico del health check
        assert self.validator.validate_health_response(data), \
            f"Invalid health response structure: {self.validator.get_errors()}"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("health_check")
        assert self.performance_validator.validate_response_time("health_check", response_time), \
            f"Health check too slow: {response_time:.2f}ms (max: {threshold}ms)"
            
        self.metrics["successful_requests"] += 1
        
    @pytest.mark.api
    @pytest.mark.integration
    def test_get_all_products(self):
        """
        Prueba: Obtener lista de todos los productos
        Verifica que el endpoint retorne una lista válida de productos
        """
        start_time = time.time()
        
        response = self.api.get_all_products()
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("get_products", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/products")
        
        # Validaciones HTTP
        assert response.status_code == 200, f"Get products failed: {response.status_code}"
        assert self.validator.validate_content_type(response)
        
        # Validar JSON
        data = self.validator.validate_json_response(response)
        assert data is not None, "Products response should be valid JSON"
        
        # Validar estructura de lista de productos
        assert self.validator.validate_products_list(data), \
            f"Invalid products list: {self.validator.get_errors()}"
        
        # Validaciones adicionales de negocio
        for product in data:
            # Verificar consistencia del campo inStock
            expected_in_stock = product['stock'] > 0
            assert product['inStock'] == expected_in_stock, \
                f"Product {product['productId']}: inStock inconsistent with stock"
            
            # Verificar categorías válidas
            assert product['category'] in TestConfig.VALID_CATEGORIES, \
                f"Product {product['productId']}: invalid category '{product['category']}'"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("get_products")
        assert response_time <= threshold, \
            f"Get products too slow: {response_time:.2f}ms (max: {threshold}ms)"
            
        self.metrics["successful_requests"] += 1
        
        # Guardar productos encontrados para otros tests
        self.metrics["products_found"] = len(data)
        if data:
            self.metrics["sample_product_id"] = data[0]['productId']
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_create_product_valid_data(self, created_products):
        """
        Prueba: Crear producto con datos válidos
        Verifica que se puedan crear productos con todos los campos requeridos
        """
        # Generar datos de prueba válidos
        product_data = self.test_data.generate_valid_product(
            category="vegetales",
            custom_name="Integration Test Papa Criolla"
        )
        
        start_time = time.time()
        
        response = self.api.create_product(product_data)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("create_product", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/products POST")
        
        # Validaciones HTTP
        assert response.status_code == 201, \
            f"Create product failed: {response.status_code} - {response.text}"
        
        assert self.validator.validate_content_type(response)
        
        # Validar JSON response
        created_product = self.validator.validate_json_response(response)
        assert created_product is not None, "Created product response should be valid JSON"
        
        # Validar estructura del producto creado
        assert self.validator.validate_product_structure(created_product), \
            f"Invalid created product structure: {self.validator.get_errors()}"
        
        # Validaciones específicas de creación
        assert 'productId' in created_product, "Created product should have productId"
        assert created_product['productId'].startswith('PROD-'), \
            "ProductId should start with 'PROD-'"
        
        # Verificar que los datos enviados coincidan con los recibidos
        for field in ['name', 'category', 'price', 'unit', 'stock', 'origin', 'description']:
            assert created_product[field] == product_data[field], \
                f"Field '{field}' mismatch: expected {product_data[field]}, got {created_product[field]}"
        
        # Registrar el producto creado para cleanup
        product_id = created_product['productId']
        created_products(product_data)  # Usar fixture para tracking
        self.metrics["created_product_id"] = product_id
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("create_product")
        assert response_time <= threshold, \
            f"Create product too slow: {response_time:.2f}ms (max: {threshold}ms)"
            
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_get_product_by_id(self):
        """
        Prueba: Obtener producto específico por ID
        Verifica que se pueda consultar un producto individual
        """
        # Primero crear un producto para consultarlo
        product_data = self.test_data.generate_valid_product(
            custom_name="Test Product for ID Query"
        )
        
        create_response = self.api.create_product(product_data)
        assert create_response.status_code == 201, "Setup: Failed to create test product"
        
        created_product = create_response.json()
        product_id = created_product['productId']
        
        # Consultar el producto por ID
        start_time = time.time()
        
        response = self.api.get_product_by_id(product_id)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("get_product_by_id", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add(f"/products/{product_id}")
        
        # Validaciones HTTP
        assert response.status_code == 200, \
            f"Get product by ID failed: {response.status_code}"
        
        assert self.validator.validate_content_type(response)
        
        # Validar JSON
        product = self.validator.validate_json_response(response)
        assert product is not None, "Product response should be valid JSON"
        
        # Validar estructura
        assert self.validator.validate_product_structure(product), \
            f"Invalid product structure: {self.validator.get_errors()}"
        
        # Verificar que es el producto correcto
        assert product['productId'] == product_id, \
            f"Wrong product returned: expected {product_id}, got {product['productId']}"
        
        # Verificar consistencia de datos
        assert product['name'] == product_data['name'], \
            "Product name should match original data"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("get_product_by_id")
        assert response_time <= threshold, \
            f"Get product by ID too slow: {response_time:.2f}ms (max: {threshold}ms)"
            
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_create_multiple_products_different_categories(self, created_products):
        """
        Prueba: Crear productos en diferentes categorías
        Verifica que el sistema maneje productos de todas las categorías válidas
        """
        products_by_category = self.test_data.generate_products_by_category()
        created_ids = []
        
        for category, products in products_by_category.items():
            for product_data in products:
                start_time = time.time()
                
                response = self.api.create_product(product_data)
                
                response_time = (time.time() - start_time) * 1000
                self.metrics["response_times"].append(("create_product", response_time))
                self.metrics["requests_made"] += 1
                
                # Validar respuesta
                assert response.status_code == 201, \
                    f"Failed to create {category} product: {response.status_code}"
                
                created_product = response.json()
                created_ids.append(created_product['productId'])
                
                # Verificar categoría
                assert created_product['category'] == category, \
                    f"Category mismatch: expected {category}, got {created_product['category']}"
                
                self.metrics["successful_requests"] += 1
        
        # Verificar que se crearon productos en todas las categorías
        assert len(created_ids) == sum(len(products) for products in products_by_category.values()), \
            "Not all products were created successfully"
        
        self.metrics["created_products_count"] = len(created_ids)
        
        # Verificar que todos los productos son recuperables
        get_all_response = self.api.get_all_products()
        assert get_all_response.status_code == 200
        
        all_products = get_all_response.json()
        all_product_ids = [p['productId'] for p in all_products]
        
        for created_id in created_ids:
            assert created_id in all_product_ids, \
                f"Created product {created_id} not found in product list"
    
    @pytest.mark.api
    @pytest.mark.observability
    def test_metrics_endpoint(self):
        """
        Prueba: Endpoint de métricas de observabilidad
        Verifica que las métricas de Prometheus estén disponibles
        """
        start_time = time.time()
        
        response = self.api.get_metrics()
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("metrics", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/metrics")
        
        # Validaciones HTTP
        assert response.status_code == 200, f"Metrics endpoint failed: {response.status_code}"
        
        # Las métricas deberían ser texto plano, no JSON
        content_type = response.headers.get('Content-Type', '')
        assert 'text/plain' in content_type or 'text/html' in content_type, \
            f"Metrics should be text/plain, got: {content_type}"
        
        # Validar contenido de métricas
        metrics_text = response.text
        assert self.validator.validate_prometheus_metrics(metrics_text), \
            f"Invalid Prometheus metrics format: {self.validator.get_errors()}"
        
        # Verificar métricas específicas del servicio
        expected_metrics = [
            'productos_requests_total',
            'productos_request_duration_seconds',
            'productos_errors_total'
        ]
        
        for metric in expected_metrics:
            assert metric in metrics_text, f"Missing expected metric: {metric}"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("metrics")
        assert response_time <= threshold, \
            f"Metrics endpoint too slow: {response_time:.2f}ms (max: {threshold}ms)"
            
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_test_endpoint(self):
        """
        Prueba: Endpoint de test básico
        Verifica conectividad básica del servicio
        """
        start_time = time.time()
        
        response = self.api.get_test_endpoint()
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("test_endpoint", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/test")
        
        # Validaciones HTTP
        assert response.status_code == 200, f"Test endpoint failed: {response.status_code}"
        
        # Verificar respuesta
        response_text = response.text.strip('"')  # Remover comillas si las hay
        assert "Test route is working!" in response_text, \
            f"Unexpected test response: {response_text}"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("test_endpoint")
        assert response_time <= threshold, \
            f"Test endpoint too slow: {response_time:.2f}ms (max: {threshold}ms)"
            
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.integration
    @pytest.mark.regression
    def test_product_lifecycle_complete(self, created_products):
        """
        Prueba: Ciclo de vida completo de un producto
        Crea un producto, lo consulta, verifica en listado
        """
        # 1. Crear producto
        product_data = self.test_data.generate_valid_product(
            custom_name="Lifecycle Test Product",
            custom_stock=25
        )
        
        create_response = self.api.create_product(product_data)
        assert create_response.status_code == 201
        
        created_product = create_response.json()
        product_id = created_product['productId']
        
        # 2. Consultar producto individual
        get_response = self.api.get_product_by_id(product_id)
        assert get_response.status_code == 200
        
        individual_product = get_response.json()
        assert individual_product['productId'] == product_id
        assert individual_product['name'] == product_data['name']
        
        # 3. Verificar en listado completo
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        all_products = list_response.json()
        found_in_list = False
        
        for product in all_products:
            if product['productId'] == product_id:
                found_in_list = True
                # Verificar consistencia de datos
                assert product['name'] == product_data['name']
                assert product['category'] == product_data['category']
                assert product['price'] == product_data['price']
                break
        
        assert found_in_list, f"Created product {product_id} not found in products list"
        
        # 4. Verificar métricas después de las operaciones
        metrics_response = self.api.get_metrics()
        assert metrics_response.status_code == 200
        
        metrics_text = metrics_response.text
        assert 'flask_http_requests_total' in metrics_text
        
        self.metrics["lifecycle_test_completed"] = True
        self.metrics["successful_requests"] += 4  # create + get + list + metrics
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_concurrent_product_creation(self, created_products):
        """
        Prueba: Creación concurrente de productos
        Verifica que el sistema maneje múltiples creaciones simultáneas
        """
        import threading
        import concurrent.futures
        
        num_products = 10
        products_data = [
            self.test_data.generate_valid_product(
                custom_name=f"Concurrent Test Product {i+1}"
            )
            for i in range(num_products)
        ]
        
        results = []
        start_time = time.time()
        
        # Crear productos concurrentemente
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.api.create_product, product_data)
                for product_data in products_data
            ]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response)
                except Exception as e:
                    self.metrics["errors_encountered"].append(str(e))
        
        total_time = time.time() - start_time
        
        # Validar resultados
        successful_creations = [r for r in results if r.status_code == 201]
        assert len(successful_creations) == num_products, \
            f"Expected {num_products} successful creations, got {len(successful_creations)}"
        
        # Verificar que todos los productos se crearon con IDs únicos
        created_ids = set()
        for response in successful_creations:
            product = response.json()
            product_id = product['productId']
            assert product_id not in created_ids, f"Duplicate product ID: {product_id}"
            created_ids.add(product_id)
        
        # Validar rendimiento
        avg_time_per_request = (total_time / num_products) * 1000
        threshold = TestConfig.get_performance_threshold("create_product")
        assert avg_time_per_request <= threshold, \
            f"Concurrent creation too slow: {avg_time_per_request:.2f}ms avg (max: {threshold}ms)"
        
        self.metrics["concurrent_products_created"] = len(successful_creations)
        self.metrics["concurrent_test_time"] = total_time
        self.metrics["successful_requests"] += len(successful_creations)

    @pytest.mark.api
    @pytest.mark.integration
    def test_get_products_by_user(self):
        """
        Prueba: Obtener productos por usuario
        """
        user_id = "1234567890"
        # Crear productos para ese usuario
        product1 = self.test_data.generate_valid_product(user_id=user_id)
        product2 = self.test_data.generate_valid_product(user_id=user_id)
        self.api.create_product(product1)
        self.api.create_product(product2)
        # Consultar productos por usuario
        response = self.api.get_products_by_user(user_id)
        assert response.status_code == 200
        products = response.json()
        assert all(p['user_id'] == user_id for p in products)