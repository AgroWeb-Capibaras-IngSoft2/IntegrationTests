"""
Pruebas de rendimiento y carga para el Servicio de Gestión de Productos
Verifica el comportamiento del sistema bajo diferentes cargas de trabajo
"""

import pytest
import requests
import time
import statistics
import concurrent.futures
from typing import Dict, Any, List, Tuple
from datetime import datetime

from config.productos.test_config import TestConfig
from utils.productos.api_client import ProductsAPIClient
from utils.productos.validators import ResponseValidator, PerformanceValidator
from utils.productos.test_data import ProductTestDataGenerator, TestScenarios

class TestPerformance:
    """Suite de pruebas de rendimiento y carga"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, api_health_check, test_metrics):
        """Configuración inicial para cada test"""
        self.api = ProductsAPIClient(api_client, TestConfig.API_BASE_URL)
        self.validator = ResponseValidator()
        self.performance_validator = PerformanceValidator()
        self.test_data = ProductTestDataGenerator()
        self.metrics = test_metrics
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_response_time_under_load(self):
        """
        Prueba: Tiempo de respuesta bajo carga
        Verifica que los tiempos de respuesta se mantengan dentro de umbrales aceptables
        """
        num_requests = 50
        concurrent_users = 5
        
        # Preparar datos de prueba
        test_products = [
            self.test_data.generate_valid_product(custom_name=f"Load Test Product {i}")
            for i in range(num_requests)
        ]
        
        response_times = []
        successful_requests = 0
        failed_requests = 0
        
        start_time = time.time()
        
        # Ejecutar requests concurrentes
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # Mapear cada producto a una función de creación
            futures = [
                executor.submit(self._create_product_with_timing, product_data)
                for product_data in test_products
            ]
            
            # Recopilar resultados
            for future in concurrent.futures.as_completed(futures):
                try:
                    response, response_time = future.result()
                    response_times.append(response_time)
                    
                    if response.status_code == 201:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                        
                except Exception as e:
                    failed_requests += 1
                    self.metrics["errors_encountered"].append(str(e))
        
        total_time = time.time() - start_time
        
        # Calcular métricas de rendimiento
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]  # Percentil 95
        p99_response_time = statistics.quantiles(response_times, n=100)[98]  # Percentil 99
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        
        throughput = successful_requests / total_time  # requests per second
        
        # Actualizar métricas
        self.metrics["requests_made"] += num_requests
        self.metrics["successful_requests"] += successful_requests
        self.metrics["failed_requests"] += failed_requests
        self.metrics["load_test_throughput"] = throughput
        self.metrics["avg_response_time"] = avg_response_time
        self.metrics["p95_response_time"] = p95_response_time
        
        # Validaciones de rendimiento
        threshold = TestConfig.get_performance_threshold("create_product")
        
        assert avg_response_time <= threshold, \
            f"Average response time too high: {avg_response_time:.2f}ms (max: {threshold}ms)"
        
        assert p95_response_time <= threshold * 2, \
            f"P95 response time too high: {p95_response_time:.2f}ms (max: {threshold * 2}ms)"
        
        # Verificar tasa de éxito mínima
        success_rate = successful_requests / num_requests
        assert success_rate >= TestConfig.MIN_SUCCESS_RATE, \
            f"Success rate too low: {success_rate:.2%} (min: {TestConfig.MIN_SUCCESS_RATE:.2%})"
        
        # Verificar throughput mínimo
        min_throughput = 5  # requests per second
        assert throughput >= min_throughput, \
            f"Throughput too low: {throughput:.2f} req/s (min: {min_throughput} req/s)"
        
        print(f"\n📊 Performance Metrics:")
        print(f"   • Total requests: {num_requests}")
        print(f"   • Successful: {successful_requests} ({success_rate:.2%})")
        print(f"   • Average response time: {avg_response_time:.2f}ms")
        print(f"   • P95 response time: {p95_response_time:.2f}ms")
        print(f"   • P99 response time: {p99_response_time:.2f}ms")
        print(f"   • Throughput: {throughput:.2f} req/s")
    
    def _create_product_with_timing(self, product_data: Dict[str, Any]) -> Tuple[requests.Response, float]:
        """Crear producto y medir tiempo de respuesta"""
        start_time = time.time()
        response = self.api.create_product(product_data)
        end_time = time.time()
        response_time_ms = (end_time - start_time) * 1000
        return response, response_time_ms
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_get_products_performance_with_large_dataset(self):
        """
        Prueba: Rendimiento de consulta con dataset grande
        Verifica que la consulta de productos mantenga buen rendimiento
        """
        # Crear múltiples productos primero
        num_products = 20
        products_data = [
            self.test_data.generate_valid_product(custom_name=f"Dataset Product {i}")
            for i in range(num_products)
        ]
        
        # Crear productos
        created_count = 0
        for product_data in products_data:
            response = self.api.create_product(product_data)
            if response.status_code == 201:
                created_count += 1
        
        print(f"Created {created_count} products for dataset testing")
        
        # Medir rendimiento de consulta múltiples veces
        num_queries = 10
        response_times = []
        
        for i in range(num_queries):
            start_time = time.time()
            response = self.api.get_all_products()
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
            
            assert response.status_code == 200, f"Query {i+1} failed: {response.status_code}"
            
            # Verificar que retorna datos
            products = response.json()
            assert len(products) >= created_count, \
                f"Should return at least {created_count} products, got {len(products)}"
        
        # Calcular métricas
        avg_query_time = statistics.mean(response_times)
        max_query_time = max(response_times)
        min_query_time = min(response_times)
        
        self.metrics["requests_made"] += num_queries
        self.metrics["successful_requests"] += num_queries
        self.metrics["avg_query_time"] = avg_query_time
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("get_products")
        assert avg_query_time <= threshold, \
            f"Average query time too high: {avg_query_time:.2f}ms (max: {threshold}ms)"
        
        assert max_query_time <= threshold * 1.5, \
            f"Max query time too high: {max_query_time:.2f}ms (max: {threshold * 1.5}ms)"
        
        print(f"\n📊 Query Performance Metrics:")
        print(f"   • Dataset size: {created_count} products")
        print(f"   • Queries performed: {num_queries}")
        print(f"   • Average query time: {avg_query_time:.2f}ms")
        print(f"   • Min query time: {min_query_time:.2f}ms")
        print(f"   • Max query time: {max_query_time:.2f}ms")
    
    @pytest.mark.performance
    @pytest.mark.api
    def test_individual_product_query_performance(self):
        """
        Prueba: Rendimiento de consulta individual de productos
        Verifica que las consultas por ID sean rápidas
        """
        # Crear algunos productos de prueba
        test_products = []
        for i in range(5):
            product_data = self.test_data.generate_valid_product(
                custom_name=f"Query Performance Test {i}"
            )
            response = self.api.create_product(product_data)
            if response.status_code == 201:
                product = response.json()
                test_products.append(product['productId'])
        
        assert len(test_products) > 0, "Need at least one product for testing"
        
        # Medir rendimiento de consultas individuales
        num_queries_per_product = 5
        all_response_times = []
        
        for product_id in test_products:
            for _ in range(num_queries_per_product):
                start_time = time.time()
                response = self.api.get_product_by_id(product_id)
                end_time = time.time()
                
                response_time_ms = (end_time - start_time) * 1000
                all_response_times.append(response_time_ms)
                
                assert response.status_code == 200, \
                    f"Failed to query product {product_id}: {response.status_code}"
                
                self.metrics["requests_made"] += 1
                self.metrics["successful_requests"] += 1
        
        # Calcular métricas
        avg_individual_query = statistics.mean(all_response_times)
        p95_individual_query = statistics.quantiles(all_response_times, n=20)[18]
        
        self.metrics["avg_individual_query_time"] = avg_individual_query
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("get_product_by_id")
        assert avg_individual_query <= threshold, \
            f"Average individual query too slow: {avg_individual_query:.2f}ms (max: {threshold}ms)"
        
        print(f"\n📊 Individual Query Performance:")
        print(f"   • Products tested: {len(test_products)}")
        print(f"   • Queries per product: {num_queries_per_product}")
        print(f"   • Average query time: {avg_individual_query:.2f}ms")
        print(f"   • P95 query time: {p95_individual_query:.2f}ms")
    
    @pytest.mark.performance
    @pytest.mark.observability
    def test_metrics_endpoint_performance(self):
        """
        Prueba: Rendimiento del endpoint de métricas
        Verifica que las métricas se sirvan rápidamente
        """
        num_requests = 20
        response_times = []
        
        for i in range(num_requests):
            start_time = time.time()
            response = self.api.get_metrics()
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
            
            assert response.status_code == 200, f"Metrics request {i+1} failed"
            
            # Verificar que las métricas contienen datos
            metrics_text = response.text
            assert len(metrics_text) > 100, "Metrics response should contain substantial data"
            
            self.metrics["requests_made"] += 1
            self.metrics["successful_requests"] += 1
        
        # Calcular métricas
        avg_metrics_time = statistics.mean(response_times)
        max_metrics_time = max(response_times)
        
        self.metrics["avg_metrics_time"] = avg_metrics_time
        
        # Validar rendimiento - Las métricas deberían ser muy rápidas
        threshold = TestConfig.get_performance_threshold("metrics")
        assert avg_metrics_time <= threshold, \
            f"Metrics endpoint too slow: {avg_metrics_time:.2f}ms (max: {threshold}ms)"
        
        print(f"\n📊 Metrics Endpoint Performance:")
        print(f"   • Requests: {num_requests}")
        print(f"   • Average response time: {avg_metrics_time:.2f}ms")
        print(f"   • Max response time: {max_metrics_time:.2f}ms")
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_sustained_load_performance(self):
        """
        Prueba: Rendimiento bajo carga sostenida
        Verifica que el sistema mantenga rendimiento durante períodos extendidos
        """
        duration_seconds = 30  # Prueba de 30 segundos
        target_rps = 2  # 2 requests per second
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        request_count = 0
        response_times = []
        errors = 0
        
        print(f"\n🔄 Starting sustained load test for {duration_seconds} seconds...")
        
        while time.time() < end_time:
            # Crear producto
            product_data = self.test_data.generate_valid_product(
                custom_name=f"Sustained Load {request_count}"
            )
            
            request_start = time.time()
            response = self.api.create_product(product_data)
            request_end = time.time()
            
            response_time_ms = (request_end - request_start) * 1000
            response_times.append(response_time_ms)
            request_count += 1
            
            if response.status_code != 201:
                errors += 1
            
            # Controlar tasa de requests
            time_to_wait = (1.0 / target_rps) - (request_end - request_start)
            if time_to_wait > 0:
                time.sleep(time_to_wait)
        
        actual_duration = time.time() - start_time
        actual_rps = request_count / actual_duration
        
        # Calcular métricas
        avg_response_time = statistics.mean(response_times)
        error_rate = errors / request_count
        
        self.metrics["requests_made"] += request_count
        self.metrics["successful_requests"] += (request_count - errors)
        self.metrics["failed_requests"] += errors
        self.metrics["sustained_load_rps"] = actual_rps
        self.metrics["sustained_load_avg_time"] = avg_response_time
        self.metrics["sustained_load_error_rate"] = error_rate
        
        # Validaciones
        threshold = TestConfig.get_performance_threshold("create_product")
        assert avg_response_time <= threshold * 1.5, \
            f"Sustained load response time too high: {avg_response_time:.2f}ms"
        
        assert error_rate <= TestConfig.MAX_ERROR_RATE, \
            f"Error rate too high under sustained load: {error_rate:.2%}"
        
        assert actual_rps >= target_rps * 0.8, \
            f"Actual RPS too low: {actual_rps:.2f} (target: {target_rps})"
        
        print(f"📊 Sustained Load Results:")
        print(f"   • Duration: {actual_duration:.1f}s")
        print(f"   • Total requests: {request_count}")
        print(f"   • Actual RPS: {actual_rps:.2f}")
        print(f"   • Average response time: {avg_response_time:.2f}ms")
        print(f"   • Error rate: {error_rate:.2%}")
    
    @pytest.mark.performance
    @pytest.mark.integration
    def test_mixed_workload_performance(self):
        """
        Prueba: Rendimiento con carga de trabajo mixta
        Simula un patrón realista mezclando creación y consulta de productos
        """
        duration_seconds = 20
        
        operations = []
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        # Crear algunos productos iniciales
        initial_products = []
        for i in range(5):
            product_data = self.test_data.generate_valid_product(
                custom_name=f"Mixed Workload Initial {i}"
            )
            response = self.api.create_product(product_data)
            if response.status_code == 201:
                product = response.json()
                initial_products.append(product['productId'])
        
        print(f"\n🔀 Starting mixed workload test for {duration_seconds} seconds...")
        
        operation_count = 0
        while time.time() < end_time:
            operation_start = time.time()
            
            # Alternar entre diferentes operaciones
            operation_type = operation_count % 4
            
            if operation_type == 0:  # Crear producto (25%)
                product_data = self.test_data.generate_valid_product(
                    custom_name=f"Mixed Workload Create {operation_count}"
                )
                response = self.api.create_product(product_data)
                op_name = "create"
                
            elif operation_type == 1:  # Consultar todos los productos (25%)
                response = self.api.get_all_products()
                op_name = "get_all"
                
            elif operation_type == 2 and initial_products:  # Consultar producto específico (25%)
                product_id = initial_products[operation_count % len(initial_products)]
                response = self.api.get_product_by_id(product_id)
                op_name = "get_by_id"
                
            else:  # Health check (25%)
                response = self.api.get_health()
                op_name = "health"
            
            operation_end = time.time()
            response_time_ms = (operation_end - operation_start) * 1000
            
            operations.append({
                'type': op_name,
                'response_time': response_time_ms,
                'status_code': response.status_code,
                'success': response.status_code < 400
            })
            
            operation_count += 1
            
            # Pequeña pausa para simular comportamiento real
            time.sleep(0.1)
        
        # Analizar resultados por tipo de operación
        operations_by_type = {}
        for op in operations:
            op_type = op['type']
            if op_type not in operations_by_type:
                operations_by_type[op_type] = []
            operations_by_type[op_type].append(op)
        
        print(f"\n📊 Mixed Workload Results:")
        for op_type, ops in operations_by_type.items():
            if not ops:
                continue
                
            avg_time = statistics.mean([op['response_time'] for op in ops])
            success_rate = sum(1 for op in ops if op['success']) / len(ops)
            
            print(f"   • {op_type}: {len(ops)} ops, {avg_time:.2f}ms avg, {success_rate:.2%} success")
            
            # Validar que cada tipo de operación mantiene buen rendimiento
            if op_type in ['create', 'get_all', 'get_by_id']:
                threshold = TestConfig.get_performance_threshold(
                    'create_product' if op_type == 'create' else 
                    'get_products' if op_type == 'get_all' else 
                    'get_product_by_id'
                )
                assert avg_time <= threshold * 1.5, \
                    f"{op_type} operations too slow in mixed workload: {avg_time:.2f}ms"
        
        total_operations = len(operations)
        total_success_rate = sum(1 for op in operations if op['success']) / total_operations
        
        self.metrics["requests_made"] += total_operations
        self.metrics["mixed_workload_success_rate"] = total_success_rate
        
        assert total_success_rate >= 0.95, \
            f"Mixed workload success rate too low: {total_success_rate:.2%}"
