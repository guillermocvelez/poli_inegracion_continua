<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Usar el nombre del contenedor para comunicación entre contenedores
// O localhost si accedes desde el navegador del host
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : 'http://hr-backend:8000'

interface Empleado {
  id: number
  nombre: string
  documento: string
  correo: string | null
  telefono: string | null
  area: string | null
  sueldo: number | null
  fecha_ingreso: string | null
}

interface EmpleadoForm {
  nombre: string
  documento: string
  correo: string
  telefono: string
  area: string
  sueldo: string
  fecha_ingreso: string
}

const empleados = ref<Empleado[]>([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)
const editingId = ref<number | null>(null)
const formData = ref<EmpleadoForm>({
  nombre: '',
  documento: '',
  correo: '',
  telefono: '',
  area: '',
  sueldo: '',
  fecha_ingreso: new Date().toISOString().split('T')[0]
})

// READ - Obtener todos los empleados
const fetchEmpleados = async () => {
  try {
    loading.value = true
    const response = await fetch(`${API_URL}/empleados`)
    if (!response.ok) throw new Error('Error al cargar empleados')
    empleados.value = await response.json()
    error.value = ''
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error desconocido'
  } finally {
    loading.value = false
  }
}

// CREATE - Crear nuevo empleado
const createEmpleado = async () => {
  try {
    const payload = {
      ...formData.value,
      sueldo: formData.value.sueldo ? parseFloat(formData.value.sueldo) : null,
      correo: formData.value.correo || null,
      telefono: formData.value.telefono || null,
      area: formData.value.area || null,
      fecha_ingreso: formData.value.fecha_ingreso || null
    }
    
    const response = await fetch(`${API_URL}/empleados`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Error al crear empleado')
    }
    
    await fetchEmpleados()
    closeModal()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al crear empleado'
  }
}

// UPDATE - Actualizar empleado
const updateEmpleado = async () => {
  if (!editingId.value) return
  
  try {
    const payload = {
      ...formData.value,
      sueldo: formData.value.sueldo ? parseFloat(formData.value.sueldo) : null,
      correo: formData.value.correo || null,
      telefono: formData.value.telefono || null,
      area: formData.value.area || null,
      fecha_ingreso: formData.value.fecha_ingreso || null
    }
    
    const response = await fetch(`${API_URL}/empleados/${editingId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Error al actualizar empleado')
    }
    
    await fetchEmpleados()
    closeModal()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al actualizar empleado'
  }
}

// DELETE - Eliminar empleado
const deleteEmpleado = async (id: number) => {
  if (!confirm('¿Estás seguro de eliminar este empleado?')) return
  
  try {
    const response = await fetch(`${API_URL}/empleados/${id}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) throw new Error('Error al eliminar empleado')
    
    await fetchEmpleados()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al eliminar empleado'
  }
}

// Abrir modal para crear
const openCreateModal = () => {
  editingId.value = null
  formData.value = {
    nombre: '',
    documento: '',
    correo: '',
    telefono: '',
    area: '',
    sueldo: '',
    fecha_ingreso: new Date().toISOString().split('T')[0]
  }
  showModal.value = true
}

// Abrir modal para editar
const openEditModal = (empleado: Empleado) => {
  editingId.value = empleado.id
  formData.value = {
    nombre: empleado.nombre,
    documento: empleado.documento,
    correo: empleado.correo || '',
    telefono: empleado.telefono || '',
    area: empleado.area || '',
    sueldo: empleado.sueldo?.toString() || '',
    fecha_ingreso: empleado.fecha_ingreso || ''
  }
  showModal.value = true
}

// Cerrar modal
const closeModal = () => {
  showModal.value = false
  editingId.value = null
  error.value = ''
}

// Enviar formulario
const handleSubmit = () => {
  if (editingId.value) {
    updateEmpleado()
  } else {
    createEmpleado()
  }
}

onMounted(() => {
  fetchEmpleados()
})
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="header-content">
          <div>
            <h1>💼 HR Management - Para la sustentación</h1>
            <p class="subtitle">Sistema de Gestión de Recursos Humanos</p>
          </div>
          <button @click="openCreateModal" class="btn-primary">
            <span class="icon">➕</span>
            Nuevo Empleado
          </button>
        </div>
      </div>
    </header>

    <main class="container">
      <div v-if="error" class="alert alert-error">
        <span class="alert-icon">⚠️</span>
        {{ error }}
        <button @click="error = ''" class="alert-close">✕</button>
      </div>
      
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando empleados...</p>
      </div>
      
      <div v-else-if="empleados.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>No hay empleados registrados</h3>
        <p>Comienza agregando tu primer empleado</p>
        <button @click="openCreateModal" class="btn-primary">
          <span class="icon">➕</span>
          Crear Empleado
        </button>
      </div>
      
      <div v-else class="table-container">
        <table class="empleados-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Documento</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>Área</th>
              <th>Sueldo</th>
              <th>Fecha de Ingreso</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="empleado in empleados" :key="empleado.id">
              <td>{{ empleado.nombre }}</td>
              <td>{{ empleado.documento }}</td>
              <td>{{ empleado.correo || 'N/A' }}</td>
              <td>{{ empleado.telefono || 'N/A' }}</td>
              <td>
                <span v-if="empleado.area" class="badge">{{ empleado.area }}</span>
                <span v-else>N/A</span>
              </td>
              <td class="salary">
                <span v-if="empleado.sueldo">${{ Number(empleado.sueldo).toLocaleString('es-CO') }}</span>
                <span v-else>N/A</span>
              </td>
              <td>
                <span v-if="empleado.fecha_ingreso">{{ new Date(empleado.fecha_ingreso).toLocaleDateString('es-CO') }}</span>
                <span v-else>N/A</span>
              </td>
              <td class="actions">
                <button class="btn-edit" @click="openEditModal(empleado)">
                  Editar
                </button>
                <button class="btn-delete" @click="deleteEmpleado(empleado.id)">
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal -->
    <Transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <h2>
              <span class="icon">{{ editingId ? '✏️' : '➕' }}</span>
              {{ editingId ? 'Editar Empleado' : 'Nuevo Empleado' }}
            </h2>
            <button @click="closeModal" class="btn-close">✕</button>
          </div>
          
          <form @submit.prevent="handleSubmit" class="modal-body">
            <div class="form-grid">
              <div class="form-group">
                <label for="nombre">
                  <span class="icon">👤</span>
                  Nombre Completo *
                </label>
                <input 
                  v-model="formData.nombre" 
                  id="nombre" 
                  type="text" 
                  placeholder="Ej: Juan Pérez"
                  required 
                />
              </div>
              
              <div class="form-group">
                <label for="documento">
                  <span class="icon">🆔</span>
                  Documento *
                </label>
                <input 
                  v-model="formData.documento" 
                  id="documento" 
                  type="text" 
                  placeholder="Ej: 1234567890"
                  required 
                />
              </div>
              
              <div class="form-group">
                <label for="correo">
                  <span class="icon">📧</span>
                  Correo Electrónico
                </label>
                <input 
                  v-model="formData.correo" 
                  id="correo" 
                  type="email" 
                  placeholder="correo@ejemplo.com"
                />
              </div>
              
              <div class="form-group">
                <label for="telefono">
                  <span class="icon">📱</span>
                  Teléfono
                </label>
                <input 
                  v-model="formData.telefono" 
                  id="telefono" 
                  type="tel" 
                  placeholder="Ej: 3001234567"
                />
              </div>
              
              <div class="form-group">
                <label for="area">
                  <span class="icon">🏢</span>
                  Área
                </label>
                <input 
                  v-model="formData.area" 
                  id="area" 
                  type="text" 
                  placeholder="Ej: Ventas, IT, RRHH"
                />
              </div>
              
              <div class="form-group">
                <label for="sueldo">
                  <span class="icon">💰</span>
                  Sueldo
                </label>
                <input 
                  v-model="formData.sueldo" 
                  id="sueldo" 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  placeholder="0.00"
                />
              </div>
              
              <div class="form-group full-width">
                <label for="fecha_ingreso">
                  <span class="icon">📅</span>
                  Fecha de Ingreso
                </label>
                <input 
                  v-model="formData.fecha_ingreso" 
                  id="fecha_ingreso" 
                  type="date" 
                />
              </div>
            </div>
            
            <div class="modal-actions">
              <button type="button" @click="closeModal" class="btn-secondary">
                Cancelar
              </button>
              <button type="submit" class="btn-primary">
                <span class="icon">{{ editingId ? '💾' : '➕' }}</span>
                {{ editingId ? 'Guardar Cambios' : 'Crear Empleado' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #6c757d;
  margin-bottom: 2rem;
}

.empleados-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

h2 {
  color: #495057;
  font-size: 1.5rem;
  margin: 0;
}

.alert {
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.alert-error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 6px;
  border: 1px solid #dee2e6;
}

.empleados-table {
  width: 100%;
  border-collapse: collapse;
}

.empleados-table thead {
  background: #f8f9fa;
}

.empleados-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

.empleados-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  color: #495057;
}

.empleados-table tbody tr:hover {
  background: #f8f9fa;
}

.empleados-table tbody tr:last-child td {
  border-bottom: none;
}

.badge {
  background: #007bff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  white-space: nowrap;
}

.salary {
  font-weight: 600;
  color: #28a745;
}

.actions {
  display: flex;
  gap: 0.5rem;
  white-space: nowrap;
}

/* Botones */
.btn-primary, .btn-secondary, .btn-edit, .btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-edit {
  background: #28a745;
  color: white;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.btn-edit:hover {
  background: #218838;
}

.btn-delete {
  background: #dc3545;
  color: white;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

.btn-delete:hover {
  background: #c82333;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  padding: 0;
  width: 2rem;
  height: 2rem;
}

.btn-close:hover {
  color: #212529;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style>
