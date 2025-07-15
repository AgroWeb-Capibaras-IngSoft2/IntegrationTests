"""
Generador de datos de prueba para integration testing del Servicio de Gestión de Productos
Proporciona datos válidos e inválidos siguiendo el patrón AgroWeb
"""

from datetime import datetime
from typing import Dict, Any, List
import random
import uuid

class ProductTestDataGenerator:
    """Generador de datos de prueba para productos AgroWeb"""
    
    # Categorías válidas según la API
    VALID_CATEGORIES = ["vegetables", "fruits", "dairy", "herbs"]
    
    # Categorías inválidas para testing de errores
    INVALID_CATEGORIES = ["invalid_cat", "VEGETABLES", "123", "", None]
    
    # Nombres base para productos por categoría
    PRODUCT_NAMES = {
        'vegetables': [
            'Lechuga Crespa', 'Espinaca Baby', 'Apio Fresco', 'Acelga Verde', 
            'Rúgula Orgánica', 'Brócoli', 'Coliflor', 'Zanahoria', 'Cebolla Cabezona'
        ],
        'fruits': [
            'Mango Tommy', 'Papaya Maradol', 'Banano Bocadillo', 'Piña Gold', 
            'Maracuyá', 'Guayaba Pera', 'Lulo', 'Mora de Castilla', 'Fresa'
        ],
        'herbs': [
            'Cilantro', 'Perejil Crespo', 'Albahaca', 'Orégano', 'Tomillo', 
            'Romero', 'Hierbabuena', 'Yerbabuena', 'Cebollín'
        ],
        'dairy': [
            'Leche Entera', 'Queso Campesino', 'Yogurt Natural', 'Mantequilla', 
            'Cuajada', 'Queso Doble Crema', 'Kumis', 'Suero Costeño'
        ]
    }
    
    # Orígenes colombianos
    ORIGINS = [
        'Boyacá', 'Cundinamarca', 'Antioquia', 'Tolima', 'Huila', 'Nariño',
        'Valle del Cauca', 'Santander', 'Córdoba', 'Meta', 'Quindío', 'Risaralda'
    ]
    
    # Unidades de medida
    UNITS = [
        '1kg', '500g', '250g', '1 unidad', 'Docena', 'Racimo', 
        'Atado', '2kg', '300g', 'Libra', 'Costal'
    ]
    
    # Descripciones base
    DESCRIPTIONS = [
        "Producto fresco cultivado en la región andina colombiana con certificación de calidad",
        "Alimento orgánico certificado de alta calidad nutricional y sabor excepcional",
        "Producto tradicional de la agricultura colombiana, cultivado por productores locales",
        "Cosecha reciente de productores certificados con técnicas sostenibles",
        "Producto seleccionado de las mejores fincas del país para consumo directo"
    ]
    
    def __init__(self):
        self.generated_product_names = set()
        self.test_counter = 0
    
    def generate_valid_product(self, 
                              category: str = None,
                              custom_name: str = None,
                              custom_price: float = None,
                              custom_stock: int = None) -> Dict[str, Any]:
        """Generar producto válido con datos realistas"""
        
        self.test_counter += 1
        
        # Seleccionar categoría
        selected_category = category or random.choice(self.VALID_CATEGORIES)
        
        # Generar nombre único
        if custom_name:
            product_name = custom_name
        else:
            base_names = self.PRODUCT_NAMES.get(selected_category, ['Producto Genérico'])
            base_name = random.choice(base_names)
            
            # Generar variaciones del nombre para unicidad
            variations = [
                f"{base_name} Test {self.test_counter}",
                f"{base_name} Premium Test",
                f"{base_name} Orgánico Test",
                f"{base_name} de Exportación Test",
                f"{base_name} Fresco Test"
            ]
            
            product_name = random.choice(variations)
            
            # Asegurar unicidad
            while product_name in self.generated_product_names:
                product_name = f"{base_name} Test {self.test_counter}_{random.randint(1000, 9999)}"
            
            self.generated_product_names.add(product_name)
        
        # Generar precio realista según categoría
        if custom_price is not None:
            price = custom_price
        else:
            price_ranges = {
                'vegetables': (800, 4000),
                'fruits': (1200, 6000),
                'herbs': (500, 2500),
                'dairy': (2000, 8000)
            }
            price_range = price_ranges.get(selected_category, (1000, 5000))
            price = round(random.uniform(price_range[0], price_range[1]), 2)
        
        # Generar stock
        if custom_stock is not None:
            stock = custom_stock
        else:
            stock = random.randint(0, 500)
        
        # Seleccionar otros campos
        unit = random.choice(self.UNITS)
        origin = random.choice(self.ORIGINS)
        description = random.choice(self.DESCRIPTIONS)
        
        # URL de imagen realista
        image_name = product_name.lower().replace(' ', '_').replace('ó', 'o').replace('ñ', 'n')
        image_url = f"http://localhost:5000/static/catalog/{image_name}.jpg"
        
        return {
            "name": product_name,
            "category": selected_category,
            "price": price,
            "unit": unit,
            "imageUrl": image_url,
            "stock": stock,
            "origin": origin,
            "description": f"{description}. {product_name} de excelente calidad.",
            "isActive": True,
            # Campos opcionales
            "originalPrice": round(price * 1.2, 2) if random.choice([True, False]) else None,
            "isOrganic": random.choice([True, False]),
            "isBestSeller": random.choice([True, False]),
            "freeShipping": random.choice([True, False])
        }
    
    def generate_invalid_product_missing_fields(self) -> Dict[str, Any]:
        """Generar producto con campos faltantes para testing de errores"""
        return {
            "name": "Producto Incompleto Test",
            "category": "vegetables"
            # Faltan: price, unit, imageUrl, stock, origin, description, isActive
        }
    
    def generate_invalid_product_wrong_types(self) -> Dict[str, Any]:
        """Generar producto con tipos de datos incorrectos"""
        return {
            "name": "Producto Tipos Incorrectos",
            "category": "vegetables",
            "price": "precio_no_numerico",  # Debe ser número
            "unit": "1kg",
            "imageUrl": "http://localhost:5000/static/test.jpg",
            "stock": "stock_no_numerico",  # Debe ser entero
            "origin": "Bogotá",
            "description": "Producto con tipos incorrectos",
            "isActive": "true"  # Debe ser booleano
        }
    
    def generate_invalid_product_negative_values(self) -> Dict[str, Any]:
        """Generar producto con valores negativos"""
        return {
            "name": "Producto Valores Negativos",
            "category": "vegetables",
            "price": -1500.0,  # Precio negativo
            "unit": "1kg",
            "imageUrl": "http://localhost:5000/static/test.jpg",
            "stock": -10,  # Stock negativo
            "origin": "Bogotá",
            "description": "Producto con valores negativos para testing",
            "isActive": True
        }
    
    def generate_invalid_product_invalid_category(self) -> Dict[str, Any]:
        """Generar producto con categoría inválida"""
        return {
            "name": "Producto Categoría Inválida",
            "category": random.choice(self.INVALID_CATEGORIES),
            "price": 2500.0,
            "unit": "1kg",
            "imageUrl": "http://localhost:5000/static/test.jpg",
            "stock": 50,
            "origin": "Bogotá",
            "description": "Producto con categoría inválida",
            "isActive": True
        }
    
    def generate_empty_product(self) -> Dict[str, Any]:
        """Generar producto completamente vacío"""
        return {}
    
    def generate_product_with_very_long_strings(self) -> Dict[str, Any]:
        """Generar producto con strings excesivamente largos"""
        long_string = "A" * 1000  # String de 1000 caracteres
        
        return {
            "name": long_string,
            "category": "vegetables",
            "price": 2500.0,
            "unit": "1kg",
            "imageUrl": "http://localhost:5000/static/test.jpg",
            "stock": 50,
            "origin": long_string,
            "description": long_string,
            "isActive": True
        }
    
    def generate_bulk_products(self, count: int, category: str = None) -> List[Dict[str, Any]]:
        """Generar múltiples productos para testing de carga"""
        products = []
        for i in range(count):
            product = self.generate_valid_product(
                category=category,
                custom_name=f"Bulk Test Product {i+1}"
            )
            products.append(product)
        return products
    
    def generate_products_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generar productos por cada categoría válida"""
        products_by_category = {}
        
        for category in self.VALID_CATEGORIES:
            products_by_category[category] = [
                self.generate_valid_product(category=category)
                for _ in range(3)  # 3 productos por categoría
            ]
        
        return products_by_category
    
    def generate_edge_case_products(self) -> List[Dict[str, Any]]:
        """Generar productos para casos extremos"""
        return [
            # Producto con stock 0
            self.generate_valid_product(custom_stock=0),
            
            # Producto con precio mínimo
            self.generate_valid_product(custom_price=0.01),
            
            # Producto con precio muy alto
            self.generate_valid_product(custom_price=999999.99),
            
            # Producto con stock muy alto
            self.generate_valid_product(custom_stock=999999),
            
            # Producto con nombre muy corto
            self.generate_valid_product(custom_name="A"),
            
            # Producto con todos los campos opcionales como None/False
            {
                "name": "Producto Minimalista Test",
                "category": "vegetables",
                "price": 1000.0,
                "unit": "1kg",
                "imageUrl": "http://localhost:5000/static/minimal.jpg",
                "stock": 10,
                "origin": "Bogotá",
                "description": "Producto con campos opcionales mínimos",
                "isActive": True,
                "originalPrice": None,
                "isOrganic": False,
                "isBestSeller": False,
                "freeShipping": False
            }
        ]

class TestScenarios:
    """Escenarios de prueba predefinidos"""
    
    @staticmethod
    def get_performance_test_data(num_products: int = 100) -> List[Dict[str, Any]]:
        """Datos para pruebas de rendimiento"""
        generator = ProductTestDataGenerator()
        return generator.generate_bulk_products(num_products)
    
    @staticmethod
    def get_error_test_cases() -> List[Dict[str, Any]]:
        """Casos de prueba para manejo de errores"""
        generator = ProductTestDataGenerator()
        return [
            generator.generate_invalid_product_missing_fields(),
            generator.generate_invalid_product_wrong_types(),
            generator.generate_invalid_product_negative_values(),
            generator.generate_invalid_product_invalid_category(),
            generator.generate_empty_product(),
            generator.generate_product_with_very_long_strings()
        ]
    
    @staticmethod
    def get_integration_test_data() -> List[Dict[str, Any]]:
        """Datos para pruebas de integración completas"""
        generator = ProductTestDataGenerator()
        
        # Un producto por cada categoría válida
        integration_products = []
        for category in generator.VALID_CATEGORIES:
            product = generator.generate_valid_product(
                category=category,
                custom_name=f"Integration Test {category.title()}"
            )
            integration_products.append(product)
        
        # Agregar casos extremos
        integration_products.extend(generator.generate_edge_case_products())
        
        return integration_products
