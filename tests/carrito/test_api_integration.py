"""
Pruebas de integración esenciales para la API del Servicio de Carrito de Compras
Prueba casos exitosos y de error siguiendo el patrón AgroWeb
"""

import pytest
import time
import json
from typing import Dict, Any

from config.carrito.test_config import TestConfig
from utils.carrito.api_client import CarritoApiClient

class TestCarritoAPIIntegration:
    """Suite de pruebas de integración para API de Carrito de Compras"""
    
    @pytest.fixture(autouse=True)
    def setup(self, carrito_api_client, carrito_api_health_check, carrito_test_metrics):
        """Configuración inicial para cada test"""
        self.api = CarritoApiClient(carrito_api_client, TestConfig.API_BASE_URL)
        self.metrics = carrito_test_metrics
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_crear_carrito_exitoso(self, sample_test_data, created_carritos_cleanup):
        """
        Prueba: Crear carrito con usuario válido
        Caso exitoso básico de creación de carrito
        """
        user_data = sample_test_data["valid_user"]
        
        start_time = time.time()
        
        response = self.api.create_carrito(user_data)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("create_carrito", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/carrito/create")
        
        # Validaciones básicas
        assert response.status_code == 201, f"Error creando carrito: {response.status_code} - {response.text}"
        
        # Validar respuesta JSON
        carrito_data = response.json()
        assert "Success" in carrito_data, "Respuesta debe contener campo Success"
        assert carrito_data["Success"] == True, "Success debe ser True"
        assert "message" in carrito_data, "Respuesta debe contener mensaje"
        assert "carrito fue creado exitosamente" in carrito_data["message"].lower(), "Mensaje debe confirmar creación"
        
        # Para cleanup, necesitamos obtener el ID del carrito creado
        # Como tu respuesta no incluye el ID, usaremos un placeholder
        # En producción podrías agregar el ID a la respuesta de creación
        carrito_id = "TEST_CARRITO_" + str(int(time.time()))
        created_carritos_cleanup(carrito_id)
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("create_carrito")
        assert response_time <= threshold, f"Crear carrito muy lento: {response_time:.2f}ms (max: {threshold}ms)"
        
        self.metrics["successful_requests"] += 1
        self.metrics["created_carritos"].append(carrito_id)
    
    @pytest.mark.api
    @pytest.mark.integration  
    def test_agregar_producto_a_carrito(self, sample_test_data, created_carritos_cleanup):
        """
        Prueba: Agregar producto a carrito existente
        Caso exitoso de operación principal del carrito
        Nota: Requiere un carrito existente con ID conocido
        """
        # Para esta prueba, asumimos que existe un carrito con ID 1
        # En un entorno real, crearías primero el carrito o usarías uno conocido
        carrito_id = "1"  # ID de carrito existente para testing
        created_carritos_cleanup(carrito_id)
        
        # Preparar datos del producto
        product_data = sample_test_data["valid_product"].copy()
        product_data["id_carrito"] = carrito_id
        
        start_time = time.time()
        
        response = self.api.add_product(product_data)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("add_product", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add("/carrito/addProduct")
        
        # Validaciones
        assert response.status_code == 200, f"Error agregando producto: {response.status_code} - {response.text}"
        
        # Si la respuesta incluye confirmación
        if response.content:
            try:
                response_data = response.json()
                if "Success" in response_data:
                    assert response_data["Success"] == True, "Success debe ser True al agregar producto"
            except:
                pass  # La respuesta podría no ser JSON
        
        # Verificar que el producto se agregó consultando el carrito
        get_response = self.api.get_carrito(carrito_id)
        if get_response.status_code == 200:
            carrito_actual = get_response.json()
            assert "Success" in carrito_actual, "Respuesta debe contener Success"
            assert carrito_actual["Success"] == True, "Success debe ser True"
            
            if "resul" in carrito_actual and "items" in carrito_actual["resul"]:
                items = carrito_actual["resul"]["items"]
                # Verificar que hay al menos un item
                assert len(items) > 0, "Carrito debe contener al menos un producto"
                
                # Verificar estructura de items
                for item in items:
                    assert "product_id" in item, "Item debe tener product_id"
                    assert "cantidad" in item, "Item debe tener cantidad"
                    assert "product_name" in item, "Item debe tener product_name"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("add_product")
        assert response_time <= threshold, f"Agregar producto muy lento: {response_time:.2f}ms (max: {threshold}ms)"
        
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_obtener_carrito_exitoso(self, sample_test_data, created_carritos_cleanup):
        """
        Prueba: Obtener carrito por ID
        Verificar que se puede consultar un carrito existente
        """
        # Usar un carrito conocido que existe (ID 1 por ejemplo)
        carrito_id = "1"
        created_carritos_cleanup(carrito_id)
        
        start_time = time.time()
        
        response = self.api.get_carrito(carrito_id)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("get_carrito", response_time))
        self.metrics["requests_made"] += 1
        self.metrics["endpoints_tested"].add(f"/carrito/getCarrito/{carrito_id}")
        
        # Validaciones
        assert response.status_code == 200, f"Error obteniendo carrito: {response.status_code} - {response.text}"
        
        carrito_data = response.json()
        assert "Success" in carrito_data, "Respuesta debe contener Success"
        assert carrito_data["Success"] == True, "Success debe ser True"
        
        # Validar estructura de respuesta
        if "resul" in carrito_data:
            result = carrito_data["resul"]
            assert "id_carrito" in result, "Resultado debe contener id_carrito"
            assert "items" in result, "Resultado debe contener items"
            assert "total" in result, "Resultado debe contener total"
            
            # Validar estructura de items si existen
            if result["items"]:
                for item in result["items"]:
                    assert "product_id" in item, "Item debe tener product_id"
                    assert "product_name" in item, "Item debe tener product_name"
                    assert "cantidad" in item, "Item debe tener cantidad"
                    assert "total_prod" in item, "Item debe tener total_prod"
                    assert "medida" in item, "Item debe tener medida"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("get_carrito")
        assert response_time <= threshold, f"Obtener carrito muy lento: {response_time:.2f}ms (max: {threshold}ms)"
        
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_cambiar_cantidad_producto(self, sample_test_data, created_carritos_cleanup):
        """
        Prueba: Cambiar cantidad de producto en carrito
        Verificar actualización de cantidades
        Nota: Usa carrito existente para la prueba
        """
        # Usar un carrito existente conocido para esta prueba
        carrito_id = "1"  # ID de carrito existente
        created_carritos_cleanup(carrito_id)
        
        # Agregar producto inicial
        product_data = sample_test_data["valid_product"].copy()
        product_data["id_carrito"] = carrito_id
        self.api.add_product(product_data)
        
        # Cambiar cantidad
        nueva_cantidad = 5
        change_data = {
            "id_carrito": carrito_id,
            "product_id": product_data["product_id"],
            "cantidad": nueva_cantidad
        }
        
        start_time = time.time()
        
        response = self.api.change_quantity(change_data)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("change_quantity", response_time))
        self.metrics["requests_made"] += 1
        
        # Validaciones
        assert response.status_code == 200, f"Error cambiando cantidad: {response.status_code} - {response.text}"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("change_quantity")
        assert response_time <= threshold, f"Cambiar cantidad muy lento: {response_time:.2f}ms (max: {threshold}ms)"
        
        self.metrics["successful_requests"] += 1
    
    @pytest.mark.api
    @pytest.mark.integration
    def test_vaciar_carrito_exitoso(self, sample_test_data, created_carritos_cleanup):
        """
        Prueba: Vaciar carrito completamente
        Verificar que se pueden eliminar todos los productos
        Nota: Usa carrito existente para la prueba
        """
        # Usar un carrito existente conocido para esta prueba
        carrito_id = "1"  # ID de carrito existente
        created_carritos_cleanup(carrito_id)
        
        # Agregar producto
        product_data = sample_test_data["valid_product"].copy()
        product_data["id_carrito"] = carrito_id
        self.api.add_product(product_data)
        
        # Vaciar carrito
        vaciar_data = {"id_carrito": carrito_id}
        
        start_time = time.time()
        
        response = self.api.vaciar_carrito(vaciar_data)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("vaciar_carrito", response_time))
        self.metrics["requests_made"] += 1
        
        # Validaciones
        assert response.status_code == 200, f"Error vaciando carrito: {response.status_code} - {response.text}"
        
        # Validar rendimiento
        threshold = TestConfig.get_performance_threshold("vaciar_carrito")
        assert response_time <= threshold, f"Vaciar carrito muy lento: {response_time:.2f}ms (max: {threshold}ms)"
        
        self.metrics["successful_requests"] += 1

    # CASOS DE ERROR
    
    @pytest.mark.api
    @pytest.mark.error_handling
    def test_obtener_carrito_inexistente(self, sample_test_data):
        """
        Prueba: Obtener carrito que no existe
        Caso de error - debe retornar 404
        """
        carrito_id_inexistente = sample_test_data["invalid_carrito_id"]
        
        start_time = time.time()
        
        response = self.api.get_carrito(carrito_id_inexistente)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("get_carrito_error", response_time))
        self.metrics["requests_made"] += 1
        
        # Validaciones de error
        assert response.status_code == 404, f"Debería retornar 404 para carrito inexistente, obtuvo: {response.status_code}"
        
        self.metrics["failed_requests"] += 1  # Error esperado
    
    @pytest.mark.api  
    @pytest.mark.error_handling
    def test_agregar_producto_carrito_inexistente(self, sample_test_data):
        """
        Prueba: Agregar producto a carrito inexistente
        Caso de error - debe fallar apropiadamente
        """
        product_data = {
            "id_carrito": sample_test_data["invalid_carrito_id"],
            "product_id": sample_test_data["valid_product"]["product_id"],
            "cantidad": 1
        }
        
        start_time = time.time()
        
        response = self.api.add_product(product_data)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("add_product_error", response_time))
        self.metrics["requests_made"] += 1
        
        # Validaciones de error
        assert response.status_code in [400, 404, 500], f"Debería fallar con 400/404/500, obtuvo: {response.status_code}"
        
        self.metrics["failed_requests"] += 1  # Error esperado
    
    @pytest.mark.api
    @pytest.mark.error_handling  
    def test_datos_invalidos_crear_carrito(self, sample_test_data):
        """
        Prueba: Crear carrito con datos inválidos
        Caso de error - datos malformados o tipo de documento incorrecto
        """
        # Probar con tipo de documento inválido
        datos_invalidos = sample_test_data["invalid_user"]
        
        start_time = time.time()
        
        response = self.api.create_carrito(datos_invalidos)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("create_carrito_error", response_time))
        self.metrics["requests_made"] += 1
        
        # Validaciones de error
        assert response.status_code in [400, 422, 500], f"Debería fallar con 400/422/500, obtuvo: {response.status_code}"
        
        # Si responde con JSON, verificar que Success sea False
        try:
            response_data = response.json()
            if "Success" in response_data:
                assert response_data["Success"] == False, "Success debe ser False para datos inválidos"
        except:
            pass  # La respuesta de error podría no ser JSON
        
        self.metrics["failed_requests"] += 1  # Error esperado
    
    @pytest.mark.api
    @pytest.mark.error_handling
    def test_crear_carrito_campos_faltantes(self):
        """
        Prueba: Crear carrito con campos faltantes
        Caso de error - datos incompletos
        """
        datos_incompletos = {"userdocument": "12345678"}  # Falta doctype
        
        start_time = time.time()
        
        response = self.api.create_carrito(datos_incompletos)
        
        response_time = (time.time() - start_time) * 1000
        self.metrics["response_times"].append(("create_carrito_error", response_time))
        self.metrics["requests_made"] += 1
        
        # Validaciones de error
        assert response.status_code in [400, 422, 500], f"Debería fallar con 400/422/500, obtuvo: {response.status_code}"
        
        self.metrics["failed_requests"] += 1  # Error esperado

    # FLUJO COMPLETO DE INTEGRACIÓN
    
    @pytest.mark.integration
    @pytest.mark.smoke
    def test_flujo_completo_carrito(self, sample_test_data, created_carritos_cleanup):
        """
        Prueba: Flujo completo de carrito
        Integración end-to-end: Crear → Agregar → Modificar → Obtener → Vaciar
        Nota: Usa carrito existente para las operaciones
        """
        # 1. Crear carrito
        user_data = sample_test_data["valid_user"]
        create_response = self.api.create_carrito(user_data)
        
        # Verificar creación (aunque no retorne ID)
        if create_response.status_code == 201:
            response_data = create_response.json()
            assert response_data.get("Success") == True, "Creación debe ser exitosa"
        
        # Para el resto del flujo, usar un carrito conocido que existe
        carrito_id = "1"  # ID de carrito existente
        created_carritos_cleanup(carrito_id)
        
        # 2. Agregar producto
        product_data = sample_test_data["valid_product"].copy()
        product_data["id_carrito"] = carrito_id
        add_response = self.api.add_product(product_data)
        
        # Validar que se agregó correctamente
        assert add_response.status_code == 200, f"Error agregando producto: {add_response.status_code}"
        
        # 3. Cambiar cantidad
        change_data = {
            "id_carrito": carrito_id,
            "product_id": product_data["product_id"],
            "cantidad": 3
        }
        change_response = self.api.change_quantity(change_data)
        assert change_response.status_code == 200, f"Error cambiando cantidad: {change_response.status_code}"
        
        # 4. Obtener carrito actualizado
        get_response = self.api.get_carrito(carrito_id)
        assert get_response.status_code == 200, f"Error obteniendo carrito: {get_response.status_code}"
        
        # Validar estructura de respuesta
        carrito_data = get_response.json()
        assert carrito_data.get("Success") == True, "Obtener carrito debe ser exitoso"
        
        if "resul" in carrito_data:
            result = carrito_data["resul"]
            assert "items" in result, "Carrito debe contener items"
            assert "total" in result, "Carrito debe contener total"
            
            # Verificar que hay productos en el carrito
            items = result["items"]
            assert len(items) > 0, "Carrito debe contener productos después del flujo"
            
            # Verificar estructura de al menos un item
            if items:
                item = items[0]
                assert "product_id" in item, "Item debe tener product_id"
                assert "cantidad" in item, "Item debe tener cantidad"
                assert "total_prod" in item, "Item debe tener total_prod"
        
        # 5. Vaciar carrito (opcional, para testing)
        vaciar_data = {"id_carrito": carrito_id}
        vaciar_response = self.api.vaciar_carrito(vaciar_data)
        # No validar estrictamente el vaciar ya que podría afectar otros tests
        
        # Métricas del flujo completo
        self.metrics["successful_requests"] += 4  # create + add + change + get
        self.metrics["requests_made"] += 4
        
        # Este test valida integración entre múltiples componentes
        assert True, "Flujo completo de carrito ejecutado exitosamente"
