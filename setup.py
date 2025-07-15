"""
Script de configuración inicial para el entorno de pruebas de integración
Configura dependencias, directorios y verifica requisitos
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_directory_structure():
    """Crear estructura de directorios necesaria"""
    directories = [
        "reports",
        "config/university_assets",
        "reporting/templates",
        "tests",
        "utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def install_dependencies():
    """Instalar dependencias de Python"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crear archivo .env desde .env.example si no existe"""
    env_file = ".env"
    example_file = "config/.env.example"
    
    if not os.path.exists(env_file) and os.path.exists(example_file):
        with open(example_file, 'r') as src:
            content = src.read()
        
        with open(env_file, 'w') as dst:
            dst.write(content)
        
        print(f"✅ Archivo {env_file} creado desde {example_file}")
    else:
        print(f"ℹ️ Archivo {env_file} ya existe o {example_file} no encontrado")

def verify_api_connection():
    """Verificar conexión con el API"""
    try:
        import requests
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API de productos disponible")
            return True
        else:
            print(f"⚠️ API responde con código {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al API en http://localhost:5000")
        print("💡 Asegúrate de ejecutar:")
        print("   1. docker-compose up -d")
        print("   2. python app.py")
        return False
    except ImportError:
        print("⚠️ Requests no instalado, no se puede verificar API")
        return False

def create_sample_test_config():
    """Crear configuración de prueba de ejemplo"""
    config = {
        "test_environment": "integration",
        "api_base_url": "http://localhost:5000",
        "timeout_seconds": 30,
        "retry_attempts": 3,
        "generate_pdf_reports": True,
        "university_info": {
            "name": "Universidad Nacional de Colombia",
            "faculty": "Facultad de Ingeniería",
            "course": "Ingeniería de Software II",
            "team": "Capibaras Team"
        }
    }
    
    config_file = "config/test_settings.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuración de pruebas creada: {config_file}")

def main():
    """Función principal de configuración"""
    print("🛠️  CONFIGURACIÓN INICIAL - PRUEBAS DE INTEGRACIÓN AGROWEB")
    print("=" * 60)
    
    # Verificar versión de Python
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    
    # Crear estructura de directorios
    print("\n📁 Creando estructura de directorios...")
    create_directory_structure()
    
    # Instalar dependencias
    print("\n📦 Configurando dependencias...")
    if not install_dependencies():
        print("⚠️ Algunas dependencias pueden no haberse instalado correctamente")
    
    # Crear archivo de configuración
    print("\n⚙️ Configurando entorno...")
    create_env_file()
    create_sample_test_config()
    
    # Verificar conectividad
    print("\n🔍 Verificando servicios...")
    api_available = verify_api_connection()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE CONFIGURACIÓN")
    print("=" * 60)
    
    print("✅ Estructura de directorios creada")
    print("✅ Dependencias instaladas") 
    print("✅ Archivos de configuración creados")
    
    if api_available:
        print("✅ API de productos accesible")
        print("\n🚀 ¡Todo listo! Puedes ejecutar las pruebas con:")
        print("   python -m pytest tests/ -v")
        print("   o")
        print("   ./run_tests.bat")
    else:
        print("⚠️ API de productos no accesible")
        print("\n🔧 Para continuar:")
        print("   1. Inicia la infraestructura: docker-compose up -d") 
        print("   2. Inicia el API: python app.py")
        print("   3. Ejecuta las pruebas: ./run_tests.bat")
    
    print("\n📄 Los reportes se generarán en el directorio 'reports/'")
    print("📊 Incluye reportes HTML, JSON, JUnit y PDF profesional")

if __name__ == "__main__":
    main()
