# Pruebas Unitarias - API de Recursos Humanos

## 📋 Descripción

Este proyecto incluye pruebas unitarias completas para la API de gestión de empleados usando pytest y FastAPI TestClient.

## 🧪 Cobertura de Pruebas

Las pruebas cubren los siguientes aspectos:

### 1. **Endpoint Raíz** (`TestRootEndpoint`)

- ✅ Verificar mensaje de bienvenida

### 2. **Crear Empleados** (`TestCreateEmpleado`)

- ✅ Crear empleado con datos válidos
- ✅ Validar documento único (no duplicados)
- ✅ Validar campos requeridos
- ✅ Validar formato de email
- ✅ Validar sueldo no negativo
- ✅ Crear empleado solo con campos obligatorios

### 3. **Listar Empleados** (`TestGetEmpleados`)

- ✅ Obtener lista vacía
- ✅ Obtener lista con empleados
- ✅ Paginación (skip y limit)

### 4. **Obtener Empleado por ID** (`TestGetEmpleadoById`)

- ✅ Obtener empleado existente
- ✅ Error 404 para empleado inexistente

### 5. **Actualizar Empleado** (`TestUpdateEmpleado`)

- ✅ Actualizar con datos válidos
- ✅ Error 404 para empleado inexistente
- ✅ Actualización parcial de campos

### 6. **Eliminar Empleado** (`TestDeleteEmpleado`)

- ✅ Eliminar empleado existente
- ✅ Error 404 para empleado inexistente
- ✅ Verificar eliminación efectiva

### 7. **Buscar por Documento** (`TestSearchByDocumento`)

- ✅ Buscar empleado por documento existente
- ✅ Error 404 para documento inexistente

### 8. **Validación de Datos** (`TestDataValidation`)

- ✅ Validar longitud máxima de campos
- ✅ Validar campos no vacíos

## 🚀 Ejecutar las Pruebas

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar con salida detallada

```bash
pytest -v
```

### Ejecutar pruebas específicas

```bash
# Ejecutar una clase de pruebas
pytest test_main.py::TestCreateEmpleado

# Ejecutar una prueba específica
pytest test_main.py::TestCreateEmpleado::test_create_empleado_success
```

### Ejecutar con cobertura

```bash
# Instalar pytest-cov
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest --cov=. --cov-report=html

# Ver reporte en navegador
open htmlcov/index.html
```

### Ejecutar con reporte resumido

```bash
pytest --tb=short
```

## 📊 Estructura de las Pruebas

```
Back_recursos_humanos/
├── main.py              # API principal
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── database.py          # Configuración de BD
├── test_main.py         # Pruebas unitarias
├── pytest.ini           # Configuración pytest
├── .coveragerc          # Configuración cobertura
└── requirements.txt     # Dependencias
```

## 🔧 Configuración

Las pruebas usan una base de datos SQLite en memoria, por lo que:

- ✅ No afectan la base de datos de producción
- ✅ Son rápidas
- ✅ Se limpian automáticamente después de cada test
- ✅ No requieren configuración adicional

## 📝 Fixtures Disponibles

### `setup_database`

- Se ejecuta automáticamente antes de cada test
- Crea y limpia las tablas de la base de datos

### `sample_empleado_data`

- Proporciona datos de ejemplo para crear empleados
- Reutilizable en múltiples tests

## 🎯 Comandos Útiles

```bash
# Ver tests disponibles sin ejecutarlos
pytest --collect-only

# Ejecutar solo tests que fallaron la última vez
pytest --lf

# Ejecutar tests en paralelo (requiere pytest-xdist)
pip install pytest-xdist
pytest -n auto

# Detener en el primer fallo
pytest -x

# Mostrar print statements
pytest -s
```

## ✅ Ejemplo de Salida Exitosa

```
test_main.py::TestRootEndpoint::test_read_root PASSED
test_main.py::TestCreateEmpleado::test_create_empleado_success PASSED
test_main.py::TestCreateEmpleado::test_create_empleado_duplicate_documento PASSED
...
========================= 25 passed in 2.45s =========================
```

## 🔍 Debugging

Para debuggear un test específico:

```bash
# Agregar punto de interrupción en el código
import pdb; pdb.set_trace()

# Ejecutar con pdb
pytest --pdb
```

## 📦 Integración Continua

Las pruebas están diseñadas para integrarse fácilmente con GitHub Actions:

```yaml
- name: Run tests
  run: |
    cd Back_recursos_humanos
    pytest --cov=. --cov-report=xml
```
