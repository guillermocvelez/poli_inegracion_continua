"""Configuración de pytest y fixtures compartidos"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Configurar variable de entorno para tests ANTES de importar la aplicación
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["TESTING"] = "true"

# Ahora podemos importar la aplicación
from main import app, get_db
from models import Base

# Configurar base de datos de prueba en memoria
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Sobrescribe la dependencia de base de datos para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def test_client():
    """Cliente de test de FastAPI"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Crea y limpia la base de datos antes de cada test"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def sample_empleado_data():
    """Datos de ejemplo para crear empleados"""
    return {
        "nombre": "Juan Pérez",
        "documento": "1234567890",
        "correo": "juan.perez@example.com",
        "telefono": "3001234567",
        "area": "Sistemas",
        "sueldo": 3500000.00,
        "fecha_ingreso": "2024-01-15"
    }
