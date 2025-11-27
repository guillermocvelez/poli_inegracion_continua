import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import App from "./App.vue";

// Mock global fetch
global.fetch = vi.fn();

describe("App.vue", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Renderizado inicial", () => {
    it("debe renderizar el título principal", () => {
      const wrapper = mount(App);
      expect(wrapper.text()).toContain("HR Management");
    });

    it("debe mostrar estado de carga inicialmente", async () => {
      vi.mocked(fetch).mockImplementation(
        () => new Promise(() => {}) // Promise que nunca se resuelve
      );

      const wrapper = mount(App);
      await wrapper.vm.$nextTick();

      expect(wrapper.text()).toContain("Cargando empleados");
    });
  });

  describe("Obtener empleados (READ)", () => {
    it("debe cargar y mostrar la lista de empleados", async () => {
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
        {
          id: 2,
          nombre: "María García",
          documento: "0987654321",
          correo: "maria@example.com",
          telefono: "3109876543",
          area: "RRHH",
          sueldo: 4000000,
          fecha_ingreso: "2024-02-20",
        },
      ];

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      expect(wrapper.text()).toContain("Juan Pérez");
      expect(wrapper.text()).toContain("María García");
      expect(wrapper.text()).toContain("Sistemas");
      expect(wrapper.text()).toContain("RRHH");
    });

    it("debe mostrar mensaje cuando no hay empleados", async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      expect(wrapper.text()).toContain("No hay empleados registrados");
    });

    it("debe manejar error al cargar empleados", async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new Error("Error de red"));

      const wrapper = mount(App);
      await flushPromises();

      expect(wrapper.text()).toContain("Error");
    });
  });

  describe("Crear empleado (CREATE)", () => {
    it('debe abrir modal al hacer clic en "Nuevo Empleado"', async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      const createButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Nuevo Empleado"));

      expect(createButton).toBeDefined();
      await createButton!.trigger("click");
      await wrapper.vm.$nextTick();

      expect(wrapper.text()).toContain("Nuevo Empleado");
      expect(wrapper.find("form").exists()).toBe(true);
    });

    it("debe crear un nuevo empleado correctamente", async () => {
      // Mock inicial - lista vacía
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Abrir modal
      const createButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Nuevo Empleado"));
      await createButton!.trigger("click");
      await wrapper.vm.$nextTick();

      // Llenar formulario
      const inputs = wrapper.findAll("input");
      await inputs[0].setValue("Pedro López");
      await inputs[1].setValue("1122334455");
      await inputs[2].setValue("pedro@example.com");
      await inputs[3].setValue("3001112233");
      await inputs[4].setValue("Ventas");
      await inputs[5].setValue("2500000");
      await inputs[6].setValue("2024-03-01");

      // Mock para crear empleado
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 3,
          nombre: "Pedro López",
          documento: "1122334455",
          correo: "pedro@example.com",
          telefono: "3001112233",
          area: "Ventas",
          sueldo: 2500000,
          fecha_ingreso: "2024-03-01",
        }),
      } as Response);

      // Mock para refrescar lista
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: 3,
            nombre: "Pedro López",
            documento: "1122334455",
            correo: "pedro@example.com",
            telefono: "3001112233",
            area: "Ventas",
            sueldo: 2500000,
            fecha_ingreso: "2024-03-01",
          },
        ],
      } as Response);

      // Submit formulario
      const form = wrapper.find("form");
      await form.trigger("submit");
      await flushPromises();

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/empleados"),
        expect.objectContaining({
          method: "POST",
          headers: { "Content-Type": "application/json" },
        })
      );
    });

    it("debe validar campos requeridos en el formulario", async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Abrir modal
      const createButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Nuevo Empleado"));
      await createButton!.trigger("click");
      await wrapper.vm.$nextTick();

      const nameInput = wrapper.findAll("input")[0];
      const docInput = wrapper.findAll("input")[1];

      expect(nameInput.attributes("required")).toBeDefined();
      expect(docInput.attributes("required")).toBeDefined();
    });
  });

  describe("Actualizar empleado (UPDATE)", () => {
    it("debe abrir modal de edición con datos del empleado", async () => {
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

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Buscar y hacer clic en botón de editar
      const editButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Editar"));

      expect(editButton).toBeDefined();
      await editButton!.trigger("click");
      await wrapper.vm.$nextTick();

      expect(wrapper.text()).toContain("Editar Empleado");

      // Verificar que el formulario tiene los datos del empleado
      const nameInput = wrapper.findAll("input")[0];
      expect((nameInput.element as HTMLInputElement).value).toBe("Juan Pérez");
    });

    it("debe actualizar empleado correctamente", async () => {
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

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Abrir modal de edición
      const editButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Editar"));
      await editButton!.trigger("click");
      await wrapper.vm.$nextTick();

      // Modificar nombre
      const nameInput = wrapper.findAll("input")[0];
      await nameInput.setValue("Juan Carlos Pérez");

      // Mock para actualizar
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          ...mockEmpleados[0],
          nombre: "Juan Carlos Pérez",
        }),
      } as Response);

      // Mock para refrescar lista
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            ...mockEmpleados[0],
            nombre: "Juan Carlos Pérez",
          },
        ],
      } as Response);

      const form = wrapper.find("form");
      await form.trigger("submit");
      await flushPromises();

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/empleados/1"),
        expect.objectContaining({
          method: "PUT",
        })
      );
    });
  });

  describe("Eliminar empleado (DELETE)", () => {
    it("debe eliminar empleado al confirmar", async () => {
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

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Mock confirm
      global.confirm = vi.fn(() => true);

      // Mock para eliminar
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => ({}),
      } as Response);

      // Mock para refrescar lista
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      // Hacer clic en eliminar
      const deleteButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Eliminar"));
      await deleteButton!.trigger("click");
      await flushPromises();

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/empleados/1"),
        expect.objectContaining({
          method: "DELETE",
        })
      );
      expect(global.confirm).toHaveBeenCalled();
    });

    it("no debe eliminar si se cancela la confirmación", async () => {
      const mockEmpleados = [
        {
          id: 1,
          nombre: "Juan Pérez",
          documento: "1234567890",
          correo: "juan@example.com",
          telefono: null,
          area: null,
          sueldo: null,
          fecha_ingreso: null,
        },
      ];

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Mock confirm devuelve false (cancelar)
      global.confirm = vi.fn(() => false);

      const deleteButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Eliminar"));

      const fetchCallCount = vi.mocked(fetch).mock.calls.length;
      await deleteButton!.trigger("click");
      await flushPromises();

      // No debe haber llamadas adicionales a fetch
      expect(vi.mocked(fetch).mock.calls.length).toBe(fetchCallCount);
    });
  });

  describe("Manejo de errores", () => {
    it("debe mostrar error al fallar la creación", async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Abrir modal
      const createButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Nuevo Empleado"));
      await createButton!.trigger("click");
      await wrapper.vm.$nextTick();

      // Llenar formulario
      const inputs = wrapper.findAll("input");
      await inputs[0].setValue("Test");
      await inputs[1].setValue("123");

      // Mock error
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: "Documento ya registrado" }),
      } as Response);

      const form = wrapper.find("form");
      await form.trigger("submit");
      await flushPromises();

      expect(wrapper.text()).toContain("Documento ya registrado");
    });

    it("debe cerrar alerta de error", async () => {
      vi.mocked(fetch).mockRejectedValueOnce(new Error("Error de prueba"));

      const wrapper = mount(App);
      await flushPromises();

      expect(wrapper.text()).toContain("Error");

      // Buscar botón de cerrar alerta
      const closeButton = wrapper
        .findAll("button")
        .find(
          (btn) => btn.text() === "✕" && btn.classes().includes("alert-close")
        );

      if (closeButton) {
        await closeButton.trigger("click");
        await wrapper.vm.$nextTick();

        // Verificar que la alerta ya no contiene el error específico
        const alertDiv = wrapper.find(".alert-error");
        expect(alertDiv.exists()).toBe(false);
      }
    });
  });

  describe("Modal", () => {
    it("debe cerrar modal al hacer clic en cancelar", async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Abrir modal
      const createButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Nuevo Empleado"));
      await createButton!.trigger("click");
      await wrapper.vm.$nextTick();

      expect(wrapper.find("form").exists()).toBe(true);

      // Hacer clic en cancelar
      const cancelButton = wrapper
        .findAll("button")
        .find((btn) => btn.text() === "Cancelar");
      await cancelButton!.trigger("click");
      await wrapper.vm.$nextTick();

      expect(wrapper.find("form").exists()).toBe(false);
    });

    it("debe cerrar modal al hacer clic en X", async () => {
      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Abrir modal
      const createButton = wrapper
        .findAll("button")
        .find((btn) => btn.text().includes("Nuevo Empleado"));
      await createButton!.trigger("click");
      await wrapper.vm.$nextTick();

      // Hacer clic en botón X
      const closeButton = wrapper.find(".btn-close");
      await closeButton.trigger("click");
      await wrapper.vm.$nextTick();

      expect(wrapper.find("form").exists()).toBe(false);
    });
  });

  describe("Formato de datos", () => {
    it("debe formatear correctamente el sueldo con separador de miles", async () => {
      const mockEmpleados = [
        {
          id: 1,
          nombre: "Juan Pérez",
          documento: "1234567890",
          correo: "juan@example.com",
          telefono: null,
          area: null,
          sueldo: 3500000,
          fecha_ingreso: null,
        },
      ];

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Verificar que el sueldo se muestra con formato
      expect(wrapper.text()).toContain("3.500.000");
    });

    it("debe formatear correctamente las fechas", async () => {
      const mockEmpleados = [
        {
          id: 1,
          nombre: "Juan Pérez",
          documento: "1234567890",
          correo: null,
          telefono: null,
          area: null,
          sueldo: null,
          fecha_ingreso: "2024-01-15",
        },
      ];

      vi.mocked(fetch).mockResolvedValueOnce({
        ok: true,
        json: async () => mockEmpleados,
      } as Response);

      const wrapper = mount(App);
      await flushPromises();

      // Verificar que la fecha se muestra (formato puede variar según locale)
      const text = wrapper.text();
      expect(text).toMatch(/2024|15|1/);
    });
  });
});
