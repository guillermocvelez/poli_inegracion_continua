<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Empleado {
  id: number
  nombre: string
  documento: string
  correo: string
  telefono: string
  area: string
  sueldo: number
  fecha_ingreso: string
}

const empleados = ref<Empleado[]>([])
const loading = ref(true)
const error = ref('')

const fetchEmpleados = async () => {
  try {
    const response = await fetch('http://localhost:8000/empleados')
    if (!response.ok) throw new Error('Error al cargar empleados')
    empleados.value = await response.json()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error desconocido'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchEmpleados()
})
</script>

<template>
  <div class="container">
    <h1>Proyecto entrega Integración continua Politécnico Grancolombiano</h1>
    <h2>Hacemos un cambio menor dentro del código para probar el webhook</h2>
    
    <div class="empleados-section">
      <h2>Lista de Empleados</h2>
      
      <div v-if="loading" class="message">Cargando empleados...</div>
      <div v-else-if="error" class="message error">{{ error }}</div>
      <div v-else-if="empleados.length === 0" class="message">No hay empleados registrados</div>
      
      <div v-else class="empleados-list">
        <div v-for="empleado in empleados" :key="empleado.id" class="empleado-card">
          <div class="empleado-header">
            <h3>{{ empleado.nombre }}</h3>
            <span class="badge">{{ empleado.area || 'Sin área' }}</span>
          </div>
          <div class="empleado-info">
            <p><strong>Documento:</strong> {{ empleado.documento }}</p>
            <p><strong>Correo:</strong> {{ empleado.correo || 'N/A' }}</p>
            <p><strong>Teléfono:</strong> {{ empleado.telefono || 'N/A' }}</p>
            <p><strong>Sueldo:</strong> ${{ Number(empleado.sueldo).toLocaleString() }}</p>
            <p><strong>Fecha Ingreso:</strong> {{ empleado.fecha_ingreso }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.empleados-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

h2 {
  color: #495057;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.message {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.message.error {
  color: #dc3545;
}

.empleados-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.empleado-card {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 1.25rem;
  transition: box-shadow 0.2s;
}

.empleado-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.empleado-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e9ecef;
}

.empleado-header h3 {
  margin: 0;
  color: #212529;
  font-size: 1.1rem;
}

.badge {
  background: #007bff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.empleado-info p {
  margin: 0.5rem 0;
  color: #495057;
  font-size: 0.95rem;
}

.empleado-info strong {
  color: #212529;
}
</style>
