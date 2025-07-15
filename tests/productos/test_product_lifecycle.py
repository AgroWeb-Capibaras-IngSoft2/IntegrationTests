"""
Pruebas del ciclo de vida completo de productos para el Servicio de Gestión de Productos
Verifica escenarios completos de negocio y flujos de trabajo end-to-end
"""

import pytest
import requests
import time
from typing import Dict, Any, List
from datetime import datetime

from config.productos.test_config import TestConfig
from utils.productos.api_client import ProductsAPIClient, APITestHelper
from utils.productos.validators import ResponseValidator
from utils.productos.test_data import ProductTestDataGenerator

class TestProductLifecycle:
    """Suite de pruebas del ciclo de vida completo de productos"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, api_health_check, test_metrics):
        """Configuración inicial para cada test"""
        self.api = ProductsAPIClient(api_client, TestConfig.API_BASE_URL)
        self.validator = ResponseValidator()
        self.test_data = ProductTestDataGenerator()
        self.metrics = test_metrics
    
    @pytest.mark.integration
    @pytest.mark.regression
    def test_complete_product_lifecycle(self, created_products):
        """
        Prueba: Ciclo de vida completo de un producto
        Crea → Consulta Individual → Verifica en Lista → Valida Métricas
        """
        # 1. Crear producto
        product_data = self.test_data.generate_valid_product(
            category="vegetables",
            custom_name="Lifecycle Test Papa Criolla Premium",
            custom_stock=150
        )
        
        create_start = time.time()
        create_response = self.api.create_product(product_data)
        create_time = (time.time() - create_start) * 1000
        
        self.metrics["requests_made"] += 1
        self.metrics["response_times"].append(("create_product", create_time))
        
        # Validar creación exitosa
        assert create_response.status_code == 201, \
            f"Product creation failed: {create_response.status_code}"
        
        created_product = create_response.json()
        assert self.validator.validate_product_structure(created_product), \
            f"Invalid created product: {self.validator.get_errors()}"
        
        product_id = created_product['productId']
        assert product_id.startswith('PROD-'), "ProductId should start with PROD-"
        
        # Verificar datos del producto creado
        assert created_product['name'] == product_data['name']
        assert created_product['category'] == product_data['category']
        assert created_product['price'] == product_data['price']
        assert created_product['stock'] == product_data['stock']
        assert created_product['inStock'] == True  # stock > 0
        
        self.metrics["successful_requests"] += 1
        
        # 2. Consultar producto individual
        get_start = time.time()
        get_response = self.api.get_product_by_id(product_id)
        get_time = (time.time() - get_start) * 1000
        
        self.metrics["requests_made"] += 1
        self.metrics["response_times"].append(("get_product_by_id", get_time))
        
        assert get_response.status_code == 200, \
            f"Product retrieval failed: {get_response.status_code}"
        
        retrieved_product = get_response.json()
        assert self.validator.validate_product_structure(retrieved_product), \
            f"Invalid retrieved product: {self.validator.get_errors()}"
        
        # Verificar consistencia de datos
        assert retrieved_product['productId'] == product_id
        assert retrieved_product['name'] == product_data['name']
        assert retrieved_product['category'] == product_data['category']
        assert retrieved_product['price'] == product_data['price']
        
        self.metrics["successful_requests"] += 1
        
        # 3. Verificar producto en lista completa
        list_start = time.time()
        list_response = self.api.get_all_products()
        list_time = (time.time() - list_start) * 1000
        
        self.metrics["requests_made"] += 1
        self.metrics["response_times"].append(("get_all_products", list_time))
        
        assert list_response.status_code == 200, \
            f"Product list retrieval failed: {list_response.status_code}"
        
        all_products = list_response.json()
        assert self.validator.validate_products_list(all_products), \
            f"Invalid products list: {self.validator.get_errors()}"
        
        # Buscar nuestro producto en la lista
        found_product = None
        for product in all_products:
            if product['productId'] == product_id:
                found_product = product
                break
        
        assert found_product is not None, \
            f"Created product {product_id} not found in products list"
        
        # Verificar consistencia en la lista
        assert found_product['name'] == product_data['name']
        assert found_product['category'] == product_data['category']
        assert found_product['price'] == product_data['price']
        
        self.metrics["successful_requests"] += 1
        
        # 4. Validar métricas de observabilidad
        metrics_start = time.time()
        metrics_response = self.api.get_metrics()
        metrics_time = (time.time() - metrics_start) * 1000
        
        self.metrics["requests_made"] += 1
        self.metrics["response_times"].append(("metrics", metrics_time))
        
        assert metrics_response.status_code == 200, \
            "Metrics endpoint should be accessible"
        
        metrics_text = metrics_response.text
        assert self.validator.validate_prometheus_metrics(metrics_text), \
            f"Invalid metrics format: {self.validator.get_errors()}"
        
        # Verificar que las métricas reflejan nuestras operaciones
        assert 'flask_http_requests_total' in metrics_text
        assert 'agroweb_productos_info' in metrics_text
        
        self.metrics["successful_requests"] += 1
        
        # 5. Verificar health check final
        health_response = self.api.get_health()
        assert health_response.status_code == 200
        
        health_data = health_response.json()
        assert health_data['status'] == 'healthy'
        
        self.metrics["requests_made"] += 1
        self.metrics["successful_requests"] += 1
        self.metrics["lifecycle_product_id"] = product_id
        
        print(f"\n✅ Complete lifecycle test successful for product: {product_id}")
        print(f"   • Create time: {create_time:.2f}ms")
        print(f"   • Get time: {get_time:.2f}ms")
        print(f"   • List time: {list_time:.2f}ms")
        print(f"   • Metrics time: {metrics_time:.2f}ms")
    
    @pytest.mark.integration
    @pytest.mark.api
    def test_multiple_products_different_categories_lifecycle(self):
        """
        Prueba: Ciclo de vida de múltiples productos en diferentes categorías
        Verifica que el sistema maneje correctamente productos de todas las categorías
        """
        created_products = []
        
        # Crear un producto por cada categoría válida
        for category in TestConfig.VALID_CATEGORIES:
            product_data = self.test_data.generate_valid_product(
                category=category,
                custom_name=f"Lifecycle Test {category.title()}",
                custom_stock=50
            )
            
            # Crear producto
            create_response = self.api.create_product(product_data)
            assert create_response.status_code == 201, \
                f"Failed to create {category} product"
            
            created_product = create_response.json()
            created_products.append({
                'product_id': created_product['productId'],
                'category': category,
                'original_data': product_data,
                'created_data': created_product
            })
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        # Verificar que todos los productos se crearon
        assert len(created_products) == len(TestConfig.VALID_CATEGORIES), \
            f"Expected {len(TestConfig.VALID_CATEGORIES)} products, created {len(created_products)}"
        
        # Consultar cada producto individualmente
        for product_info in created_products:
            get_response = self.api.get_product_by_id(product_info['product_id'])
            assert get_response.status_code == 200, \
                f"Failed to retrieve {product_info['category']} product"
            
            retrieved_product = get_response.json()
            assert retrieved_product['category'] == product_info['category']
            assert retrieved_product['name'] == product_info['original_data']['name']
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        # Verificar lista completa contiene todos los productos
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        all_products = list_response.json()
        created_ids = {p['product_id'] for p in created_products}
        found_ids = {p['productId'] for p in all_products if p['productId'] in created_ids}
        
        assert created_ids == found_ids, \
            f"Not all created products found in list. Created: {created_ids}, Found: {found_ids}"
        
        # Verificar distribución por categorías
        products_by_category = {}
        for product in all_products:
            if product['productId'] in created_ids:
                category = product['category']
                if category not in products_by_category:
                    products_by_category[category] = []
                products_by_category[category].append(product)
        
        for category in TestConfig.VALID_CATEGORIES:
            assert category in products_by_category, \
                f"No products found for category: {category}"
            assert len(products_by_category[category]) >= 1, \
                f"Expected at least 1 product in {category}, found {len(products_by_category[category])}"
        
        self.metrics["requests_made"] += 1
        self.metrics["successful_requests"] += 1
        self.metrics["multi_category_test_products"] = len(created_products)
        
        print(f"\n✅ Multi-category lifecycle test successful:")
        for category, products in products_by_category.items():
            print(f"   • {category}: {len(products)} product(s)")
    
    @pytest.mark.integration
    @pytest.mark.regression
    def test_product_stock_consistency_lifecycle(self):
        """
        Prueba: Consistencia del stock en el ciclo de vida del producto
        Verifica que el campo inStock se calcule correctamente
        """
        # Crear productos con diferentes niveles de stock
        stock_scenarios = [
            ("Zero Stock Product", 0),
            ("Low Stock Product", 1),
            ("Medium Stock Product", 50),
            ("High Stock Product", 1000)
        ]
        
        created_products = []
        
        for name_suffix, stock_value in stock_scenarios:
            product_data = self.test_data.generate_valid_product(
                custom_name=f"Stock Test {name_suffix}",
                custom_stock=stock_value
            )
            
            # Crear producto
            create_response = self.api.create_product(product_data)
            assert create_response.status_code == 201
            
            created_product = create_response.json()
            expected_in_stock = stock_value > 0
            
            # Verificar cálculo correcto de inStock
            assert created_product['stock'] == stock_value, \
                f"Stock mismatch: expected {stock_value}, got {created_product['stock']}"
            assert created_product['inStock'] == expected_in_stock, \
                f"inStock calculation wrong: stock={stock_value}, inStock={created_product['inStock']}"
            
            created_products.append({
                'product_id': created_product['productId'],
                'stock': stock_value,
                'expected_in_stock': expected_in_stock
            })
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        # Verificar consistencia en consultas individuales
        for product_info in created_products:
            get_response = self.api.get_product_by_id(product_info['product_id'])
            assert get_response.status_code == 200
            
            product = get_response.json()
            assert product['stock'] == product_info['stock']
            assert product['inStock'] == product_info['expected_in_stock']
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        # Verificar consistencia en lista completa
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        all_products = list_response.json()
        created_ids = {p['product_id'] for p in created_products}
        
        for product in all_products:
            if product['productId'] in created_ids:
                # Encontrar el producto correspondiente
                product_info = next(
                    p for p in created_products 
                    if p['product_id'] == product['productId']
                )
                
                assert product['stock'] == product_info['stock'], \
                    f"Stock inconsistency in list for {product['productId']}"
                assert product['inStock'] == product_info['expected_in_stock'], \
                    f"inStock inconsistency in list for {product['productId']}"
        
        self.metrics["requests_made"] += 1
        self.metrics["successful_requests"] += 1
        self.metrics["stock_consistency_test_products"] = len(created_products)
        
        print(f"\n✅ Stock consistency test successful:")
        for product_info in created_products:
            print(f"   • Stock {product_info['stock']}: inStock = {product_info['expected_in_stock']}")
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_bulk_product_creation_lifecycle(self):
        """
        Prueba: Ciclo de vida de creación masiva de productos
        Verifica que el sistema maneje múltiples productos eficientemente
        """
        num_products = 25
        bulk_products = self.test_data.generate_bulk_products(
            count=num_products,
            category="vegetables"
        )
        
        created_ids = []
        creation_times = []
        
        print(f"\n🔄 Creating {num_products} products in bulk...")
        
        # Crear productos en lote
        start_time = time.time()
        for i, product_data in enumerate(bulk_products):
            create_start = time.time()
            response = self.api.create_product(product_data)
            create_end = time.time()
            
            creation_time = (create_end - create_start) * 1000
            creation_times.append(creation_time)
            
            assert response.status_code == 201, \
                f"Bulk creation failed at product {i+1}: {response.status_code}"
            
            created_product = response.json()
            created_ids.append(created_product['productId'])
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
            
            # Progreso cada 10 productos
            if (i + 1) % 10 == 0:
                print(f"   Created {i + 1}/{num_products} products...")
        
        total_creation_time = time.time() - start_time
        avg_creation_time = sum(creation_times) / len(creation_times)
        
        # Verificar que todos los productos se crearon
        assert len(created_ids) == num_products, \
            f"Expected {num_products} products, created {len(created_ids)}"
        
        # Verificar unicidad de IDs
        assert len(set(created_ids)) == num_products, \
            "Some product IDs are duplicated"
        
        # Verificar rendimiento de creación masiva
        max_avg_time = TestConfig.get_performance_threshold("create_product")
        assert avg_creation_time <= max_avg_time, \
            f"Bulk creation too slow: {avg_creation_time:.2f}ms avg (max: {max_avg_time}ms)"
        
        # Verificar que todos los productos aparecen en la lista
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        all_products = list_response.json()
        all_product_ids = {p['productId'] for p in all_products}
        
        missing_ids = set(created_ids) - all_product_ids
        assert len(missing_ids) == 0, \
            f"Some bulk created products missing from list: {missing_ids}"
        
        # Verificar consulta individual de muestra
        sample_ids = created_ids[:5]  # Consultar primeros 5
        for product_id in sample_ids:
            get_response = self.api.get_product_by_id(product_id)
            assert get_response.status_code == 200, \
                f"Failed to retrieve bulk created product: {product_id}"
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        self.metrics["requests_made"] += 1  # Para get_all_products
        self.metrics["successful_requests"] += 1
        self.metrics["bulk_creation_count"] = num_products
        self.metrics["bulk_creation_avg_time"] = avg_creation_time
        self.metrics["bulk_creation_total_time"] = total_creation_time
        
        print(f"✅ Bulk creation lifecycle test successful:")
        print(f"   • Products created: {num_products}")
        print(f"   • Total time: {total_creation_time:.2f}s")
        print(f"   • Average per product: {avg_creation_time:.2f}ms")
        print(f"   • Throughput: {num_products/total_creation_time:.2f} products/s")
    
    @pytest.mark.integration
    @pytest.mark.regression
    def test_edge_cases_lifecycle(self):
        """
        Prueba: Ciclo de vida con casos extremos
        Verifica manejo correcto de valores límite y casos especiales
        """
        edge_case_products = self.test_data.generate_edge_case_products()
        
        created_products = []
        
        for i, product_data in enumerate(edge_case_products):
            # Crear producto
            create_response = self.api.create_product(product_data)
            assert create_response.status_code == 201, \
                f"Edge case product {i} creation failed: {create_response.status_code}"
            
            created_product = create_response.json()
            created_products.append(created_product)
            
            # Validar estructura
            assert self.validator.validate_product_structure(created_product), \
                f"Invalid edge case product {i}: {self.validator.get_errors()}"
            
            # Verificar datos específicos del caso extremo
            assert created_product['price'] == product_data['price']
            assert created_product['stock'] == product_data['stock']
            assert created_product['inStock'] == (product_data['stock'] > 0)
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        # Verificar que todos los casos extremos aparecen en la lista
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        all_products = list_response.json()
        created_ids = {p['productId'] for p in created_products}
        found_ids = {p['productId'] for p in all_products if p['productId'] in created_ids}
        
        assert created_ids == found_ids, \
            "Not all edge case products found in list"
        
        # Verificar casos específicos en la lista
        for product in all_products:
            if product['productId'] in created_ids:
                # Verificar consistencia de cálculos
                assert product['inStock'] == (product['stock'] > 0), \
                    f"Edge case inStock calculation wrong for {product['productId']}"
                
                # Verificar valores extremos se mantienen
                assert product['price'] >= 0, \
                    f"Edge case price should be non-negative: {product['price']}"
                assert product['stock'] >= 0, \
                    f"Edge case stock should be non-negative: {product['stock']}"
        
        self.metrics["requests_made"] += 1
        self.metrics["successful_requests"] += 1
        self.metrics["edge_cases_tested"] = len(edge_case_products)
        
        print(f"\n✅ Edge cases lifecycle test successful:")
        print(f"   • Edge cases tested: {len(edge_case_products)}")
        print(f"   • All cases handled correctly")
    
    @pytest.mark.integration
    @pytest.mark.observability
    def test_observability_during_lifecycle(self):
        """
        Prueba: Observabilidad durante el ciclo de vida completo
        Verifica que las métricas se actualicen correctamente durante las operaciones
        """
        # Obtener métricas iniciales
        initial_metrics_response = self.api.get_metrics()
        assert initial_metrics_response.status_code == 200
        initial_metrics = initial_metrics_response.text
        
        # Realizar múltiples operaciones
        operations_count = 10
        
        for i in range(operations_count):
            # Crear producto
            product_data = self.test_data.generate_valid_product(
                custom_name=f"Observability Test Product {i}"
            )
            create_response = self.api.create_product(product_data)
            assert create_response.status_code == 201
            
            created_product = create_response.json()
            product_id = created_product['productId']
            
            # Consultar producto
            get_response = self.api.get_product_by_id(product_id)
            assert get_response.status_code == 200
            
            # Health check
            health_response = self.api.get_health()
            assert health_response.status_code == 200
            
            self.metrics["requests_made"] += 3
            self.metrics["successful_requests"] += 3
        
        # Consultar lista de productos
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        # Obtener métricas finales
        final_metrics_response = self.api.get_metrics()
        assert final_metrics_response.status_code == 200
        final_metrics = final_metrics_response.text
        
        self.metrics["requests_made"] += 2
        self.metrics["successful_requests"] += 2
        
        # Verificar que las métricas contienen información actualizada
        assert 'flask_http_requests_total' in final_metrics
        assert 'flask_http_request_duration_seconds' in final_metrics
        
        # Verificar que hay más datos en las métricas finales
        assert len(final_metrics) >= len(initial_metrics), \
            "Final metrics should contain at least as much data as initial"
        
        # Verificar métricas específicas del servicio
        expected_endpoints = ['/products', '/health', '/metrics']
        for endpoint in expected_endpoints:
            # Buscar métricas que mencionen estos endpoints
            if endpoint == '/products':
                assert 'products' in final_metrics.lower() or '/products' in final_metrics
        
        self.metrics["observability_operations"] = operations_count * 3 + 2
        
        print(f"\n✅ Observability lifecycle test successful:")
        print(f"   • Operations performed: {operations_count * 3 + 2}")
        print(f"   • Initial metrics size: {len(initial_metrics)} chars")
        print(f"   • Final metrics size: {len(final_metrics)} chars")
        print(f"   • Metrics properly updated")

class TestBusinessLogicLifecycle:
    """Pruebas de lógica de negocio en ciclos de vida completos"""
    
    @pytest.fixture(autouse=True) 
    def setup(self, api_client, api_health_check, test_metrics):
        """Configuración inicial para cada test"""
        self.api = ProductsAPIClient(api_client, TestConfig.API_BASE_URL)
        self.validator = ResponseValidator()
        self.test_data = ProductTestDataGenerator()
        self.metrics = test_metrics
    
    @pytest.mark.integration
    @pytest.mark.regression
    def test_category_based_product_management_lifecycle(self):
        """
        Prueba: Gestión de productos por categoría a lo largo del ciclo de vida
        Verifica que las categorías se manejen correctamente en todas las operaciones
        """
        # Crear productos específicos por categoría
        products_by_category = {}
        
        for category in TestConfig.VALID_CATEGORIES:
            products_by_category[category] = []
            
            # Crear 3 productos por categoría
            for i in range(3):
                product_data = self.test_data.generate_valid_product(
                    category=category,
                    custom_name=f"Category Test {category} Product {i+1}"
                )
                
                create_response = self.api.create_product(product_data)
                assert create_response.status_code == 201
                
                created_product = create_response.json()
                products_by_category[category].append(created_product)
                
                self.metrics["requests_made"] += 1
                self.metrics["successful_requests"] += 1
        
        # Verificar distribución en lista completa
        list_response = self.api.get_all_products()
        assert list_response.status_code == 200
        
        all_products = list_response.json()
        
        # Contar productos por categoría en la lista
        category_counts = {}
        all_created_ids = set()
        
        for category, products in products_by_category.items():
            for product in products:
                all_created_ids.add(product['productId'])
        
        for product in all_products:
            if product['productId'] in all_created_ids:
                category = product['category']
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Verificar que cada categoría tiene los productos esperados
        for category in TestConfig.VALID_CATEGORIES:
            assert category in category_counts, f"No products found for category {category}"
            assert category_counts[category] >= 3, \
                f"Expected at least 3 products for {category}, found {category_counts[category]}"
        
        self.metrics["requests_made"] += 1
        self.metrics["successful_requests"] += 1
        self.metrics["category_management_test_completed"] = True
        
        print(f"\n✅ Category-based management lifecycle successful:")
        for category, count in category_counts.items():
            print(f"   • {category}: {count} products")
