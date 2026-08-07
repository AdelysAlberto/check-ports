# Documento de Requerimientos de Producto (PRD)
## Project Name: Ubuntu Port Inspector & Guard

> *"Te estoy observando... siempre te observo. Sin el papeleo en regla no se escribe una sola línea de código."* — **Roz**

---

## 1. Visión del Producto
Una herramienta de escritorio nativa para **Ubuntu Linux** (Python + PySide6) que permita monitorear, auditar y gestionar puertos de red abiertos y procesos vinculados en tiempo real. Proporciona una interfaz dividida en 2 columnas con clasificación inteligente de puertos (Comunes del sistema vs. No Comunes/Apps), detalles técnicos profundos y una base de conocimientos local en español para enriquecimiento automático.

---

## 2. Requerimientos Funcionales (MoSCoW)

### Must Have (Indispensable para el MVP)
- **FR-01: Escaneo y Detección Automática de Puertos**:
  - Detección de sockets escucha (TCP/UDP) activos en el sistema Ubuntu mediante `psutil` / `ss` / `/proc`.
  - Captura del número de puerto, protocolo (TCP/UDP), dirección local/remota, PID del proceso, nombre del proceso y usuario ejecutor.
- **FR-02: Clasificación en Columna Izquierda**:
  - Renderizado de la lista de puertos categorizados en:
    - **Puertos Comunes de Ubuntu**: SSH (22), DNS (53), HTTP (80), HTTPS (443), CUPS (631), Systemd-resolved (5353/53), etc.
    - **Puertos No Comunes / Personalizados**: Puertos de desarrollo (3000, 5173, 8080, 5432, 27017, etc.) y sockets desconocidos.
  - Indicadores visuales de estado y filtro rápido por búsqueda de puerto o proceso.
- **FR-03: Panel Extendido de Detalle (Columna Derecha)**:
  - Al hacer clic en un puerto de la lista, despliega:
    - Identificación del proceso: PID, nombre ejecutable, ruta completa (`/usr/bin/...`), línea de comandos con argumentos, usuario y consumo de recursos básico.
    - Información del socket: Dirección IP, máscara, estado del listener.
    - **Enriquecimiento de Conocimiento Local**: Si el sistema operativo no provee descripción detallada, se consulta automáticamente el archivo `ports_knowledge.json` local.
- **FR-04: Botones de Acción y Control de Procesos**:
  - **Cerrar Puerto / Matar Proceso**: Botón dedicado para enviar señales `SIGTERM` (cierre limpio) o `SIGKILL` (cierre forzado) al PID.
  - **Copiar Información**: Copia rápida al portapapeles de los detalles del puerto/proceso.
  - **Actualizar / Recargar**: Botón manual de refresco + auto-refresco configurable.
- **FR-05: Archivo de Base de Conocimiento de Puertos (`ports_knowledge.json`)**:
  - Archivo estructurado local pre-poblado con más de 100 puertos estándar y de desarrollo, incluyendo nombre común, descripción técnica en español, nivel de riesgo y recomendaciones de seguridad.

### Should Have (Deseable V1.1)
- **FR-06: Elevación de Privilegios Integrada**:
  - Detección si la app corre como usuario no-root y sugerencia/diálogo para solicitar permisos `sudo` y visibilidad completa de PIDs protegidos.
- **FR-07: Exportación de Reportes**:
  - Exportación de la lista de puertos activos en formato JSON o CSV.

### Could Have (Futuras iteraciones)
- **FR-08: Notificaciones del Sistema**:
  - Alerta en el área de notificación cuando un nuevo puerto no común se abra en el sistema.

---

## 3. Criterios de Aceptación
1. Al abrir la app en Ubuntu, la lista de puertos se carga en menos de 1 segundo.
2. Cada puerto seleccionado despliega en la columna derecha la información del PID, usuario, binario y la descripción traída del archivo local `ports_knowledge.json`.
3. El botón "Matar Proceso" finaliza el proceso seleccionado previa confirmación visual del usuario.
