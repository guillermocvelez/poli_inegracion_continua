# Pruebas Unitarias - Frontend Vue.js

## 📋 Descripción

Este proyecto incluye pruebas unitarias completas para el frontend de gestión de empleados usando Vitest y Vue Test Utils.

## 🧪 Cobertura de Pruebas

Las pruebas cubren los siguientes aspectos:

### 1. **Renderizado Inicial**

- ✅ Renderizar título principal
- ✅ Mostrar estado de carga

### 2. **Obtener Empleados (READ)**

- ✅ Cargar y mostrar lista de empleados
- ✅ Mostrar mensaje cuando no hay empleados
- ✅ Manejar errores de carga

### 3. **Crear Empleado (CREATE)**

- ✅ Abrir modal de creación
- ✅ Crear nuevo empleado
- ✅ Validar campos requeridos

### 4. **Actualizar Empleado (UPDATE)**

- ✅ Abrir modal de edición con datos
- ✅ Actualizar empleado correctamente

### 5. **Eliminar Empleado (DELETE)**

- ✅ Eliminar con confirmación
- ✅ Cancelar eliminación

### 6. **Manejo de Errores**

- ✅ Mostrar errores de creación
- ✅ Cerrar alertas de error

### 7. **Modal**

- ✅ Cerrar modal con botón cancelar
- ✅ Cerrar modal con botón X

### 8. **Formato de Datos**

- ✅ Formatear sueldo con separadores
- ✅ Formatear fechas correctamente

## 🚀 Ejecutar las Pruebas

### Instalar dependencias

```bash
npm install
```

### Ejecutar todas las pruebas

```bash
npm test
```

### Ejecutar con interfaz UI

```bash
npm run test:ui
```

### Ejecutar con cobertura

```bash
npm run test:coverage
```

### Modo watch (desarrollo)

```bash
npm test -- --watch
```

### Ejecutar pruebas específicas

```bash
# Ejecutar un archivo específico
npm test App.spec.ts

# Ejecutar tests que coincidan con un patrón
npm test -- -t "crear empleado"
```

## 📊 Estructura de las Pruebas

```
Front_recursos_humanos/
├── src/
│   ├── App.vue              # Componente principal
│   ├── App.spec.ts          # Pruebas unitarias
│   └── main.ts              # Entry point
├── vitest.config.ts         # Configuración Vitest
├── package.json             # Scripts y dependencias
└── README_TESTS.md          # Esta documentación
```

## 🔧 Configuración

Las pruebas usan:

- **Vitest**: Framework de testing rápido
- **Vue Test Utils**: Utilidades para testing de componentes Vue
- **jsdom**: Entorno DOM simulado
- **@vitest/coverage-v8**: Reporte de cobertura de código

## 📝 Mocks y Fixtures

### Mock de Fetch

```typescript
global.fetch = vi.fn();
```

### Mock de Confirm

```typescript
global.confirm = vi.fn(() => true);
```

### Datos de ejemplo

```typescript
const mockEmpleados = [
  {
    id: 1,
    nombre: "Juan Pérez",
    documento: "1234567890",
    correo: "juan@example.com",
    telefono: "3001234567",
    area: "Sistemas",
    sueldo: 3500000,
    fecha_ingreso: "2024-01-15",
  },
];
```

## 🎯 Comandos Útiles

```bash
# Ver cobertura en el navegador
npm run test:coverage
open coverage/index.html

# Ejecutar solo tests que fallaron
npm test -- --rerun-failed

# Ejecutar con reporter específico
npm test -- --reporter=verbose

# Generar reporte JSON
npm test -- --reporter=json --outputFile=test-results.json

# Modo debug
npm test -- --inspect-brk
```

## ✅ Ejemplo de Salida Exitosa

```
 ✓ src/App.spec.ts (25 tests) 1234ms
   ✓ Renderizado inicial (2 tests)
   ✓ Obtener empleados (3 tests)
   ✓ Crear empleado (3 tests)
   ✓ Actualizar empleado (2 tests)
   ✓ Eliminar empleado (2 tests)
   ✓ Manejo de errores (2 tests)
   ✓ Modal (2 tests)
   ✓ Formato de datos (2 tests)

Test Files  1 passed (1)
Tests  25 passed (25)
```

## 🔍 Debugging

Para debuggear un test específico:

```typescript
// Usar solo() para ejecutar un test
it.only("debe crear empleado", async () => {
  // test code
});

// Agregar console.log
console.log(wrapper.html());

// Inspeccionar componente
console.log(wrapper.vm);
```

## 📦 Integración Continua

Las pruebas están diseñadas para integrarse con GitHub Actions:

```yaml
- name: Run Frontend Tests
  run: |
    cd Front_recursos_humanos
    npm install
    npm test
    npm run test:coverage
```

## 🎨 Best Practices

1. **Usar `flushPromises()`** después de operaciones asíncronas
2. **Mock fetch** para evitar llamadas reales a la API
3. **Limpiar mocks** con `beforeEach`
4. **Probar comportamiento**, no implementación
5. **Usar selectores semánticos** cuando sea posible
6. **Mantener tests independientes** entre sí

## 📈 Cobertura Esperada

- **Statements**: > 80%
- **Branches**: > 75%
- **Functions**: > 80%
- **Lines**: > 80%

## 🛠️ Troubleshooting

### Error: Cannot find module 'vitest'

```bash
npm install --save-dev vitest @vue/test-utils jsdom
```

### Error: ReferenceError: fetch is not defined

```typescript
global.fetch = vi.fn();
```

### Tests muy lentos

```bash
# Usar happy-dom en lugar de jsdom
npm install --save-dev happy-dom
```

Luego en `vitest.config.ts`:

```typescript
test: {
  environment: "happy-dom";
}
```
