# Proyecto de Recursos Humanos - Tests

Este proyecto incluye pruebas unitarias completas tanto para el backend como para el frontend.

## 🧪 Backend (FastAPI + Python)

### Cobertura: 95%

- **Framework**: pytest
- **Tests**: 22 pruebas
- **Archivo**: `Back_recursos_humanos/test_main.py`

### Ejecutar tests del backend:

```bash
cd Back_recursos_humanos
pytest -v
pytest --cov=. --cov-report=html
```

### Tests incluidos:

- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Validaciones de datos
- ✅ Manejo de errores
- ✅ Búsqueda por documento
- ✅ Documentos duplicados
- ✅ Campos requeridos

## 🎨 Frontend (Vue.js + TypeScript)

### Tests: 25 pruebas

- **Framework**: Vitest + Vue Test Utils
- **Archivo**: `Front_recursos_humanos/src/App.spec.ts`

### Ejecutar tests del frontend:

```bash
cd Front_recursos_humanos
npm install
npm test
npm run test:coverage
```

### Tests incluidos:

- ✅ Renderizado de componentes
- ✅ Operaciones CRUD (UI)
- ✅ Modales y formularios
- ✅ Manejo de errores
- ✅ Formato de datos
- ✅ Validaciones de formulario

## 🚀 Ejecutar todos los tests

### Localmente:

```bash
# Backend
cd Back_recursos_humanos && pytest -v

# Frontend
cd Front_recursos_humanos && npm test
```

### Con Docker:

```bash
# Backend
docker compose run --rm hr-backend pytest -v

# Frontend
docker compose run --rm hr-frontend npm test
```

## 📊 CI/CD

Los tests se ejecutan automáticamente en GitHub Actions en cada push a `main`:

```yaml
- Backend: pytest con cobertura
- Frontend: vitest con cobertura
- Build: Docker compose build de ambos servicios
```

## 📁 Estructura de Tests

```
proyecto/
├── Back_recursos_humanos/
│   ├── test_main.py         # Tests unitarios backend
│   ├── conftest.py          # Configuración pytest
│   ├── pytest.ini           # Config pytest
│   └── README_TESTS.md      # Documentación backend
│
├── Front_recursos_humanos/
│   ├── src/
│   │   └── App.spec.ts      # Tests unitarios frontend
│   ├── vitest.config.ts     # Config vitest
│   └── README_TESTS.md      # Documentación frontend
│
└── .github/
    └── workflows/
        └── ci.yml           # Pipeline CI/CD
```

## ✅ Resultados Esperados

### Backend:

```
========================= 22 passed =========================
Coverage: 95%
```

### Frontend:

```
Test Files  1 passed (1)
Tests  25 passed (25)
```

## 🔧 Troubleshooting

### Backend - Error de conexión a PostgreSQL

Las pruebas usan SQLite en memoria, no PostgreSQL. Asegúrate de que `TESTING=true` en el entorno.

### Frontend - Módulo no encontrado

```bash
cd Front_recursos_humanos
rm -rf node_modules package-lock.json
npm install
```

### Docker - Tests no se ejecutan

```bash
docker compose down -v
docker compose build --no-cache
docker compose run --rm hr-backend pytest -v
```

## 📚 Documentación Adicional

- [Backend Tests](Back_recursos_humanos/README_TESTS.md)
- [Frontend Tests](Front_recursos_humanos/README_TESTS.md)
- [GitHub Actions](.github/workflows/ci.yml)
