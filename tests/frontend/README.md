# Integration Tests for AgroWeb Login Component

Este directorio contiene las pruebas de integración para el componente de login del frontend de AgroWeb.

## Archivos

- `login_test.py` - Test de integración principal  
- `requirements.txt` - Dependencias necesarias para ejecutar las pruebas
- `README.md` - Este archivo de documentación
- `documentación*.pdf` - Reportes PDF generados automáticamente

## 🚀 Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Asegurar que Google Chrome esté instalado
- Descargar desde: https://www.google.com/chrome/

### 3. Configurar el Frontend
Antes de ejecutar las pruebas, el frontend debe estar corriendo:

```bash
cd ../..  # Regresar al directorio raíz del frontend
npm run dev
```

El frontend debería estar disponible en `http://localhost:5174`

## ▶️ Ejecución de las Pruebas

```bash
python login_test.py
```

## 🧪 Pruebas Incluidas

Las pruebas cubren los siguientes aspectos del componente de login:

### Pruebas de UI/UX
- ✅ Verificación de elementos del formulario
- ✅ Validación de campos vacíos  
- ✅ Funcionalidad del botón "mostrar/ocultar contraseña"
- ✅ Funcionalidad del botón "Entrar" con datos válidos
- ✅ Checkbox "Recuérdame"
- ✅ Navegación a página de registro
- ✅ Funcionalidad "Continuar como visitante"

## 📄 Generación de Reportes PDF

Cada vez que se ejecutan las pruebas, se genera automáticamente un reporte PDF con:

- ✅ **Logo de la Universidad Nacional** centrado en la parte superior
- ✅ **Resumen ejecutivo** con estadísticas de las pruebas
- ✅ **Fecha y hora** de ejecución  
- ✅ **Tabla detallada** con resultados de cada prueba
- ✅ **Estado de cada prueba** (PASSED/FAILED/ERROR)
- ✅ **Detalles de errores** si los hay

### Nomenclatura de archivos PDF:
- `documentación1.pdf` - Primer reporte
- `documentación2.pdf` - Segundo reporte (si el primero ya existe)
- `documentación3.pdf` - Y así sucesivamente...

Los archivos PDF se guardan automáticamente en el mismo directorio de las pruebas.

## 🔧 Configuración del Navegador

Por defecto, las pruebas se ejecutan con el navegador visible. Para ejecutar en modo headless (sin ventana visible), edita el archivo y descomenta la línea:

```python
# options.add_argument('--headless')  # Descomenta esta línea
```

## 💡 Notas

- El puerto del frontend está configurado como 5174 (según package.json)
- Las pruebas incluyen delays apropiados para permitir que la UI cargue
- Se incluyen mensajes informativos para facilitar el debugging
- Solo se ejecutan pruebas de UI que no requieren backend

## 🔧 Solución de Problemas

### Error: ChromeDriver no encontrado
- Verifica que Google Chrome esté instalado
- El test maneja automáticamente ChromeDriver

### Error: Puerto 5174 no disponible  
- Verifica que el frontend esté ejecutándose con `npm run dev`
- Revisa que no haya otro proceso usando el puerto

### Timeouts en las pruebas
- Verifica que tu máquina tenga suficientes recursos
- Aumenta los valores de timeout si es necesario

## Pruebas Incluidas

Las pruebas cubren los siguientes aspectos del componente de login:

### Pruebas de UI/UX
- ✅ Verificación de elementos del formulario
- ✅ Validación de campos vacíos
- ✅ Funcionalidad del botón "mostrar/ocultar contraseña"
- ✅ Checkbox "Recuérdame"
- ✅ Navegación a página de registro
- ✅ Funcionalidad "Continuar como visitante"

### Pruebas de Funcionalidad (requieren backend)
- ⚠️ Login exitoso con credenciales válidas
- ⚠️ Manejo de credenciales inválidas

## Configuración del Navegador

Por defecto, las pruebas se ejecutan con el navegador visible. Para ejecutar en modo headless (sin ventana visible), descomenta la línea:

```python
options.add_argument('--headless')
```

## Notas

- El puerto del frontend está configurado como 5174 (según package.json)
- Las pruebas incluyen delays apropiados para permitir que la UI cargue
- Se incluyen mensajes informativos para facilitar el debugging
- Las pruebas que requieren backend mostrarán advertencias si el backend no está disponible

## Solución de Problemas

### Error: ChromeDriver no encontrado
- Usa `login_test_with_manager.py` en su lugar
- O instala ChromeDriver manualmente y agrega al PATH

### Error: Puerto 5174 no disponible
- Verifica que el frontend esté ejecutándose con `npm run dev`
- Revisa que no haya otro proceso usando el puerto

### Timeouts en las pruebas
- Verifica que tu máquina tenga suficientes recursos
- Aumenta los valores de timeout si es necesario
