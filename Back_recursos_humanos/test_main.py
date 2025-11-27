"""Pruebas unitarias para la API de Recursos Humanos"""
import pytest


class TestRootEndpoint:
    """Pruebas para el endpoint raíz"""

    def test_read_root(self, test_client):
        """Test: GET / debe retornar mensaje de bienvenida"""
        response = test_client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "HR API" in response.json()["message"]


class TestCreateEmpleado:
    """Pruebas para crear empleados (POST /empleados)"""

    def test_create_empleado_success(self, test_client, sample_empleado_data):
        """Test: Crear empleado con datos válidos"""
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == sample_empleado_data["nombre"]
        assert data["documento"] == sample_empleado_data["documento"]
        assert data["correo"] == sample_empleado_data["correo"]
        assert "id" in data

    def test_create_empleado_duplicate_documento(self, test_client, sample_empleado_data):
        """Test: No se puede crear empleado con documento duplicado"""
        # Crear primer empleado
        test_client.post("/empleados", json=sample_empleado_data)
        
        # Intentar crear segundo empleado con mismo documento
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 400
        assert "ya está registrado" in response.json()["detail"]

    def test_create_empleado_missing_required_fields(self, test_client):
        """Test: Falla al crear empleado sin campos requeridos"""
        invalid_data = {
            "correo": "test@example.com"
        }
        response = test_client.post("/empleados", json=invalid_data)
        assert response.status_code == 422

    def test_create_empleado_invalid_email(self, test_client, sample_empleado_data):
        """Test: Falla al crear empleado con email inválido"""
        sample_empleado_data["correo"] = "email-invalido"
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 422

    def test_create_empleado_negative_salary(self, test_client, sample_empleado_data):
        """Test: Falla al crear empleado con sueldo negativo"""
        sample_empleado_data["sueldo"] = -1000
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 422

    def test_create_empleado_with_optional_fields_null(self, test_client):
        """Test: Crear empleado solo con campos requeridos"""
        minimal_data = {
            "nombre": "María García",
            "documento": "9876543210"
        }
        response = test_client.post("/empleados", json=minimal_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == minimal_data["nombre"]
        assert data["documento"] == minimal_data["documento"]


class TestGetEmpleados:
    """Pruebas para obtener lista de empleados (GET /empleados)"""

    def test_get_empleados_empty(self, test_client):
        """Test: Obtener lista vacía cuando no hay empleados"""
        response = test_client.get("/empleados")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_empleados_with_data(self, test_client, sample_empleado_data):
        """Test: Obtener lista con empleados existentes"""
        # Crear algunos empleados
        test_client.post("/empleados", json=sample_empleado_data)
        
        sample_empleado_data["documento"] = "0987654321"
        sample_empleado_data["nombre"] = "Ana López"
        test_client.post("/empleados", json=sample_empleado_data)
        
        response = test_client.get("/empleados")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_empleados_pagination(self, test_client, sample_empleado_data):
        """Test: Paginación con skip y limit"""
        # Crear 5 empleados
        for i in range(5):
            sample_empleado_data["documento"] = f"doc{i}"
            sample_empleado_data["nombre"] = f"Empleado {i}"
            test_client.post("/empleados", json=sample_empleado_data)
        
        # Test skip=2, limit=2
        response = test_client.get("/empleados?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestGetEmpleadoById:
    """Pruebas para obtener empleado por ID (GET /empleados/{id})"""

    def test_get_empleado_by_id_success(self, test_client, sample_empleado_data):
        """Test: Obtener empleado existente por ID"""
        # Crear empleado
        create_response = test_client.post("/empleados", json=sample_empleado_data)
        empleado_id = create_response.json()["id"]
        
        # Obtener empleado por ID
        response = test_client.get(f"/empleados/{empleado_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == empleado_id
        assert data["nombre"] == sample_empleado_data["nombre"]

    def test_get_empleado_by_id_not_found(self, test_client):
        """Test: Error 404 cuando el empleado no existe"""
        response = test_client.get("/empleados/999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]


class TestUpdateEmpleado:
    """Pruebas para actualizar empleado (PUT /empleados/{id})"""

    def test_update_empleado_success(self, test_client, sample_empleado_data):
        """Test: Actualizar empleado con datos válidos"""
        # Crear empleado
        create_response = test_client.post("/empleados", json=sample_empleado_data)
        empleado_id = create_response.json()["id"]
        
        # Actualizar datos
        update_data = {
            "nombre": "Juan Carlos Pérez",
            "area": "Desarrollo",
            "sueldo": 4000000.00
        }
        response = test_client.put(f"/empleados/{empleado_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == update_data["nombre"]
        assert data["area"] == update_data["area"]
        assert float(data["sueldo"]) == update_data["sueldo"]

    def test_update_empleado_not_found(self, test_client):
        """Test: Error 404 al actualizar empleado inexistente"""
        update_data = {"nombre": "Test"}
        response = test_client.put("/empleados/999", json=update_data)
        assert response.status_code == 404

    def test_update_empleado_partial(self, test_client, sample_empleado_data):
        """Test: Actualización parcial mantiene otros campos"""
        # Crear empleado
        create_response = test_client.post("/empleados", json=sample_empleado_data)
        empleado_id = create_response.json()["id"]
        
        # Actualizar solo el teléfono
        update_data = {"telefono": "3109876543"}
        response = test_client.put(f"/empleados/{empleado_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["telefono"] == update_data["telefono"]
        assert data["nombre"] == sample_empleado_data["nombre"]
        assert data["correo"] == sample_empleado_data["correo"]


class TestDeleteEmpleado:
    """Pruebas para eliminar empleado (DELETE /empleados/{id})"""

    def test_delete_empleado_success(self, test_client, sample_empleado_data):
        """Test: Eliminar empleado existente"""
        # Crear empleado
        create_response = test_client.post("/empleados", json=sample_empleado_data)
        empleado_id = create_response.json()["id"]
        
        # Eliminar empleado
        response = test_client.delete(f"/empleados/{empleado_id}")
        assert response.status_code == 204
        
        # Verificar que ya no existe
        get_response = test_client.get(f"/empleados/{empleado_id}")
        assert get_response.status_code == 404

    def test_delete_empleado_not_found(self, test_client):
        """Test: Error 404 al eliminar empleado inexistente"""
        response = test_client.delete("/empleados/999")
        assert response.status_code == 404


class TestSearchByDocumento:
    """Pruebas para buscar empleado por documento"""

    def test_search_by_documento_success(self, test_client, sample_empleado_data):
        """Test: Buscar empleado por documento existente"""
        # Crear empleado
        test_client.post("/empleados", json=sample_empleado_data)
        
        # Buscar por documento
        documento = sample_empleado_data["documento"]
        response = test_client.get(f"/empleados/buscar/documento/{documento}")
        assert response.status_code == 200
        data = response.json()
        assert data["documento"] == documento
        assert data["nombre"] == sample_empleado_data["nombre"]

    def test_search_by_documento_not_found(self, test_client):
        """Test: Error 404 cuando el documento no existe"""
        response = test_client.get("/empleados/buscar/documento/999999999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]


class TestDataValidation:
    """Pruebas adicionales de validación de datos"""

    def test_nombre_too_long(self, test_client, sample_empleado_data):
        """Test: Falla con nombre demasiado largo"""
        sample_empleado_data["nombre"] = "A" * 101
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 422

    def test_documento_too_long(self, test_client, sample_empleado_data):
        """Test: Falla con documento demasiado largo"""
        sample_empleado_data["documento"] = "1" * 21
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 422

    def test_empty_nombre(self, test_client, sample_empleado_data):
        """Test: Falla con nombre vacío"""
        sample_empleado_data["nombre"] = ""
        response = test_client.post("/empleados", json=sample_empleado_data)
        assert response.status_code == 422
