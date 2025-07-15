"""
Pruebas de casos de error y manejo de excepciones para el Servicio de Gestión de Productos
Verifica el comportamiento del sistema ante datos inválidos y condiciones de error
"""

import pytest
import requests
import json
import time
from typing import Dict, Any, List

from config.productos.test_config import TestConfig
from utils.productos.api_client import ProductsAPIClient, APITestHelper
from utils.productos.validators import ResponseValidator
from utils.productos.test_data import ProductTestDataGenerator, TestScenarios

class TestErrorScenarios:
    """Suite de pruebas para casos de error y manejo de excepciones"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_client, api_health_check, test_metrics):
        """Configuración inicial para cada test"""
        self.api = ProductsAPIClient(api_client, TestConfig.API_BASE_URL)
        self.validator = ResponseValidator()
        self.test_data = ProductTestDataGenerator()
        self.metrics = test_metrics
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_missing_required_fields(self):
        """
        Prueba: Crear producto con campos requeridos faltantes
        Verifica que la API rechace productos incompletos con error 400
        """
        incomplete_product = self.test_data.generate_invalid_product_missing_fields()
        
        response = self.api.create_product_invalid_data(incomplete_product)
        
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/products POST (error)")
        
        # Validar respuesta de error
        assert response.status_code == 400, \
            f"Expected 400 for missing fields, got {response.status_code}"
        
        # Validar formato de error
        assert self.validator.validate_content_type(response), \
            "Error response should be JSON"
        
        error_data = self.validator.validate_json_response(response)
        assert error_data is not None, "Error response should be valid JSON"
        
        assert self.validator.validate_error_response(error_data, 400), \
            f"Invalid error response: {self.validator.get_errors()}"
        
        # Verificar mensaje de error descriptivo
        error_message = error_data.get('error', '')
        assert 'campo' in error_message.lower() or 'field' in error_message.lower(), \
            f"Error message should mention missing fields: {error_message}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_invalid_data_types(self):
        """
        Prueba: Crear producto con tipos de datos incorrectos
        Verifica validación de tipos de datos
        """
        invalid_product = self.test_data.generate_invalid_product_wrong_types()
        
        response = self.api.create_product_invalid_data(invalid_product)
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 400 por datos inválidos
        assert response.status_code == 400, \
            f"Expected 400 for invalid data types, got {response.status_code}"
        
        error_data = response.json()
        assert 'error' in error_data, "Error response should contain error message"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_negative_values(self):
        """
        Prueba: Crear producto con valores negativos
        Verifica validación de valores numéricos
        """
        negative_product = self.test_data.generate_invalid_product_negative_values()
        
        response = self.api.create_product_invalid_data(negative_product)
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 400 por valores inválidos
        assert response.status_code == 400, \
            f"Expected 400 for negative values, got {response.status_code}"
        
        error_data = response.json()
        error_message = error_data.get('error', '')
        
        # El mensaje debería mencionar valores negativos o inválidos
        assert any(word in error_message.lower() for word in ['negativ', 'invalid', 'positive']), \
            f"Error message should mention negative values: {error_message}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_invalid_category(self):
        """
        Prueba: Crear producto con categoría inválida
        Verifica validación de categorías permitidas
        """
        invalid_category_product = self.test_data.generate_invalid_product_invalid_category()
        
        response = self.api.create_product_invalid_data(invalid_category_product)
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 400 por categoría inválida
        assert response.status_code == 400, \
            f"Expected 400 for invalid category, got {response.status_code}"
        
        error_data = response.json()
        error_message = error_data.get('error', '')
        
        # El mensaje debería mencionar categoría inválida
        assert 'categor' in error_message.lower(), \
            f"Error message should mention category validation: {error_message}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_empty_data(self):
        """
        Prueba: Crear producto con datos completamente vacíos
        Verifica manejo de requests vacíos
        """
        empty_product = self.test_data.generate_empty_product()
        
        response = self.api.create_product_invalid_data(empty_product)
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 400 por datos faltantes
        assert response.status_code == 400, \
            f"Expected 400 for empty data, got {response.status_code}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_invalid_content_type(self):
        """
        Prueba: Crear producto con Content-Type incorrecto
        Verifica validación de headers HTTP
        """
        product_data = self.test_data.generate_valid_product()
        product_json = json.dumps(product_data)
        
        response = self.api.create_product_invalid_content_type(product_json)
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 415 (Unsupported Media Type)
        assert response.status_code == 415, \
            f"Expected 415 for invalid content type, got {response.status_code}"
        
        error_data = response.json()
        error_message = error_data.get('error', '')
        
        # El mensaje debería mencionar Content-Type
        assert 'content-type' in error_message.lower() or 'application/json' in error_message.lower(), \
            f"Error message should mention Content-Type: {error_message}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_get_nonexistent_product(self):
        """
        Prueba: Consultar producto que no existe
        Verifica manejo de recursos no encontrados
        """
        response = self.api.get_nonexistent_product()
        
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/products/NONEXISTENT")
        
        # Debería retornar error 404 (Not Found)
        assert response.status_code == 404, \
            f"Expected 404 for nonexistent product, got {response.status_code}"
        
        error_data = response.json()
        assert self.validator.validate_error_response(error_data, 404), \
            f"Invalid 404 error response: {self.validator.get_errors()}"
        
        error_message = error_data.get('error', '')
        assert 'encontrado' in error_message.lower() or 'not found' in error_message.lower(), \
            f"Error message should indicate product not found: {error_message}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_get_product_invalid_id_format(self):
        """
        Prueba: Consultar producto con ID de formato inválido
        Verifica validación de formato de IDs
        """
        response = self.api.get_invalid_product_id()
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 400 o 404 dependiendo de la implementación
        assert response.status_code in [400, 404], \
            f"Expected 400 or 404 for invalid ID format, got {response.status_code}"
        
        error_data = response.json()
        error_message = error_data.get('error', '')
        
        if response.status_code == 400:
            assert 'invalid' in error_message.lower() or 'formato' in error_message.lower(), \
                f"Error message should mention invalid ID format: {error_message}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_get_nonexistent_endpoint(self):
        """
        Prueba: Acceder a endpoint que no existe
        Verifica manejo de rutas inexistentes
        """
        response = self.api.get_nonexistent_endpoint()
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 404 (Not Found)
        assert response.status_code == 404, \
            f"Expected 404 for nonexistent endpoint, got {response.status_code}"
        
        self.metrics["failed_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.api
    def test_create_product_very_long_strings(self):
        """
        Prueba: Crear producto con strings excesivamente largos
        Verifica validación de longitud de campos
        """
        long_strings_product = self.test_data.generate_product_with_very_long_strings()
        
        response = self.api.create_product_invalid_data(long_strings_product)
        
        self.metrics["requests_made"] += 1
        
        # Debería retornar error 400 por datos inválidos (strings muy largos)
        # Nota: Dependiendo de la implementación, podría aceptarse o rechazarse
        if response.status_code == 400:
            error_data = response.json()
            error_message = error_data.get('error', '')
            # Verificar que el error mencione longitud o tamaño
            assert any(word in error_message.lower() for word in ['long', 'length', 'size', 'large']), \
                f"Error should mention string length: {error_message}"
            self.metrics["failed_requests"] += 1
        else:
            # Si se acepta, verificar que el producto se creó correctamente
            assert response.status_code == 201, \
                f"Unexpected status code: {response.status_code}"
            self.metrics["successful_requests"] += 1
    
    @pytest.mark.error_handling
    @pytest.mark.performance
    def test_multiple_error_scenarios_performance(self):
        """
        Prueba: Rendimiento del sistema bajo múltiples errores
        Verifica que los errores no degraden significativamente el performance
        """
        error_test_cases = TestScenarios.get_error_test_cases()
        
        start_time = time.time()
        
        for i, invalid_data in enumerate(error_test_cases):
            response = self.api.create_product_invalid_data(invalid_data)
            
            self.metrics["requests_made"] += 1
            
            # Verificar que el sistema responde con error apropiado
            assert response.status_code in [400, 415], \
                f"Test case {i}: Expected error status, got {response.status_code}"
            
            # Verificar que el sistema sigue respondiendo (no crash)
            try:
                response.json()  # Debe ser JSON válido
            except json.JSONDecodeError:
                pytest.fail(f"Test case {i}: Error response is not valid JSON")
            
            self.metrics["failed_requests"] += 1
        
        total_time = time.time() - start_time
        avg_time_per_error = (total_time / len(error_test_cases)) * 1000
        
        # Los errores deberían ser rápidos de procesar
        assert avg_time_per_error <= 1000, \
            f"Error handling too slow: {avg_time_per_error:.2f}ms avg per error"
        
        self.metrics["error_handling_performance"] = avg_time_per_error
    
    @pytest.mark.error_handling
    @pytest.mark.regression
    def test_service_stability_after_errors(self):
        """
        Prueba: Estabilidad del servicio después de múltiples errores
        Verifica que el servicio siga funcionando después de errores
        """
        # Generar múltiples errores
        for _ in range(10):
            invalid_data = self.test_data.generate_invalid_product_missing_fields()
            response = self.api.create_product_invalid_data(invalid_data)
            assert response.status_code == 400
            self.metrics["requests_made"] += 1
            self.metrics["failed_requests"] += 1
        
        # Verificar que el servicio sigue funcionando correctamente
        health_response = self.api.get_health()
        assert health_response.status_code == 200, \
            "Service should remain healthy after multiple errors"
        
        health_data = health_response.json()
        assert health_data['status'] == 'healthy', \
            "Service status should remain healthy"
        
        # Verificar que se pueden crear productos válidos
        valid_product = self.test_data.generate_valid_product(
            custom_name="Post-Error Stability Test"
        )
        
        create_response = self.api.create_product(valid_product)
        assert create_response.status_code == 201, \
            "Should be able to create valid products after errors"
        
        self.metrics["requests_made"] += 2
        self.metrics["successful_requests"] += 2
        self.metrics["stability_test_passed"] = True
    
    @pytest.mark.error_handling
    @pytest.mark.integration
    def test_error_response_consistency(self):
        """
        Prueba: Consistencia de respuestas de error
        Verifica que todas las respuestas de error tengan formato consistente
        """
        error_scenarios = [
            (self.test_data.generate_invalid_product_missing_fields(), 400),
            (self.test_data.generate_invalid_product_wrong_types(), 400),
            (self.test_data.generate_invalid_product_negative_values(), 400),
            (self.test_data.generate_empty_product(), 400),
        ]
        
        for invalid_data, expected_status in error_scenarios:
            response = self.api.create_product_invalid_data(invalid_data)
            
            self.metrics["requests_made"] += 1
            
            # Verificar status code
            assert response.status_code == expected_status, \
                f"Expected {expected_status}, got {response.status_code}"
            
            # Verificar Content-Type
            assert self.validator.validate_content_type(response), \
                "All error responses should be JSON"
            
            # Verificar estructura
            error_data = self.validator.validate_json_response(response)
            assert error_data is not None, "Error response should be valid JSON"
            
            assert self.validator.validate_error_response(error_data, expected_status), \
                f"Inconsistent error response format: {self.validator.get_errors()}"
            
            # Verificar que el mensaje de error es descriptivo
            error_message = error_data.get('error', '')
            assert len(error_message) > 10, \
                f"Error message too short: '{error_message}'"
            
            self.metrics["failed_requests"] += 1
        
        self.metrics["error_consistency_test_passed"] = True
